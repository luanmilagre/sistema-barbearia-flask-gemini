// Espera o documento HTML ser completamente carregado para executar o script
document.addEventListener('DOMContentLoaded', () => {

    // --- SELETORES DE ELEMENTOS ---
    const datePicker = document.getElementById('date-picker');
    const horariosContainer = document.getElementById('horarios-container');

    // Elementos do Modal
    const modal = document.getElementById('booking-modal');
    const closeModalButton = document.querySelector('.close-button');
    const bookingForm = document.getElementById('booking-form');
    const selectedDateField = document.getElementById('selected-date');
    const selectedTimeField = document.getElementById('selected-time');
    let dataSelecionada = '';
    let horarioSelecionado = '';

    // --- LÓGICA DE AGENDAMENTO ---

    // Define a data mínima para hoje para não agendar no passado
    const hoje = new Date().toISOString().split('T')[0];
    datePicker.setAttribute('min', hoje);

    // Função para buscar e exibir os horários
    async function carregarHorarios(data) {
        // Limpa horários antigos
        horariosContainer.innerHTML = '<p>Selecione uma data para ver os horários...</p>';
        if (!data) return;

        horariosContainer.innerHTML = '<p>Carregando horários...</p>';

        try {
            // Faz uma requisição GET para a nossa API em Python
            const response = await fetch(`/horarios/${data}`);
            const horarios = await response.json();

            horariosContainer.innerHTML = ''; // Limpa o "Carregando..."

            if (horarios.length === 0) {
                horariosContainer.innerHTML = '<p>Domingo não abrimos ou não há horários disponíveis. Por favor, selecione outro dia!</p>';
                return;
            }

            // Cria um botão para cada horário retornado pela API
            horarios.forEach(item => {
                const button = document.createElement('button');
                button.classList.add('horario', item.status);
                button.textContent = item.horario;
                button.dataset.horario = item.horario;

                if (item.status === 'disponivel') {
                    button.addEventListener('click', () => abrirModalAgendamento(data, item.horario));
                } else {
                    button.disabled = true;
                }

                horariosContainer.appendChild(button);
            });

        } catch (error) {
            console.error("Erro ao carregar horários:", error);
            horariosContainer.innerHTML = '<p>Não foi possível carregar os horários. Tente novamente.</p>';
        }
    }

    // Evento que dispara a busca de horários quando a data muda
    datePicker.addEventListener('change', () => {
        dataSelecionada = datePicker.value;
        carregarHorarios(dataSelecionada);
    });

    // Função para abrir o modal
    function abrirModalAgendamento(data, horario) {
        horarioSelecionado = horario;
        selectedDateField.textContent = new Date(data + 'T00:00:00').toLocaleDateString(); // Formata a data
        selectedTimeField.textContent = horario;
        modal.style.display = 'flex'; // Exibe o modal
    }

    // Função para fechar o modal
    function fecharModal() {
        modal.style.display = 'none';
        bookingForm.reset(); // Limpa o formulário
    }

    // Eventos para fechar o modal
    closeModalButton.addEventListener('click', fecharModal);
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            fecharModal();
        }
    });

    // Evento de envio do formulário de agendamento
    bookingForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Impede o recarregamento da página

        const nomeCliente = document.getElementById('client-name').value;

        const dadosAgendamento = {
            nome: nomeCliente,
            data: dataSelecionada,
            horario: horarioSelecionado
        };

        try {
            // Envia os dados para a API em Python usando POST
            const response = await fetch('/agendar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dadosAgendamento)
            });

            const resultado = await response.json();

            if (resultado.sucesso) {
                alert(resultado.mensagem);
                fecharModal();
                carregarHorarios(dataSelecionada); // Recarrega os horários para mostrar o novo agendamento
            } else {
                alert(`Erro: ${resultado.mensagem}`);
            }

        } catch (error) {
            console.error("Erro ao agendar:", error);
            alert("Ocorreu um erro ao tentar agendar. Tente novamente.");
        }
    });

    // --- LÓGICA DO CHATBOT COM IA ---
    // ESTA É A ÚNICA SEÇÃO DO CHATBOT QUE DEVE EXISTIR.
    // A versão antiga (simulada) foi removida.
    const chatHeader = document.getElementById('chat-header');
    const chatBody = document.getElementById('chat-body');
    const toggleChatIcon = document.getElementById('toggle-chat-icon');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendChatBtn = document.getElementById('send-chat-btn');

    // Abrir/Fechar o chat
    chatHeader.addEventListener('click', () => {
        chatBody.classList.toggle('hidden');
        chatHeader.classList.toggle('chat-closed');
        toggleChatIcon.textContent = chatBody.classList.contains('hidden') ? '+' : '−';
    });

    // Função para adicionar mensagem no chat
    function adicionarMensagem(texto, tipo) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${tipo}-message`);
        messageDiv.innerHTML = `<p>${texto}</p>`;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // NOVA FUNÇÃO para enviar mensagem para o Backend com IA
    async function enviarMensagemParaIA() {
        const textoUsuario = chatInput.value.trim();
        if (!textoUsuario) return;

        adicionarMensagem(textoUsuario, 'user');
        chatInput.value = '';

        // Adiciona uma mensagem de "digitando..."
        adicionarMensagem("Digitando...", 'bot');

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ mensagem: textoUsuario })
            });

            const data = await response.json();

            // Remove a mensagem de "digitando..."
            chatMessages.removeChild(chatMessages.lastChild);

            adicionarMensagem(data.resposta, 'bot');

        } catch (error) {
            console.error("Erro ao contatar a IA:", error);
            // Remove a mensagem de "digitando..."
            chatMessages.removeChild(chatMessages.lastChild);
            adicionarMensagem("Não foi possível obter uma resposta. Verifique sua conexão.", 'bot');
        }
    }

    // Eventos para enviar mensagem (atualizados para chamar a nova função)
    sendChatBtn.addEventListener('click', enviarMensagemParaIA);
    chatInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            enviarMensagemParaIA();
        }
    });

}); // <-- ESTE É O FECHAMENTO DO 'DOMContentLoaded' LÁ DO COMEÇO