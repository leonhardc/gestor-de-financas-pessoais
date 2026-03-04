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
    
    btnTodas.classList.add('bg-primary', 'text-white');
    btnReceita.classList.remove('bg-primary', 'text-white');
    btnDespesa.classList.remove('bg-primary', 'text-white');
    btnTodas.classList.add('bg-primary', 'text-white');
    const categorias = document.querySelectorAll('.categoria');
    categorias.forEach(categoria => {
        categoria.style.display = 'block';
    });
});

document.getElementById('btn-receita').addEventListener('click', () => {
    const btnTodas = document.getElementById('btn-todas');
    const btnReceita = document.getElementById('btn-receita');
    const btnDespesa = document.getElementById('btn-despesa');
    
    btnTodas.classList.remove('bg-primary', 'text-white');
    btnReceita.classList.add('bg-primary', 'text-white');
    btnDespesa.classList.remove('bg-primary', 'text-white');
    
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
    
    btnTodas.classList.remove('bg-primary', 'text-white');
    btnReceita.classList.remove('bg-primary', 'text-white');
    btnDespesa.classList.add('bg-primary', 'text-white');
    
    const categorias = document.querySelectorAll('.categoria');
    categorias.forEach(categoria => {
         categoria.style.display =
            categoria.dataset.tipo === 'despesa' ? 'block' : 'none';
    });
});