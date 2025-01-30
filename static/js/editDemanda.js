// static/js/script.js

function initSidebarEvents() {
  const itensSidebar = document.querySelectorAll(".item-sidebar");
  const conteudoPrincipal = document.getElementById("conteudo-principal");

  itensSidebar.forEach(function (item) {
    item.addEventListener("click", function (e) {
      e.preventDefault();
      const url = this.getAttribute("data-url");

      fetch(url, {
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          conteudoPrincipal.innerHTML = data.html;

          // Reaplica os eventos após carregar o conteúdo via AJAX
          initFormEvents(); // Reaplica os eventos do formulário
          initActionButtons(); // Reaplica os eventos dos botões de ação
          initEditFormEvent(); // Reaplica a funcionalidade de edição
          initVerMaisModal(); // Reaplica a funcionalidade "Ver Mais"
          initDeletarDemandas(); // Reaplica a funcionalidade de deletar demandas
          initExcluirSelecionados(); // Reaplica a funcionalidade de exclusão em massas
          initSelecionarTodos(); // Reaplica a funcionalidade de seleção de todos
          initExcluirMembros(); // Reaplica a funcionalidade de exclusão de membros
          init();
          
        })
        .catch((error) => console.error("Erro ao carregar a aba:", error));
    });
  });
}

document.addEventListener('DOMContentLoaded', function() {
    init();

    function init() {
        // Botões de editar
        const editButtons = document.querySelectorAll('.edit-button');
        editButtons.forEach(button => {
            button.addEventListener('click', openEditModal);
        });

        // Botões de fechar modais
        const closeButtons = document.querySelectorAll('.close-button');
        closeButtons.forEach(button => {
            button.addEventListener('click', closeModals);
        });

        // Botão de cancelar no formulário de edição
        const cancelButton = document.querySelector('#edit-form .cancel-button');
        if (cancelButton) {
            cancelButton.addEventListener('click', closeModals);
        }

        // Formulário de edição
        const editForm = document.getElementById('edit-form');
        if (editForm) {
            editForm.addEventListener('submit', submitEditForm);
        }
    }

    function openEditModal(event) {
        const demandaId = event.currentTarget.getAttribute('data-id');
        const modal = document.getElementById('edit-modal');
        const form = document.getElementById('edit-form');

        // Limpa o formulário
        form.reset();

        // Preenche o campo hidden com o ID da demanda
        document.getElementById('edit-demanda-id').value = demandaId;

        // Faz uma requisição para obter os dados da demanda
        fetch(`/demandas/editar/${demandaId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const demanda = data.data;
                    form.titulo_projeto.value = demanda.titulo_projeto;
                    form.status.value = demanda.status;
                    form.nome_solicitante.value = demanda.nome_solicitante;
                    form.categoria.value = demanda.categoria;
                    form.descricao.value = demanda.descricao;
                    form.urgencia.value = demanda.urgencia;
                    form.taxa_urgencia.value = demanda.taxa_urgencia;
                    // Observação: Arquivo adicional não pode ser preenchido por motivos de segurança
                } else {
                    showNotification('error', 'Erro ao carregar os dados da demanda.');
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                showNotification('error', 'Erro ao carregar os dados da demanda.');
            });

        // Exibe o modal
        modal.style.display = 'block';
    }

    function closeModals() {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.style.display = 'none';
        });
    }

    function submitEditForm(event) {
        event.preventDefault();
        const form = event.target;
        const demandaId = form.demanda_id.value;

        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        // Convertendo valores booleanos e numéricos
        data['taxa_urgencia'] = data['taxa_urgencia'] === 'true';
        data['status'] = parseInt(data['status']);
        data['urgencia'] = parseInt(data['urgencia']);

        fetch(`/demandas/editar/${demandaId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                showNotification('success', data.message);
                // Atualiza a demanda na lista sem recarregar a página
                // Implementar a função updateDemandaInList se necessário
                closeModals();
            } else {
                showNotification('error', 'Erro ao atualizar a demanda.');
                console.error(data.message);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            showNotification('error', 'Erro ao atualizar a demanda.');
        });
    }

    function showNotification(type, message) {
        const notification = document.getElementById('notification');
        notification.className = '';
        notification.classList.add(type === 'success' ? 'success' : 'error');
        notification.textContent = message;
        notification.classList.add('show');

        setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
    }

    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, 10) === ('csrftoken=')) {
                    cookieValue = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        return cookieValue;
    }
});


/**
 * Inicializa todos os eventos necessários após o carregamento do DOM.
 */
document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM completamente carregado.");
  
    // Inicializa eventos do formulário de cadastro
    initFormEvents();
  
    // Inicializa eventos da sidebar
    initSidebarEvents();
  
    // Inicializa eventos para botões já presentes no DOM
    initActionButtons();
  
    // Inicializa eventos do formulário de edição
    initEditFormEvent();

    init();
  
    // Inicializa a funcionalidade de seleção
    initSelecionarTodos();
  
    // Inicializa a funcionalidade de exclusão em massa
    initExcluirSelecionados();
  
    // Inicializa a funcionalidade de deletar demandas individuais
    initDeletarDemandas();
  
    // Inicializa a funcionalidade "Ver Mais" para modais de detalhes
    initVerMaisModal();
  
    // Inicializa a funcionalidade de exclusão de membros
    initExcluirMembros();
  });
  