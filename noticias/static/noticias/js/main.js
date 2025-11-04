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
            // (Isso diz aos leitores de tela se o menu está aberto ou fechado)
            const isExpanded = mainNav.classList.contains('is-active');
            navToggle.setAttribute('aria-expanded', isExpanded);
        });
    }

    // Você pode adicionar mais interatividade aqui no futuro
    // (Ex: Controles de acessibilidade A+/A-)

});