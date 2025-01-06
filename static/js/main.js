document.addEventListener("DOMContentLoaded", function () {
    const togglePassword = document.querySelectorAll('.toggle-password');
    const form = document.getElementById('password-reset-form');
    const newPassword1 = document.getElementById('new_password1');
    const newPassword2 = document.getElementById('new_password2');
    const alertBox = document.getElementById('confirm-alert');
    const successBlock = document.getElementById('password-reset-success');

    // Função para alternar entre mostrar/ocultar senha
    togglePassword.forEach(item => {
        item.addEventListener('click', function () {
            const input = this.previousElementSibling;
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            this.querySelector('i').classList.toggle('fa-eye');
            this.querySelector('i').classList.toggle('fa-eye-slash');
        });
    });

    // Validação e submissão do formulário
    form.addEventListener('submit', function (e) {
        e.preventDefault(); // Impede o envio padrão do formulário

        // Verifica se as senhas coincidem
        if (newPassword1.value !== newPassword2.value) {
            alertBox.classList.remove('hidden');
            alertBox.classList.add('visible');
            setTimeout(function () {
                alertBox.classList.remove('visible');
                alertBox.classList.add('hidden');
            }, 5000);
        } else {
            // Se as senhas coincidirem, envia os dados para o backend
            fetch(form.action, {
                method: "POST",
                body: new FormData(form),
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(data); // Para verificar a estrutura do objeto
                if (data.success) {
                    // Exibe o bloco de sucesso e oculta o formulário
                    form.classList.add('hidden');
                    successBlock.classList.remove('hidden');
                    successBlock.classList.add('visible');
                } else {
                    alertBox.classList.remove('hidden');
                    alertBox.textContent = typeof data.error === 'string' ? data.error : "Ocorreu um erro.";
                }
            })
        }
    });
});
