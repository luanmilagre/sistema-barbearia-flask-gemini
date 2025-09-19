import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, timedelta
import os
import google.generativeai as genai


app = Flask(__name__)

# --- CONFIGURAÇÃO DA API GEMINI ---
# Pega a chave da variável de ambiente que configuramos
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Modelo rápido e eficiente


# --- FUNÇÃO PARA CONECTAR AO BANCO DE DADOS ---
def get_db_connection():
    conn = sqlite3.connect('barbearia.db')
    # Retorna as linhas como dicionários, o que é muito mais fácil de trabalhar
    conn.row_factory = sqlite3.Row
    return conn

# --- FUNÇÃO AUXILIAR PARA GERAR HORÁRIOS ---
# (Esta função permanece a mesma da versão anterior)
def gerar_horarios_disponiveis(data):
    horarios = []
    try:
        data_obj = datetime.strptime(data, "%Y-%m-%d")
        if data_obj.weekday() == 6: # 6 é Domingo
            return [] # Retorna lista vazia se for domingo
    except ValueError:
        return [] # Retorna vazio se a data for inválida

    hora_inicio = datetime.strptime(data + " 09:00", "%Y-%m-%d %H:%M")
    hora_fim = datetime.strptime(data + " 18:30", "%Y-%m-%d %H:%M")
    intervalo = timedelta(minutes=30)
    horario_atual = hora_inicio

    while horario_atual <= hora_fim:
        horarios.append(horario_atual.strftime("%H:%M"))
        horario_atual += intervalo
    return horarios

# --- ROTAS DA APLICAÇÃO ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/horarios/<data>')
def get_horarios(data):
    """Busca os horários no banco de dados para a data fornecida."""
    conn = get_db_connection()
    # Seleciona apenas a coluna da hora onde a data corresponde
    agendamentos_db = conn.execute('SELECT hora_agendamento FROM agendamentos WHERE data_agendamento = ?', (data,)).fetchall()
    conn.close()

    # Cria uma lista apenas com os horários (ex: ['10:00', '14:30'])
    horarios_agendados = [item['hora_agendamento'] for item in agendamentos_db]
    
    todos_os_horarios = gerar_horarios_disponiveis(data)
    
    horarios_com_status = []
    for horario in todos_os_horarios:
        if horario in horarios_agendados:
            horarios_com_status.append({"horario": horario, "status": "ocupado"})
        else:
            horarios_com_status.append({"horario": horario, "status": "disponivel"})
            
    return jsonify(horarios_com_status)

@app.route('/agendar', methods=['POST'])
def agendar():
    """Insere um novo agendamento no banco de dados."""
    dados = request.json
    nome = dados.get('nome')
    data = dados.get('data')
    horario = dados.get('horario')

    if not nome or not data or not horario:
        return jsonify({"sucesso": False, "mensagem": "Dados incompletos."}), 400

    conn = get_db_connection()
    
    # Verifica se o horário já não foi agendado
    existente = conn.execute('SELECT id FROM agendamentos WHERE data_agendamento = ? AND hora_agendamento = ?', (data, horario)).fetchone()
    
    if existente:
        conn.close()
        return jsonify({"sucesso": False, "mensagem": "Este horário já foi agendado enquanto você escolhia."}), 409

    # Insere os dados no banco
    conn.execute('INSERT INTO agendamentos (nome_cliente, data_agendamento, hora_agendamento) VALUES (?, ?, ?)',
                 (nome, data, horario))
    conn.commit()
    conn.close()
    
    return jsonify({"sucesso": True, "mensagem": f"Agendamento para {nome} às {horario} confirmado!"})

# A partir daqui, adicionaremos a lógica do Gemini.
@app.route('/chat', methods=['POST'])
def chat():
    """Recebe a mensagem do usuário, processa com o Gemini e retorna a resposta."""
    mensagem_usuario = request.json.get('mensagem')

    if not mensagem_usuario:
        return jsonify({"resposta": "Mensagem vazia."}), 400

    # ---- Lógica para dar contexto à IA ----
    # Obtemos a data de hoje para o contexto.
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    
    # Buscamos os horários já agendados para hoje para dar contexto à IA
    conn = get_db_connection()
    agendamentos_db = conn.execute('SELECT hora_agendamento FROM agendamentos WHERE data_agendamento = ?', (data_hoje,)).fetchall()
    conn.close()
    horarios_agendados_hoje = [item['hora_agendamento'] for item in agendamentos_db]
    
    # Criamos um prompt bem detalhado para a IA saber como agir
    prompt_contextual = f"""
    Você é um assistente virtual da 'Duque Barberia'. Seja amigável e direto.
    A data de hoje é {data_hoje}.
    Os preços são: Corte - R$40, Barba - R$30, Combo (Corte + Barba) - R$65.
    O horário de funcionamento é de Segunda a Sábado, das 09:00 às 18:30. Não abrimos aos Domingos.
    Os horários já agendados para HOJE ({data_hoje}) são: {', '.join(horarios_agendados_hoje) if horarios_agendados_hoje else 'nenhum horário agendado ainda'}.
    
    Com base neste contexto, responda à seguinte pergunta do cliente: "{mensagem_usuario}"
    
    Se o cliente perguntar sobre horários disponíveis para hoje, use a lista de horários agendados para deduzir e informar os que estão livres.
    Se o cliente perguntar sobre outra data, informe que você só consegue ver os horários de hoje, e que para outras datas ele deve usar o calendário na página.
    """
    
    try:
        response = model.generate_content(prompt_contextual)
        resposta_ia = response.text
    except Exception as e:
        print(f"Erro na API do Gemini: {e}")
        resposta_ia = "Desculpe, estou com um problema de conexão com minha inteligência. Tente novamente mais tarde."

    return jsonify({"resposta": resposta_ia})
# Por enquanto, a aplicação já está funcional com o banco de dados.

# --- ROTAS DE ADMINISTRAÇÃO ---

@app.route('/admin')
def admin():
    """Mostra a página de administração com todos os agendamentos."""
    conn = get_db_connection()
    # Pega todos os agendamentos, ordenando por data e hora para ficar organizado
    agendamentos = conn.execute('SELECT * FROM agendamentos ORDER BY data_agendamento, hora_agendamento').fetchall()
    conn.close()
    # Envia a lista de agendamentos para um novo template chamado admin.html
    return render_template('admin.html', agendamentos=agendamentos)


@app.route('/excluir/<int:id>', methods=['POST'])
def excluir_agendamento(id):
    """Exclui um agendamento com base no seu ID único."""
    conn = get_db_connection()
    conn.execute('DELETE FROM agendamentos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    # Redireciona o usuário de volta para a página de administração
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)