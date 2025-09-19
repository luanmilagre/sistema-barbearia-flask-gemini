import sqlite3

# Conecta ao banco de dados (cria o arquivo se ele não existir)
connection = sqlite3.connect('barbearia.db')

# Abre o arquivo schema.sql para ler os comandos de criação da tabela
with open('schema.sql') as f:
    connection.executescript(f.read())

# Cria um cursor para executar comandos
cur = connection.cursor()

# (Opcional) Insere um agendamento de exemplo para teste
cur.execute("INSERT INTO agendamentos (nome_cliente, data_agendamento, hora_agendamento) VALUES (?, ?, ?)",
            ('Cliente Teste', '2025-10-10', '14:00')
            )

# Salva as alterações e fecha a conexão
connection.commit()
connection.close()

print("Banco de dados inicializado com sucesso.")