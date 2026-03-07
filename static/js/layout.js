// static/js/layout.js

// Funcao para plotar grafico de pizza
(() => {
    const barrasPercentuais = document.querySelectorAll('.barra-percentual');
    barrasPercentuais.forEach(barra => {
        const percentual = parseFloat(barra.getAttribute('data-percentual'));
        barra.style.width = `${percentual}%`;
    });
})();

document.getElementById('btn-todas').addEventListener('click', () => {
    const btnTodas = document.getElementById('btn-todas');
    const btnReceita = document.getElementById('btn-receita');
    const btnDespesa = document.getElementById('btn-despesa');
    
    btnTodas.classList.remove('bg-secondary');
    btnTodas.classList.add('bg-dark');
    btnReceita.classList.remove('bg-dark');
    btnReceita.classList.add('bg-secondary')
    btnDespesa.classList.remove('bg-dark');
    btnDespesa.classList.add('bg-secondary');
    
    const categorias = document.querySelectorAll('.categoria');
    categorias.forEach(categoria => {
        categoria.style.display = 'block';
    });
});

document.getElementById('btn-receita').addEventListener('click', () => {
    const btnTodas = document.getElementById('btn-todas');
    const btnReceita = document.getElementById('btn-receita');
    const btnDespesa = document.getElementById('btn-despesa');
    
    btnTodas.classList.remove('bg-dark');
    btnTodas.classList.add('bg-secondary');
    btnReceita.classList.remove('bg-secondary');
    btnReceita.classList.add('bg-dark');
    btnDespesa.classList.remove('bg-dark');
    btnDespesa.classList.add('bg-secondary');
    
    const categorias = document.querySelectorAll('.categoria');
    categorias.forEach(categoria => {
         categoria.style.display =
            categoria.dataset.tipo === 'receita' ? 'block' : 'none';
    });
});

document.getElementById('btn-despesa').addEventListener('click', () => {
    const btnTodas = document.getElementById('btn-todas');
    const btnReceita = document.getElementById('btn-receita');
    const btnDespesa = document.getElementById('btn-despesa');
    
    btnTodas.classList.remove('bg-dark');
    btnTodas.classList.add('bg-secondary');
    btnReceita.classList.remove('bg-dark');
    btnReceita.classList.add('bg-secondary');
    btnDespesa.classList.remove('bg-secondary');
    btnDespesa.classList.add('bg-dark');
    
    const categorias = document.querySelectorAll('.categoria');
    categorias.forEach(categoria => {
         categoria.style.display =
            categoria.dataset.tipo === 'despesa' ? 'block' : 'none';
    });
});