// script.js

// ======================================================
// 1. Funções Utilitárias
// ======================================================

/**
 * Obtém o valor de um cookie pelo nome.
 * @param {string} name - Nome do cookie.
 * @returns {string|null} Valor do cookie ou null se não encontrado.
 */
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Carrega o token CSRF do cookie
const csrftoken = getCookie("csrftoken");

// ======================================================
// 2. Funções de Notificação
// ======================================================

/**
 * Exibe uma notificação na tela.
 * @param {string} message - Mensagem a ser exibida.
 * @param {string} type - Tipo da notificação ('success' ou 'error').
 */
function showNotification(message, type) {
  const notification = document.getElementById("notification");
  if (!notification) return;

  notification.textContent = message;
  notification.className = ""; // Reseta classes anteriores
  notification.classList.add(type); // Adiciona classe de tipo (success/error)
  notification.classList.add("show"); // Mostra a notificação

  // Oculta a notificação após 2 segundos
  setTimeout(() => {
    notification.classList.remove("show");
  }, 2000);
}

// ======================================================
// 3. Funções do Modal de Confirmação
// ======================================================

/**
 * Exibe o modal de confirmação para ações como exclusão.
 * @param {Function} callback - Função a ser executada após a confirmação.
 */
function showConfirmationModal(callback) {
  const modal = document.getElementById("confirmation-modal");
  if (!modal) {
    console.error("Modal de confirmação não encontrado.");
    return;
  }

  const closeButton = modal.querySelector(".close-button");
  const confirmButton = modal.querySelector("#confirm-excluir");
  const cancelButton = modal.querySelector("#cancel-excluir");

  if (!closeButton || !confirmButton || !cancelButton) {
    console.error("Elementos do modal de confirmação não encontrados.");
    return;
  }

  // Exibe o modal
  modal.style.display = "block";

  /**
   * Fecha o modal e remove os event listeners para evitar múltiplas chamadas.
   */
  function closeModal() {
    modal.style.display = "none";
    confirmButton.removeEventListener("click", onConfirm);
    cancelButton.removeEventListener("click", onCancel);
    closeButton.removeEventListener("click", closeModal);
    window.removeEventListener("click", outsideClick);
  }

  /**
   * Função chamada quando o usuário confirma a ação.
   */
  function onConfirm() {
    callback();
    closeModal();
  }

  /**
   * Função chamada quando o usuário cancela a ação.
   */
  function onCancel() {
    closeModal();
  }

  /**
   * Fecha o modal se o usuário clicar fora do conteúdo do modal.
   * @param {Event} event - Evento de clique.
   */
  function outsideClick(event) {
    if (event.target === modal) {
      closeModal();
    }
  }

  // Adiciona event listeners
  confirmButton.addEventListener("click", onConfirm);
  cancelButton.addEventListener("click", onCancel);
  closeButton.addEventListener("click", closeModal);
  window.addEventListener("click", outsideClick);
}

// ======================================================
// 4. Funções de Manipulação de Demandas
// ======================================================



/**
 * Verifica se há demandas no DOM e exibe a mensagem caso contrário.
 */
function verificarDemandas() {
  const demandasRestantes = document.querySelectorAll(".demanda-card");
  const noDemandaMessage = document.getElementById("no-demanda-message");

  if (demandasRestantes.length === 0 && noDemandaMessage) {
    noDemandaMessage.style.display = "block";
  } else if (noDemandaMessage) {
    noDemandaMessage.style.display = "none";
  }
}


/**
 * Exclui uma demanda após a confirmação do usuário.
 * @param {HTMLElement} button - Botão clicado para excluir a demanda.
 */
function excluirDemanda(button) {
  const demandaId = button.getAttribute("data-id");
  if (!demandaId) {
    console.error("ID da demanda não encontrado.");
    return;
  }

  // Mostra o modal de confirmação
  showConfirmationModal(() => {
    // Realiza a requisição para excluir a demanda
    fetch(`/excluir-demanda/${demandaId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          // Remove a demanda da interface com transição suave
          const demandaCard = document.getElementById(`demanda-${demandaId}`);
          if (demandaCard) {
            demandaCard.classList.add("fade-out");
            demandaCard.addEventListener("animationend", () => {
              demandaCard.remove(); // Remove completamente o elemento do DOM
              verificarDemandas(); // Verifica se precisa exibir a mensagem
            });
          }
          showNotification(
            data.message || "Demanda excluída com sucesso!",
            "success"
          );
        } else {
          showNotification(
            data.message || "Erro ao excluir a demanda.",
            "error"
          );
        }
      })
      .catch((error) => {
        console.error("Erro ao excluir a demanda:", error);
        showNotification("Ocorreu um erro ao excluir a demanda.", "error");
      });
  });
}

// Função para obter o CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Verifica se este cookie começa com o nome desejado
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

/**
 * Exibe uma notificação na tela.
 * @param {string} message - Mensagem a ser exibida.
 * @param {string} type - Tipo da notificação ('success' ou 'error').
 */
function showNotification(message, type) {
  const notification = document.getElementById("notification");
  notification.textContent = message;
  notification.className = ""; // Remove classes anteriores
  notification.classList.add(type, "show"); // Adiciona a classe de tipo e 'show'

  // Remove a notificação após 3 segundos
  setTimeout(() => {
    notification.classList.remove("show");
  }, 3000);
}

/**
 * Conclui uma demanda.
 * @param {HTMLElement} button - Botão clicado para concluir a demanda.
 */
function concluirDemanda(button) {
  const demandaId = button.getAttribute("data-id");
  if (!demandaId) {
    console.error("ID da demanda não encontrado.");
    return;
  }

  // Desabilita o botão para evitar múltiplos cliques
  button.disabled = true;

  fetch(`/concluir-demanda/${demandaId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
      "X-Requested-With": "XMLHttpRequest",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({}),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Remove a demanda do DOM com animação de fade-out
        const demandaCard = document.getElementById(`demanda-${demandaId}`);
        if (demandaCard) {
          demandaCard.classList.add("fade-out");
          demandaCard.addEventListener("animationend", () => {
            demandaCard.remove();

            // Verifica se não há mais demandas
            const demandasRestantes =
              document.querySelectorAll(".demanda-card");
            if (demandasRestantes.length === 0) {
              const noDemandaMessage =
                document.getElementById("no-demanda-message");
              if (noDemandaMessage) {
                noDemandaMessage.style.display = "block";
              }
            }
          });
        }

        // Exibe a notificação de sucesso
        showNotification(data.message, "success");
      } else {
        showNotification(data.message || "Erro ao concluir demanda.", "error");
        button.disabled = false; // Reabilita o botão em caso de erro
      }
    })
    .catch((error) => {
      console.error("Erro ao concluir a demanda:", error);
      showNotification("Ocorreu um erro ao concluir a demanda.", "error");
      button.disabled = false; // Reabilita o botão em caso de erro
    });
}

document.addEventListener("DOMContentLoaded", () => {
  // Seleciona todos os botões "Concluir"
  const concluidoButtons = document.querySelectorAll(".concluido-button");

  // Adiciona o event listener para cada botão
  concluidoButtons.forEach((button) => {
    button.addEventListener("click", () => {
      concluirDemanda(button);
    });
  });
});

/**
 * Alterna a visibilidade dos detalhes de uma demanda.
 * @param {HTMLElement} element - Elemento que foi clicado para alternar os detalhes.
 */
function toggleDetails(element) {
  const details = element.nextElementSibling;
  const icon = element.querySelector(".toggle-icon");

  if (!details || !icon) {
    console.error("Elementos de detalhes ou ícone não encontrados.");
    return;
  }

  // Alterna a classe 'open' para mostrar/ocultar os detalhes
  if (details.classList.contains("open")) {
    details.classList.remove("open");
    icon.style.transform = "rotate(0deg)";
  } else {
    details.classList.add("open");
    icon.style.transform = "rotate(180deg)";
  }
}

/**
 * Abre o modal de edição e preenche o formulário com os dados da demanda selecionada.
 * @param {HTMLElement} button - Botão clicado para editar a demanda.
 */
function editDemanda(button) {
  const demandaId = button.getAttribute("data-id");
  if (!demandaId) {
    console.error("ID da demanda não encontrado.");
    return;
  }

  // Buscar os dados atuais da demanda no DOM
  const demandaCard = document.getElementById(`demanda-${demandaId}`);
  if (!demandaCard) {
    console.error("Elemento da demanda não encontrado.");
    return;
  }

  // Extrair os valores dos campos
  const tituloProjeto = demandaCard
    .querySelector(".demanda-titulo")
    .textContent.trim();
  const solicitanteP = demandaCard.querySelector(".demanda-solicitante");
  const categoriaP = demandaCard.querySelector(".demanda-categoria");
  const descricaoP = demandaCard.querySelector(".demanda-descricao");
  const statusP = demandaCard.querySelector(".demanda-status-detail");
  const urgenciaP = demandaCard.querySelector(".demanda-urgencia");

  const nomeSolicitante = solicitanteP
    ? solicitanteP.textContent.replace("Solicitante:", "").trim()
    : "";
  const categoria = categoriaP
    ? categoriaP.textContent.replace("Categoria:", "").trim()
    : "";
  const descricao = descricaoP
    ? descricaoP.textContent.replace("Descrição:", "").trim()
    : "";
  const statusText = statusP
    ? statusP.textContent.replace("Status:", "").trim()
    : "Novo";
  const urgenciaText = urgenciaP
    ? urgenciaP.textContent.replace("Urgência:", "").trim()
    : "Baixa";

  // Mapear os textos para os valores do select
  const statusMap = {
    Novo: "novo",
    "Em Andamento": "em_andamento",
    Concluído: "concluido",
  };

  const urgenciaMap = {
    Baixa: "baixa",
    Média: "media",
    Alta: "alta",
  };

  const statusValue = statusMap[statusText] || "novo";
  const urgenciaValue = urgenciaMap[urgenciaText] || "baixa";

  // Preencher os campos do formulário no modal
  document.getElementById("edit-demanda-id").value = demandaId;
  document.getElementById("edit-titulo_projeto").value = tituloProjeto;
  document.getElementById("edit-nome_solicitante").value = nomeSolicitante;
  document.getElementById("edit-categoria").value = categoria;
  document.getElementById("edit-descricao").value = descricao;
  document.getElementById("edit-status").value = statusValue;
  document.getElementById("edit-urgencia").value = urgenciaValue;

  // Abrir o modal de edição
  const editModal = document.getElementById("edit-modal");
  if (editModal) {
    editModal.classList.add("show"); // Usa a classe 'show' para exibir o modal
    editModal.classList.remove("hidden");
  } else {
    console.error("Elemento com ID 'edit-modal' não encontrado.");
  }

  // Adicionar event listeners para fechar o modal
  const closeButton = editModal.querySelector(".close-button");
  const cancelButton = editModal.querySelector(".btn-cancel");

  // Definir funções separadas para facilitar a remoção dos event listeners
  function handleClose() {
    editModal.classList.remove("show");
    editModal.classList.add("hidden");
    clearEditForm();
    // Remover event listeners após a ação
    closeButton.removeEventListener("click", handleClose);
    cancelButton.removeEventListener("click", handleClose);
    window.removeEventListener("click", handleOutsideClick);
  }

  function handleOutsideClick(event) {
    if (event.target === editModal) {
      handleClose();
    }
  }

  // Adicionar event listeners
  closeButton.addEventListener("click", handleClose);
  cancelButton.addEventListener("click", handleClose);
  window.addEventListener("click", handleOutsideClick);
}

/**
 * Limpa os campos do formulário de edição.
 */
function clearEditForm() {
  const form = document.getElementById("editForm");
  if (form) {
    form.reset();
    document.getElementById("edit-demanda-id").value = "";
    document.getElementById("edit-feedback").innerHTML = "";
  }
}

/**
 * Função para capitalizar textos de status.
 * @param {string} status - Valor técnico do status.
 * @returns {string} Representação amigável do status.
 */
function capitalizeStatus(status) {
  const map = {
    novo: "Novo",
    em_andamento: "Em Andamento",
    concluido: "Concluído",
  };
  return map[status] || status;
}

/**
 * Função para capitalizar textos de urgência.
 * @param {string} urgencia - Valor técnico da urgência.
 * @returns {string} Representação amigável da urgência.
 */
function capitalizeUrgencia(urgencia) {
  const map = {
    baixa: "Baixa",
    media: "Média",
    alta: "Alta",
  };
  return map[urgencia] || urgencia;
}

/**
 * Inicializa os eventos do formulário de edição.
 */
function initEditFormEvent() {
  const editForm = document.getElementById("editForm");
  const feedback = document.getElementById("edit-feedback"); // Exibe mensagens de erro ou sucesso
  const editModal = document.getElementById("editModal");

  if (!editForm) {
    console.error("Elemento com ID 'editForm' não encontrado.");
    return;
  }

  editForm.addEventListener("submit", function (event) {
    event.preventDefault(); // Evita comportamento padrão

    const membroId = document.getElementById("edit-membro-id").value;
    const email = document.getElementById("edit-email").value.trim();
    const nome = document.getElementById("edit-nome").value.trim();
    const telefone = document.getElementById("edit-telefone").value.trim();
    const cargo = document.getElementById("edit-cargo").value.trim();

    if (!membroId || !email || !nome) {
      feedback.textContent = "Email e Nome são obrigatórios.";
      feedback.classList.add("error");
      feedback.classList.remove("success");
      return;
    }

    const formData = new FormData(this); // Coleta os dados do formulário

    fetch(`/editar-membro/${membroId}/`, {
      // Ajuste a URL conforme sua rota
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "X-Requested-With": "XMLHttpRequest",
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Resposta do servidor:", data); // Para depuração
        if (data.success) {
          feedback.textContent = "Membro atualizado com sucesso!";
          feedback.classList.add("success");
          feedback.classList.remove("error");

          // Atualiza os atributos de dados do botão de edição
          const editarButton = document.querySelector(
            `button.btn-editar[data-id="${membroId}"]`
          );
          if (editarButton) {
            editarButton.setAttribute("data-email", email);
            editarButton.setAttribute("data-nome", nome);
            editarButton.setAttribute("data-telefone", telefone);
            editarButton.setAttribute("data-cargo", cargo);
          }

          // Atualiza os campos na tabela
          const membroRow = editarButton.closest("tr");
          if (membroRow) {
            membroRow.querySelector("td:nth-child(2)").textContent = email;
            membroRow.querySelector("td:nth-child(3)").textContent = nome;
            membroRow.querySelector("td:nth-child(4)").textContent =
              telefone || "Pendente";
            membroRow.querySelector("td:nth-child(5)").textContent =
              cargo || "Pendente";
          }

          // Fecha o modal após um pequeno delay para exibir a mensagem de sucesso
          setTimeout(() => {
            editModal.classList.add("hidden");
            editModal.classList.remove("modal-edit");
            feedback.textContent = ""; // Limpa o feedback
          }, 1000); // 1 segundo
        } else {
          feedback.textContent = data.message || "Erro ao atualizar membro.";
          feedback.classList.add("error");
          feedback.classList.remove("success");
        }
      })
      .catch((error) => {
        console.error("Erro ao salvar a edição:", error);
        feedback.textContent = "Erro ao salvar. Tente novamente.";
        feedback.classList.add("error");
        feedback.classList.remove("success");
      });
  });
}

/**
 * Inicializa os eventos do formulário de edição de demandas.
 */
function initEditDemandFormEvent() {
  const editForm = document.getElementById("editForm");
  const feedback = document.getElementById("edit-feedback"); // Exibe mensagens de erro ou sucesso
  const editModal = document.getElementById("edit-modal");

  if (!editForm) {
    console.error("Elemento com ID 'editForm' não encontrado.");
    return;
  }

  editForm.addEventListener("submit", function (event) {
    event.preventDefault(); // Evita comportamento padrão

    const demandaId = document.getElementById("edit-demanda-id").value;
    const tituloProjeto = document
      .getElementById("edit-titulo_projeto")
      .value.trim();
    const nomeSolicitante = document
      .getElementById("edit-nome_solicitante")
      .value.trim();
    const categoria = document.getElementById("edit-categoria").value.trim();
    const descricao = document.getElementById("edit-descricao").value.trim();
    const status = document.getElementById("edit-status").value;
    const urgencia = document.getElementById("edit-urgencia").value;
    const arquivoAdicional = document.getElementById(
      "edit-arquivo_adicional"
    ).files;

    if (
      !demandaId ||
      !tituloProjeto ||
      !nomeSolicitante ||
      !categoria ||
      !descricao
    ) {
      feedback.textContent =
        "Título, Nome do Solicitante, Categoria e Descrição são obrigatórios.";
      feedback.classList.add("error");
      feedback.classList.remove("success");
      return;
    }

    const formData = new FormData(this); // Coleta os dados do formulário

    fetch(`/editar-demanda/${demandaId}/`, {
      // Ajuste a URL conforme sua rota
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "X-Requested-With": "XMLHttpRequest",
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Resposta do servidor:", data); // Para depuração
        if (data.success) {
          feedback.textContent = "Demanda atualizada com sucesso!";
          feedback.classList.add("success");
          feedback.classList.remove("error");

          // Atualiza os atributos de dados do botão de edição
          const editarButton = document.querySelector(
            `button.edit-button[data-id="${demandaId}"]`
          );
          if (editarButton) {
            editarButton.setAttribute("data-titulo_projeto", tituloProjeto);
            editarButton.setAttribute("data-nome_solicitante", nomeSolicitante);
            editarButton.setAttribute("data-categoria", categoria);
            editarButton.setAttribute("data-descricao", descricao);
            editarButton.setAttribute("data-status", status);
            editarButton.setAttribute("data-urgencia", urgencia);
          }

          // Atualiza os campos na demanda card
          const demandaCard = document.getElementById(`demanda-${demandaId}`);
          if (demandaCard) {
            demandaCard.querySelector(".demanda-titulo").textContent =
              tituloProjeto;
            demandaCard.querySelector(
              ".demanda-status"
            ).innerHTML = `<strong><i class="fa-solid fa-spinner"></i></strong> ${data.status_display}`;
            demandaCard.querySelector(
              ".demanda-data"
            ).innerHTML = `<strong><i class="fa-solid fa-calendar-days"></i></strong> ${data.data_criacao}`;

            const detalhes = demandaCard.querySelector(".demanda-details");
            if (detalhes) {
              detalhes.querySelector(
                ".demanda-solicitante"
              ).innerHTML = `<strong>Solicitante:</strong> ${nomeSolicitante}`;
              detalhes.querySelector(
                ".demanda-categoria"
              ).innerHTML = `<strong>Categoria:</strong> ${categoria}`;
              detalhes.querySelector(
                ".demanda-descricao"
              ).innerHTML = `<strong>Descrição:</strong> ${descricao}`;
              detalhes.querySelector(
                ".demanda-status-detail"
              ).innerHTML = `<strong>Status:</strong> ${data.status_display}`;
              detalhes.querySelector(
                ".demanda-urgencia"
              ).innerHTML = `<strong>Urgência:</strong> ${data.urgencia_display}`;
              detalhes.querySelector(
                ".demanda-taxa_urgencia"
              ).innerHTML = `<strong>Taxa de Urgência:</strong> ${data.taxa_urgencia}`;
              detalhes.querySelector(
                ".demanda-criacao"
              ).innerHTML = `<strong>Criado em:</strong> ${data.data_criacao}`;

              if (data.arquivo_adicional_url) {
                detalhes.querySelector(
                  ".demanda-arquivo"
                ).innerHTML = `<strong>Arquivo:</strong> <a href="${data.arquivo_adicional_url}" target="_blank">Baixar Arquivo</a>`;
              } else {
                detalhes.querySelector(
                  ".demanda-arquivo"
                ).innerHTML = `<strong>Arquivo:</strong> Nenhum arquivo enviado`;
              }
            }
          }

          // Fecha o modal após um pequeno delay para exibir a mensagem de sucesso
          setTimeout(() => {
            editModal.classList.add("hidden");
            editModal.classList.remove("show");
            feedback.textContent = ""; // Limpa o feedback
            editForm.reset(); // Reseta o formulário
          }, 1000); // 1 segundo
        } else {
          feedback.textContent = data.message || "Erro ao atualizar demanda.";
          feedback.classList.add("error");
          feedback.classList.remove("success");
        }
      })
      .catch((error) => {
        console.error("Erro ao salvar a edição:", error);
        feedback.textContent = "Erro ao salvar. Tente novamente.";
        feedback.classList.add("error");
        feedback.classList.remove("success");
      });
  });
}

// Inicializa os eventos após o carregamento do DOM
document.addEventListener("DOMContentLoaded", initEditDemandFormEvent);

// ======================================================
// 5. Funções de Inicialização
// ======================================================

/**
 * Inicializa os eventos relacionados ao formulário de demandas.
 */
function initFormEvents() {
  console.log("Inicializando eventos do formulário...");
  const form = document.getElementById("demandaForm");
  const feedback = document.getElementById("feedback");

  if (!form) {
    console.error("Elemento com ID 'demandaForm' não encontrado.");
    return;
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault(); // Impede o comportamento padrão de submissão do formulário
    feedback.innerHTML = ""; // Limpa feedback anterior
    console.log("Evento de envio acionado!");

    const formData = new FormData(this);

    fetch(relatoriosUrl, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(
            "Network response was not ok: " + response.statusText
          );
        }
        return response.json();
      })
      .then((data) => {
        if (data.success) {
          console.log("Formulário enviado com sucesso.");
          showNotification(data.message, "success");
          form.reset(); // Reseta o formulário

          // Exibe o modal de sucesso
          showSuccessMessage();

          // Oculta o modal após 3 segundos
          setTimeout(() => {
            hideSuccessMessage();
          }, 3000);
        } else {
          console.log("Erro ao enviar o formulário.");
          showNotification("Erro ao cadastrar demanda.", "error");
          for (const [campo, mensagens] of Object.entries(data.errors)) {
            mensagens.forEach((mensagem) => {
              feedback.innerHTML += `<p style="color: red;">${campo}: ${mensagem}</p>`;
            });
          }
        }
      })
      .catch((error) => {
        console.error("Erro na requisição:", error);
        showNotification("Ocorreu um erro ao enviar o formulário.", "error");
        setTimeout(() => {
          feedback.innerHTML = "";
        }, 3000);
      });
  });
}

/**
 * Inicializa os eventos relacionados à sidebar para navegação via AJAX.
 */
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
          initEditDemandFormEvent(); // Reaplica a funcionalidade de edição de demandas
          verificarDemandas(); // Verifica se há demandas restantes
          initModalDemandas(); // Reaplica a funcionalidade do modal de demandas
        })
        .catch((error) => console.error("Erro ao carregar a aba:", error));
    });
  });
}

/**
 * Inicializa os eventos para os botões de ação (Excluir, Concluir, Editar, Toggle).
 */
function initActionButtons() {
  // Botões de Excluir
  const excluirButtons = document.querySelectorAll("button.delete-button");
  excluirButtons.forEach((button) => {
    button.addEventListener("click", function () {
      excluirDemanda(this);
    });
  });

  // Botões de Concluir
  const concluirButtons = document.querySelectorAll("button.concluido-button");
  concluirButtons.forEach((button) => {
    button.addEventListener("click", function () {
      concluirDemanda(this);
    });
  });

  // Botões de Editar
  const editarButtons = document.querySelectorAll("button.btn-editar");
  editarButtons.forEach((button) => {
    button.addEventListener("click", function () {
      editarMembro(this);
    });
  });

  const editarDemandas = document.querySelectorAll("button.edit-button");
  editarDemandas.forEach((button) => {
    button.addEventListener("click", function () {
      editDemanda(this);
    });
  });

  // Botões de Toggle de Detalhes
  const toggleButtons = document.querySelectorAll(".demanda-summary");
  toggleButtons.forEach((button) => {
    button.addEventListener("click", function () {
      toggleDetails(this);
    });
  });
}

// ======================================================
// 6. Funções do Modal de Sucesso
// ======================================================

/**
 * Exibe o modal de sucesso.
 */
function showSuccessMessage() {
  const modal = document.getElementById("success-message");
  if (modal) {
    modal.classList.add("show"); // Adiciona a classe 'show' para exibir o modal
    modal.classList.remove("hidden"); // Remove a classe 'hidden' caso exista
  } else {
    console.error("Elemento com ID 'success-message' não encontrado.");
  }
}

/**
 * Oculta o modal de sucesso.
 */
function hideSuccessMessage() {
  const modal = document.getElementById("success-message");
  if (modal) {
    modal.classList.remove("show"); // Remove a classe 'show' para ocultar o modal
    modal.classList.add("hidden"); // Adiciona a classe 'hidden'
  }
}

// ======================================================
// 7. Funções do Modal "Ver Mais"
// ======================================================

/**
 * Inicializa o evento de abrir modal ao clicar em "Ver Mais".
 */
function initVerMaisModal() {
  const modal = document.getElementById("detalhesModal");
  if (!modal) {
    console.error("Elemento com ID 'detalhesModal' não encontrado.");
    return;
  }

  const closeModal = modal.querySelector(".close-modal");
  const detalhesTitulo = document.getElementById("detalhes-titulo");
  const detalhesStatus = document.getElementById("detalhes-status");
  const detalhesUrgencia = document.getElementById("detalhes-urgencia");
  const detalhesData = document.getElementById("detalhes-data");
  const detalhesDescricao = document.getElementById("detalhes-descricao");

  // Adiciona evento aos botões "Ver Mais"
  document.querySelectorAll(".ver-mais").forEach((button) => {
    button.addEventListener("click", function () {
      const demandaId = this.getAttribute("data-id");

      // Faz a requisição para obter os detalhes
      fetch(`/detalhes-demanda/${demandaId}/`, {
        headers: { "X-Requested-With": "XMLHttpRequest" },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            detalhesTitulo.innerHTML = `<i class="fa-solid fa-file-alt icon"></i> Título: ${data.titulo}`;
            detalhesStatus.innerHTML = `<i class="fa-solid fa-info-circle icon"></i> Status: ${data.status}`;
            detalhesUrgencia.innerHTML = `<i class="fa-solid fa-exclamation-triangle icon"></i> Urgência: ${data.urgencia}`;
            detalhesData.innerHTML = `<i class="fa-solid fa-calendar-alt icon"></i> Data: ${data.data}`;
            detalhesDescricao.innerHTML = `<i class="fa-solid fa-align-left icon"></i> Descrição: ${data.descricao}`;
            modal.style.display = "flex";
          } else {
            console.error("Erro ao buscar detalhes da demanda.");
            showNotification("Erro ao buscar detalhes da demanda.", "error");
          }
        })
        .catch((error) => console.error("Erro na requisição:", error));
    });
  });

  // Fecha o modal
  closeModal.addEventListener("click", () => {
    modal.style.display = "none";
  });

  // Fecha o modal ao clicar fora do conteúdo
  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });
}

// ======================================================
// 8. Funções para Exclusão em Massa
// ======================================================

/**
 * Inicializa exclusão em massa de demandas.
 */
function initExcluirSelecionados() {
  const excluirBtn = document.getElementById("excluirSelecionados");
  const checkboxes = document.querySelectorAll(".demanda-checkbox");
  const massaModal = document.getElementById("confirmacaoMassaModal");
  const confirmarBtnMassa = document.getElementById("confirmarExclusaoMassa");
  const cancelarBtnMassa = document.getElementById("cancelarExclusaoMassa");

  if (!excluirBtn || !massaModal || !confirmarBtnMassa || !cancelarBtnMassa) {
    console.error("Elementos para exclusão em massa não encontrados.");
    return;
  }

  // Ativa/desativa o botão de exclusão em massa com base nos checkboxes selecionados
  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", () => {
      const selected = Array.from(checkboxes).some((cb) => cb.checked);
      excluirBtn.disabled = !selected;
    });
  });

  // Exibe o modal de confirmação
  excluirBtn.addEventListener("click", () => {
    massaModal.style.display = "flex";
  });

  // Confirma exclusão em massa
  confirmarBtnMassa.addEventListener("click", () => {
    const idsParaExcluir = Array.from(checkboxes)
      .filter((cb) => cb.checked)
      .map((cb) => cb.getAttribute("data-id"));

    if (idsParaExcluir.length === 0) return;

    // Faz a requisição para deletar demandas em massa
    fetch(`/deletar-massa-demanda/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
      body: JSON.stringify({ ids: idsParaExcluir }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          // Remove demandas excluídas da interface com animação de fade-out
          idsParaExcluir.forEach((id) => {
            const demandaRow = document.getElementById(`demanda-${id}`);
            if (demandaRow) {
              demandaRow.classList.add("fade-out");
              demandaRow.addEventListener("animationend", () => {
                demandaRow.remove();
              });
            }
          });
          showNotification(
            data.message || "Demandas excluídas com sucesso.",
            "success"
          );
          excluirBtn.disabled = true; // Desativa o botão após exclusão
          verificarDemandas(); // Verifica se a mensagem deve ser exibida
        } else {
          showNotification(
            data.message || "Demandas excluídas com sucesso.",
            "success"
          );
        }
      })
      .catch((error) => {
        console.error("Erro na requisição de exclusão em massa:", error);
        showNotification("Erro ao excluir demandas em massa.", "error");
      })
      .finally(() => {
        massaModal.style.display = "none"; // Fecha o modal
      });
  });

  // Cancela exclusão em massa
  cancelarBtnMassa.addEventListener("click", () => {
    massaModal.style.display = "none"; // Fecha o modal
  });

  // Fecha o modal ao clicar fora do conteúdo
  window.addEventListener("click", (event) => {
    if (event.target === massaModal) {
      massaModal.style.display = "none"; // Fecha o modal
    }
  });
}

// ======================================================
// 9. Funções para Selecionar Todos os Checkboxes
// ======================================================

/**
 * Inicializa a funcionalidade de seleção de todos os checkboxes.
 */
function initSelecionarTodos() {
  const selecionarTodos = document.getElementById("selecionarTodos");
  const checkboxes = document.querySelectorAll(".demanda-checkbox");
  const excluirBtn = document.getElementById("excluirSelecionados");

  if (!selecionarTodos || !excluirBtn) {
    console.error("Elementos para selecionar todos não encontrados.");
    return;
  }

  // Marca ou desmarca todos os checkboxes
  selecionarTodos.addEventListener("change", () => {
    const isChecked = selecionarTodos.checked;
    checkboxes.forEach((checkbox) => {
      checkbox.checked = isChecked;
    });

    // Ativa ou desativa o botão de exclusão
    excluirBtn.disabled = !isChecked;
  });

  // Verifica se todos os checkboxes estão marcados ou não
  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", () => {
      const allChecked = Array.from(checkboxes).every((cb) => cb.checked);
      const anyChecked = Array.from(checkboxes).some((cb) => cb.checked);

      selecionarTodos.checked = allChecked; // Atualiza o estado do "Selecionar Todos"
      excluirBtn.disabled = !anyChecked; // Ativa ou desativa o botão de exclusão
    });
  });
}

// ======================================================
// 10. Funções para Deletar Demandas Individuais com Confirmação
// ======================================================

/**
 * Inicializa exclusão individual de demandas com confirmação.
 */
/**
 * Inicializa os eventos para os botões de exclusão de demandas.
 */
function initDeletarDemandas() {
  const deleteButtons = document.querySelectorAll(".deletar");

  deleteButtons.forEach((button) => {
    button.addEventListener("click", function () {
      excluirDemanda(this);
    });
  });
}

function initDeletarDemandas() {
  const modal = document.getElementById("confirmacaoModal");
  if (!modal) {
    console.error("Elemento com ID 'confirmacaoModal' não encontrado.");
    return;
  }

  const confirmarBtn = document.getElementById("confirmarExclusao");
  const cancelarBtn = document.getElementById("cancelarExclusao");
  let demandaIdParaExcluir = null;

  if (!confirmarBtn || !cancelarBtn) {
    console.error("Botões de confirmação/cancelamento não encontrados.");
    return;
  }

  document.querySelectorAll(".deletar").forEach((button) => {
    button.addEventListener("click", function () {
      demandaIdParaExcluir = this.getAttribute("data-id");
      if (!demandaIdParaExcluir) {
        console.error("ID da demanda para exclusão não encontrado.");
        return;
      }
      modal.style.display = "flex"; // Exibe o modal
    });
  });

  confirmarBtn.addEventListener("click", () => {
    if (!demandaIdParaExcluir) return;

    fetch(`/deletar-demanda/${demandaIdParaExcluir}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          const demandaRow = document.getElementById(
            `demanda-${demandaIdParaExcluir}`
          );
          if (demandaRow) {
            demandaRow.style.transition = "opacity 0.5s ease-out";
            demandaRow.style.opacity = "0";
            setTimeout(() => {
              demandaRow.style.display = "none";
            }, 500);
          }
          showNotification(data.message, "success");
        } else {
          showNotification(data.message, "error");
        }
      })
      .catch((error) => {
        console.error("Erro na exclusão:", error);
        showNotification("Ocorreu um erro ao excluir a demanda.", "error");
      })
      .finally(() => {
        demandaIdParaExcluir = null;
        modal.style.display = "none"; // Fecha o modal
      });
  });

  cancelarBtn.addEventListener("click", () => {
    demandaIdParaExcluir = null;
    modal.style.display = "none"; // Fecha o modal
  });

  // Fecha o modal ao clicar fora do conteúdo
  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      demandaIdParaExcluir = null;
      modal.style.display = "none"; // Fecha o modal
    }
  });
}

// ======================================================
// 11. Excluir membro equipe
// ======================================================

/**
 * Inicializa exclusão de membros utilizando o modal de confirmação personalizado.
 */
function initExcluirMembros() {
  const deleteButtons = document.querySelectorAll(".btn-deletar");

  deleteButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const membroId = this.getAttribute("data-id"); // Obtém o ID do membro do atributo data-id
      if (membroId) {
        excluirMembro(membroId); // Chama a função de exclusão com o ID do membro
      } else {
        console.error("ID do membro não encontrado.");
      }
    });
  });
}

// Função para excluir um membro usando o modal de confirmação personalizado
function excluirMembro(membroId) {
  const modal = document.getElementById("confirmacaoModalEquipe");
  const aceitarBtn = document.getElementById("aceitarExclusao");
  const negarBtn = document.getElementById("negarExclusao");

  if (!modal || !aceitarBtn || !negarBtn) {
    console.error("Elementos do modal de confirmação não encontrados.");
    return;
  }

  // Exibe o modal
  modal.classList.remove("hidden");
  modal.classList.add("modall");

  // Função para fechar o modal
  function fecharModal() {
    modal.classList.add("hidden");
    modal.classList.remove("modall");
    // Remove os event listeners após a ação para evitar múltiplas chamadas
    aceitarBtn.removeEventListener("click", onConfirm);
    negarBtn.removeEventListener("click", fecharModal);
    window.removeEventListener("click", foraDoModal);
  }

  // Função chamada quando o usuário confirma a exclusão
  function onConfirm() {
    fetch(`/excluir-membro/${membroId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((data) => {
            throw new Error(data.error || "Erro desconhecido.");
          });
        }
        return response.json();
      })
      .then((data) => {
        if (data.success) {
          // Remove o membro da interface, por exemplo, removendo o elemento da DOM
          const membroElement = document.getElementById(`membro-${membroId}`);
          if (membroElement) {
            membroElement.style.transition = "opacity 0.5s ease-out";
            membroElement.style.opacity = "0";
            setTimeout(() => {
              membroElement.style.display = "none";
            }, 500);
          }
          showNotification(
            data.message || "Membro excluído com sucesso!",
            "success"
          );
        } else {
          showNotification(
            data.message || "Erro ao excluir o membro.",
            "error"
          );
        }
      })
      .catch((error) => {
        console.error("Erro na exclusão:", error);
        showNotification(
          error.message || "Ocorreu um erro ao excluir o membro.",
          "error"
        );
      })
      .finally(() => {
        fecharModal();
      });
  }

  // Função para fechar o modal ao clicar fora do conteúdo
  function foraDoModal(event) {
    if (event.target === modal) {
      fecharModal();
    }
  }

  // Adiciona os event listeners
  aceitarBtn.addEventListener("click", onConfirm);
  negarBtn.addEventListener("click", fecharModal);
  window.addEventListener("click", foraDoModal);
}

/**
 * Abre o modal de edição e preenche o formulário com os dados do membro selecionado.
 * @param {HTMLElement} button - Botão clicado para editar o membro.
 */
function editarMembro(button) {
  // Obtém os dados do membro a partir dos atributos de dados do botão
  const membroId = button.getAttribute("data-id");
  const email = button.getAttribute("data-email");
  const nome = button.getAttribute("data-nome");
  const telefone = button.getAttribute("data-telefone") || "";
  const cargo = button.getAttribute("data-cargo") || "";

  // Preenche os campos do formulário no modal de edição
  document.getElementById("edit-membro-id").value = membroId;
  document.getElementById("edit-email").value = email;
  document.getElementById("edit-nome").value = nome;
  document.getElementById("edit-telefone").value = telefone;
  document.getElementById("edit-cargo").value = cargo;

  // Exibe o modal de edição
  const editModal = document.getElementById("editModal");
  if (editModal) {
    editModal.classList.remove("hidden");
    editModal.classList.add("modal-edit");
  } else {
    console.error("Elemento com ID 'editModal' não encontrado.");
  }

  // Adicionar event listeners para fechar o modal
  const cancelButton = editModal.querySelector(".modal-edit-cancel-button");
  const closeButton = editModal.querySelector(".close-edit-modal");

  function fecharModal() {
    editModal.classList.add("hidden");
    editModal.classList.remove("modal-edit");
    // Remove os event listeners após fechar
    cancelButton.removeEventListener("click", fecharModal);
    closeButton.removeEventListener("click", fecharModal);
    window.removeEventListener("click", foraDoModal);
    // Limpa o formulário
    clearEditForm();
  }

  function foraDoModal(event) {
    if (event.target === editModal) {
      fecharModal();
    }
  }

  // Adiciona os event listeners
  cancelButton.addEventListener("click", fecharModal);
  if (closeButton) {
    closeButton.addEventListener("click", fecharModal);
  }
  window.addEventListener("click", foraDoModal);
}

// ======================================================
// 12. Editar demandas do configuracoes.html
// ======================================================

/**
 * Abre o modal de edição e preenche o formulário com os dados da demanda selecionada.
 * @param {HTMLElement} button - Botão clicado para editar a demanda.
 */
function editarDemanda(button) {
  const demandaId = button.getAttribute("data-id");
  const tituloProjeto = button.getAttribute("data-titulo_projeto");
  const nomeSolicitante = button.getAttribute("data-nome_solicitante");
  const categoria = button.getAttribute("data-categoria");
  const descricao = button.getAttribute("data-descricao");
  const status = button.getAttribute("data-status");
  const urgencia = button.getAttribute("data-urgencia");

  // Preencher os campos do formulário no modal de edição
  document.getElementById("edit-demanda-id").value = demandaId;
  document.getElementById("edit-titulo_projeto").value = tituloProjeto;
  document.getElementById("edit-nome_solicitante").value = nomeSolicitante;
  document.getElementById("edit-categoria").value = categoria;
  document.getElementById("edit-descricao").value = descricao;
  document.getElementById("edit-status").value = status;
  document.getElementById("edit-urgencia").value = urgencia;

  // Exibir o modal de edição
  const editModal = document.getElementById("edit-modal");
  if (editModal) {
    editModal.classList.remove("hidden");
    editModal.classList.add("show");
  } else {
    console.error("Elemento com ID 'edit-modal' não encontrado.");
  }
}

// ======================================================
// 12. Inicialização dos Eventos
// ======================================================

/**
 * Inicializa todos os eventos necessários após o carregamento do DOM.
 */
document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM completamente carregado.");

  // Inicializa eventos do formulário de cadastro
  initFormEvents();

  // Inicializa eventos da sidebar
  initSidebarEvents();

  // Inicializa eventos dos botões de ação
  verificarDemandas();

  // Inicializa eventos para botões já presentes no DOM
  initActionButtons();

  // Inicializa eventos do formulário de edição
  initEditFormEvent();

  initEditDemandFormEvent();

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

  initModalDemandas();
});


// ======================================================
// Função para inicializar o modal de demandas
// ======================================================



function initModalDemandas() {
  console.log("Inicializando modal de demandas...");

  // Criação dinâmica do overlay e adição ao body
  const demandaOverlay = document.createElement("div");
  demandaOverlay.style.position = "fixed";
  demandaOverlay.style.top = "0";
  demandaOverlay.style.left = "0";
  demandaOverlay.style.width = "100%";
  demandaOverlay.style.height = "100%";
  demandaOverlay.style.backgroundColor = "rgba(0, 0, 0, 0.3)"; // Fundo menos escuro
  demandaOverlay.style.zIndex = "999"; // Atrás do modal
  demandaOverlay.style.display = "none"; // Oculto por padrão
  document.body.appendChild(demandaOverlay);

  // Seleção do modal e seus elementos internos
  const demandaModal = document.getElementById("demandaModal");
  const modalContent = demandaModal.querySelector(".modal-demandas-content");
  const modalTitulo = document.getElementById("demanda-modal-titulo");
  const modalDescricao = document.getElementById("demanda-modal-descricao");
  const modalStatus = document.getElementById("demanda-modal-status");
  const modalUrgencia = document.getElementById("demanda-modal-urgencia");
  const modalData = document.getElementById("demanda-modal-data");
  const modalSolicitante = document.getElementById("demanda-modal-solicitante");

  const closeButton = document.querySelector(".close-demandas-button");

  // Estilização inicial do modal para animação
  modalContent.style.opacity = "0";
  modalContent.style.transform = "scale(0.9)";
  modalContent.style.transition = "opacity 0.3s ease, transform 0.3s ease";

  // Abrir modal ao clicar no título da demanda
  document.querySelectorAll(".abrir-modal").forEach((item) => {
    item.addEventListener("click", (event) => {
      event.preventDefault();

      // Obter os dados da demanda
      const demanda = event.target.closest(".demanda");
      if (demanda) {
        modalTitulo.textContent = demanda.getAttribute("data-titulo");
        modalDescricao.textContent = demanda.getAttribute("data-descricao");
        modalStatus.textContent = demanda.getAttribute("data-status");
        modalUrgencia.textContent = demanda.getAttribute("data-urgencia");
        modalData.textContent = demanda.getAttribute("data-data");
        modalSolicitante.textContent = demanda.getAttribute("data-solicitante");

        // Exibir o fundo escuro imediatamente
        demandaOverlay.style.display = "block";

        // Exibir o modal
        demandaModal.style.display = "block";

        // Aplicar o efeito suave ao modal-content
        setTimeout(() => {
          modalContent.style.opacity = "1";
          modalContent.style.transform = "scale(1)";
        }, 10); // Pequeno atraso para ativar a transição
      }
    });
  });

  // Fechar o modal
  const fecharModal = () => {
    // Ocultar o modal-content com animação
    modalContent.style.opacity = "0";
    modalContent.style.transform = "scale(0.9)";

    // Após a transição, esconder o modal e o fundo escuro
    setTimeout(() => {
      demandaModal.style.display = "none";
      demandaOverlay.style.display = "none";
    }, 300); // Tempo da transição
  };

  closeButton.addEventListener("click", fecharModal);

  // Fechar o modal ao clicar no fundo (overlay)
  demandaOverlay.addEventListener("click", fecharModal);

  // Fechar o modal ao clicar fora do modal-content
  window.addEventListener("click", (event) => {
    if (event.target === demandaModal && !modalContent.contains(event.target)) {
      fecharModal();
    }
  });
}

// ======================================================


