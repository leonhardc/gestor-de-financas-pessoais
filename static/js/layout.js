// static/js/layout.js

// Funcao para plotar grafico de pizza
(() => {
    const barrasPercentuais = document.querySelectorAll('.barra-percentual');
    
    barrasPercentuais.forEach(barra => {
        const percentual = parseFloat(barra.getAttribute('data-percentual'));
        barra.style.width = `${percentual}%`;
    });
})();