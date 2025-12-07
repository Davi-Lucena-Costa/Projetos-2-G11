/* noticias/static/noticias/js/main.js */

// Este evento garante que o código só rode depois que o HTML da página for completamente carregado.
document.addEventListener('DOMContentLoaded', () => {
    
    console.log("Módulo JavaScript principal carregado.");

    // --- RESTAURAR PREFERÊNCIAS DE ACESSIBILIDADE DO LOCALSTORAGE ---
    
    // Restaurar modo alto-contraste
    const savedContrast = localStorage.getItem('alto-contraste');
    if (savedContrast === 'true') {
        document.body.classList.add('alto-contraste');
    }
    
    // Restaurar tamanho de fonte
    const savedFontSize = localStorage.getItem('font-size');
    if (savedFontSize) {
        document.documentElement.style.fontSize = savedFontSize;
    }

    // --- LÓGICA DO MENU LATERAL (BOTÃO HAMBÚRGUER) ---
    const menuToggle = document.querySelector('.menu-toggle');
    const sideMenu = document.querySelector('#side-menu');
    const menuOverlay = document.querySelector('#menu-overlay');
    const sideMenuClose = document.querySelector('.side-menu-close');

    console.log('menuToggle:', menuToggle);
    console.log('sideMenu:', sideMenu);
    console.log('menuOverlay:', menuOverlay);

    const closeSideMenu = () => {
        sideMenu?.classList.remove('is-active');
        menuOverlay?.classList.remove('is-active');
        if (menuToggle) menuToggle.setAttribute('aria-expanded', 'false');
        if (sideMenu) sideMenu.setAttribute('aria-hidden', 'true');
        if (menuOverlay) menuOverlay.setAttribute('aria-hidden', 'true');
    };

    const openSideMenu = () => {
        sideMenu?.classList.add('is-active');
        menuOverlay?.classList.add('is-active');
        if (menuToggle) menuToggle.setAttribute('aria-expanded', 'true');
        if (sideMenu) sideMenu.setAttribute('aria-hidden', 'false');
        if (menuOverlay) menuOverlay.setAttribute('aria-hidden', 'false');
    };

    if (menuToggle && sideMenu && menuOverlay) {
        console.log('Adicionando event listener ao menu-toggle');
        
        menuToggle.addEventListener('click', () => {
            const willOpen = !sideMenu.classList.contains('is-active');
            if (willOpen) {
                openSideMenu();
            } else {
                closeSideMenu();
            }
        });

        menuOverlay.addEventListener('click', closeSideMenu);

        if (sideMenuClose) {
            sideMenuClose.addEventListener('click', closeSideMenu);
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeSideMenu();
            }
        });
    } else {
        console.log('Erro: menu lateral ou overlay não encontrados');
    }

    // --- LÓGICA DO BOTÃO DE EDIÇÃO DO DIA ---
    
    const brandBadge = document.querySelector('.brand-badge');
    if (brandBadge) {
        brandBadge.addEventListener('click', () => {
            const url = brandBadge.getAttribute('data-url');
            if (url) {
                window.location.href = url;
            }
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
            // Salvar no localStorage
            const isActive = document.body.classList.contains('alto-contraste');
            localStorage.setItem('alto-contraste', isActive ? 'true' : 'false');
            console.log("Modo de alto contraste alternado. Preferência salva.");
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
                const newSize = (fontSize + 1) + 'px';
                root.style.fontSize = newSize;
                // Salvar no localStorage
                localStorage.setItem('font-size', newSize);
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
                const newSize = (fontSize - 1) + 'px';
                root.style.fontSize = newSize;
                // Salvar no localStorage
                localStorage.setItem('font-size', newSize);
            }
        });
    }

}); 