document.addEventListener("DOMContentLoaded", function () {
    const fields = ["name", "email", "password", "message"];

    // Recuperar valores salvos e preencher os campos ao carregar a página
    fields.forEach(field => {
        const savedValue = localStorage.getItem(field);
        if (savedValue) {
            document.getElementById(field).value = savedValue;
        }
    });

    // Salvar o valor no LocalStorage sempre que o usuário digitar em um campo
    fields.forEach(field => {
        const input = document.getElementById(field);
        input.addEventListener("input", function () {
            localStorage.setItem(field, this.value);
        });
    });

    // Limpar os dados do LocalStorage ao enviar o formulário (opcional)
    document.querySelector("form").addEventListener("submit", function () {
        fields.forEach(field => localStorage.removeItem(field));
    });
});





