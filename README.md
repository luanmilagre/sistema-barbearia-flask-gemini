# 💈 Sistema de Agendamento para Barbearia com IA

![Badge da Licença](https://img.shields.io/badge/license-MIT-blue.svg)

Sistema web completo para o gerenciamento de agendamentos em uma barbearia, integrado com um assistente de IA (Google Gemini) para interações inteligentes.

---

## 🚀 Funcionalidades Principais

* **Agendamento Online:** Clientes podem visualizar horários disponíveis e marcar um serviço.
* **Painel Administrativo:** Área para o administrador gerenciar, confirmar e cancelar agendamentos.
* **Assistente com IA:** Chatbot integrado com a API do Gemini para responder dúvidas comuns dos clientes.
* **Autenticação de Usuários:** Sistema de login seguro para administradores e funcionários.
* **Banco de Dados:** Armazenamento persistente de clientes e agendamentos utilizando SQLite.

---

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído com as seguintes tecnologias:

* **Backend:**
    * ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
    * ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
* **Frontend:**
    * ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
    * ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
    * ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
* **Banco de Dados:**
    * ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white) (Gerenciado com DB Browser for SQLite)
* **IA:**
    * Google Gemini API

---

## 🔧 Como Executar o Projeto Localmente

Siga os passos abaixo para rodar o projeto na sua máquina.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git](https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git)
    cd NOME-DO-REPOSITORIO
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    * Crie um arquivo `.env` na raiz do projeto.
    * Adicione sua chave da API do Gemini: `GEMINI_API_KEY="SUA_CHAVE_AQUI"`
    * (Lembre-se de adaptar seu código para ler esta variável de ambiente em vez de tê-la no código)

5.  **Inicialize o banco de dados (se necessário):**
    ```bash
    python init_db.py
    ```

6.  **Execute a aplicação:**
    ```bash
    flask run
    ```
    Acesse `http://127.0.0.1:5000` no seu navegador.

---

## 📸 Screenshots

(# 💈 Sistema de Agendamento para Barbearia com IA
## 📸 Screenshots

Aqui estão algumas telas que demonstram o sistema em funcionamento:

**Tela de Agendamento de Horários**
![Tela principal onde o cliente escolhe a data e o horário para o agendamento.](screenshots/agendamento.png)

**Agendamento Confirmado**
![Tela de confirmação após um agendamento bem-sucedido.](screenshots/agendamento-feito.png)

**Painel de Administração (Sem Agendamentos)**
![Painel onde o administrador pode visualizar e gerenciar os agendamentos.](screenshots/painel-admin.png)

**Painel de Administração (Com Agendamentos)**
![Painel de administração exibindo a lista de agendamentos existentes.](screenshots/painel-adm-com-agendamento.png)

**Exemplo de Interação com o Chatbot**
![Exemplo de interação com o chatbot inteligente, respondendo a perguntas dos clientes.](screenshots/capturar.png)

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE.md) para mais detalhes.