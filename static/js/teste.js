
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
      initModalDemandas();
  
    });
    
  
  
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
              initModalDemandas(); // Reaplica a funcionalidade do modal de demandas
              initExcluirMembros(); // Reaplica a funcionalidade de exclusão de membros
              initEditDemandFormEvent(); // Reaplica a funcionalidade de edição de demandas
              verificarDemandas(); // Verifica se há demandas restantes
            })
            .catch((error) => console.error("Erro ao carregar a aba:", error));
        });
      });
    }