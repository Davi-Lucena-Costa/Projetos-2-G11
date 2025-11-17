/* noticias/static/noticias/js/main.js */

// Este evento garante que o código só rode depois que o HTML da página for completamente carregado.
document.addEventListener('DOMContentLoaded', () => {
    
    console.log("Módulo JavaScript principal carregado.");

    // --- LÓGICA DO MENU MOBILE (HAMBÚRGUER) ---
    
    // 1. Encontra os elementos no HTML
    const navToggle = document.querySelector('.nav-toggle'); // O botão hambúrguer
    const mainNav = document.querySelector('#main-nav');   // A navegação principal

    // 2. Verifica se os elementos existem na página
    if (navToggle && mainNav) {
        
        // 3. Adiciona um "ouvinte" de clique ao botão
        navToggle.addEventListener('click', () => {
            
            // 4. Adiciona ou remove a classe 'is-active' da navegação
            mainNav.classList.toggle('is-active');
            
            // 5. Atualiza o atributo 'aria-expanded' para acessibilidade
            const isExpanded = mainNav.classList.contains('is-active');
            navToggle.setAttribute('aria-expanded', isExpanded);
        });
    }

    // --- LÓGICA DE ACESSIBILIDADE (GLOBAL) ---
    
    console.log("Carregando controles de acessibilidade...");
    
    // 1. Encontra os botões de controle
    const btnAltoContraste = document.getElementById('alto-contraste');
    const btnAumentarFonte = document.getElementById('aumentar-fonte');
    const btnDiminuirFonte = document.getElementById('diminuir-fonte');
    
    // 2. Lógica do Alto Contraste
    if (btnAltoContraste) {
        btnAltoContraste.addEventListener('click', () => {
            // Adiciona ou remove a classe 'alto-contraste' do <body>
            document.body.classList.toggle('alto-contraste');
            console.log("Modo de alto contraste alternado.");
        });
    }

    // 3. Lógica para Aumentar Fonte
    if (btnAumentarFonte) {
        btnAumentarFonte.addEventListener('click', () => {
            // Pega o 'html' (elemento raiz)
            const root = document.documentElement; 
            // Pega o tamanho da fonte atual
            let fontSize = parseFloat(window.getComputedStyle(root).fontSize);
            // Aumenta em 1px (com um limite de 24px)
            if (fontSize < 24) {
                root.style.fontSize = (fontSize + 1) + 'px';
            }
        });
    }

    // 4. Lógica para Diminuir Fonte
    if (btnDiminuirFonte) {
        btnDiminuirFonte.addEventListener('click', () => {
            const root = document.documentElement;
            let fontSize = parseFloat(window.getComputedStyle(root).fontSize);
            // Diminui em 1px (com um limite de 12px)
            if (fontSize > 12) {
                root.style.fontSize = (fontSize - 1) + 'px';
            }
        });
    }

    // --- NOVA LÓGICA DO MODO LEITURA (APENAS PÁGINA DO ARTIGO) ---

    // 1. Encontra o botão (ele só existe no detalhe.html)
    const btnModoLeitura = document.getElementById('btn-modo-leitura');

    // 2. Se o botão existir nesta página, adiciona o "ouvinte"
    if (btnModoLeitura) {
        console.log("Modo Leitura disponível nesta página.");

        btnModoLeitura.addEventListener('click', () => {
            // 3. Adiciona ou remove a classe principal no <body>
            document.body.classList.toggle('modo-leitura-ativo');

            // 4. Verifica se o modo está ativo
            const isAtivo = document.body.classList.contains('modo-leitura-ativo');

            // 5. Atualiza o texto e o estado do botão
            if (isAtivo) {
                btnModoLeitura.textContent = 'Sair do Modo Leitura';
                btnModoLeitura.setAttribute('aria-pressed', 'true');
            } else {
                btnModoLeitura.textContent = '📖 Modo Leitura';
                btnModoLeitura.setAttribute('aria-pressed', 'false');
            }
        });
    }

}); // FIM do 'DOMContentLoaded'