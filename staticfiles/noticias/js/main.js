/* noticias/static/noticias/js/main.js */

// Este evento garante que o código só rode depois que o HTML da página for completamente carregado.
document.addEventListener('DOMContentLoaded', () => {
    
    console.log("Módulo JavaScript principal carregado.");

    // --- LÓGICA DO MENU MOBILE (HAMBÚRGUER) ---
    
    // 1. Encontra os elementos no HTML
    const menuToggle = document.querySelector('.menu-toggle'); // O botão hambúrguer
    const mainNav = document.querySelector('#main-nav');   // A navegação principal

    // 2. Verifica se os elementos existem na página
    if (menuToggle && mainNav) {
        
        // 3. Adiciona um "ouvinte" de clique ao botão
        menuToggle.addEventListener('click', () => {
            
            // 4. Adiciona ou remove a classe 'is-active' da navegação
            mainNav.classList.toggle('is-active');
            
            // 5. Atualiza o atributo 'aria-expanded' para acessibilidade
            const isExpanded = mainNav.classList.contains('is-active');
            menuToggle.setAttribute('aria-expanded', isExpanded);
        });
    }

    // --- NOVA LÓGICA DE ACESSIBILIDADE ---
    
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

}); 