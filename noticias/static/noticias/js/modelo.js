// noticias/static/noticias/js/main.js

// Este evento garante que o código só rode depois que o HTML da página for completamente carregado.
document.addEventListener('DOMContentLoaded', () => {
    
    console.log("Módulo JavaScript principal carregado.");

    // No futuro, você pode adicionar interatividade aqui.
    const cards = document.querySelectorAll('.noticia-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
        });
    });

});