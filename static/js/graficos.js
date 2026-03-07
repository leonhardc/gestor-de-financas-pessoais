// static/js/graficos.js

// Funcao para plotar grafico de pizza
(() => {
    try {
        const labels = JSON.parse(document.getElementById('dashboard-labels').textContent);
        const valores = JSON.parse(document.getElementById('dashboard-valores').textContent);
    
        const ctx = document.getElementById('graficoDespesas');
    
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: valores,
                }]
            },
            options: {
                responsive: true,
                maintainAscpectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'left',
                    }
                },
            }
        });
    } catch (error) {
        console.error('Erro ao plotar gráfico de despesas:', error);
    }
})();

// Funcao para plotar grafico de linha de despesas e receitas mensais
(() => {
    try {
        const dias = JSON.parse(document.getElementById('dashboard-dias').textContent);
        const receitas = JSON.parse(document.getElementById('dashboard-receitas').textContent);
        const despesas = JSON.parse(document.getElementById('dashboard-despesas').textContent);
    
        const ctx = document.getElementById('graficoMensal');
    
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: dias,
                datasets: [
                    {
                        label: 'Receitas',
                        data: receitas,
                        borderWidth: 2,
                        tension: 0.3
                    },
                    {
                        label: 'Despesas',
                        data: despesas,
                        borderWidth: 2,
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (error) {
        console.error('Erro ao plotar gráfico mensal:', error);
    }
})();

// Funcao para plotar grafico de linha de despesas e receitas mensais
(() => {
    try {
        const labels = JSON.parse(document.getElementById('categorias-labels').textContent);
        const valores = JSON.parse(document.getElementById('categorias-valores').textContent);
    
        const ctx = document.getElementById('graficoCategoria');
    
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Gastos por Categoria',
                    data: valores,
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    catch (error) {
        console.error('Erro ao plotar gráfico de categorias:', error);
    }
})();

