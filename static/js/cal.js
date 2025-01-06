document.addEventListener('DOMContentLoaded', function() {
    const demandaForm = document.getElementById('demandaForm');
    const calendarioContainer = document.getElementById('calendarioContainer'); // Adicione um contêiner para o calendário
    const calendarioUrl = "{% url 'calendario' %}";

    demandaForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(demandaForm);
        fetch(calendarioUrl, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Atualizar o calendário
                carregarCalendario();
                // Exibir feedback
                mostrarFeedback(data.message);
                // Resetar o formulário
                demandaForm.reset();
            } else {
                // Exibir erros
                mostrarErros(data.errors);
            }
        })
        .catch(error => console.error('Erro:', error));
    });

    function carregarCalendario() {
        fetch(calendarioUrl, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
        .then(response => response.json())
        .then(data => {
            calendarioContainer.innerHTML = data.html;
        })
        .catch(error => console.error('Erro ao carregar o calendário:', error));
    }

    // Função para obter o CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Verifica se o cookie começa com o nome desejado
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function mostrarFeedback(message) {
        // Implemente a exibição de feedback ao usuário
        alert(message);
    }

    function mostrarErros(errors) {
        // Implemente a exibição de erros ao usuário
        let errorMessages = '';
        for (let field in errors) {
            errors[field].forEach(error => {
                errorMessages += `${field}: ${error}\n`;
            });
        }
        alert(errorMessages);
    }

    // Carregar o calendário ao carregar a página
    carregarCalendario();
});
