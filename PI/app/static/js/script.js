// Configuração do gráfico chart
// Seleciona o elemento do gráfico com o id 'expenseRevenueChart'
const chartElement = document.getElementById('expenseRevenueChart');

// Verifica se o elemento do gráfico está presente na página
if (chartElement) {
    // Obtém o contexto 2D do elemento do gráfico
    const ctx = chartElement.getContext('2d');

    // Cria um novo gráfico do tipo rosca com os dados
    const expenseRevenueChart = new Chart(ctx, {
        // Tipo de gráfico: rosca
        type: 'doughnut',
        data: {
            // Rótulos para os segmentos
            labels: labels,
            // Conjunto de dados para o gráfico
            datasets: [{
                // Dados para o gráfico
                data: data,
                // Cores de fundo para os segmentos (paleta do projeto)
                backgroundColor: [
                    'rgba(96, 165, 250, 0.4)',   // Azul claro principal
                    'rgba(59, 130, 246, 0.4)',   // Azul médio
                    'rgba(29, 78, 216, 0.4)',    // Azul escuro
                    'rgba(139, 92, 246, 0.4)',   // Roxo suave
                    'rgba(16, 185, 129, 0.4)',   // Verde esmeralda
                    'rgba(245, 158, 11, 0.4)',   // Âmbar
                    'rgba(236, 72, 153, 0.4)',   // Rosa
                    'rgba(34, 197, 94, 0.4)'     // Verde
                ],
                // Cores de borda para os segmentos
                borderColor: [
                    'rgba(96, 165, 250, 0.9)',   // Azul claro principal
                    'rgba(59, 130, 246, 0.9)',   // Azul médio
                    'rgba(29, 78, 216, 0.9)',    // Azul escuro
                    'rgba(139, 92, 246, 0.9)',   // Roxo suave
                    'rgba(16, 185, 129, 0.9)',   // Verde esmeralda
                    'rgba(245, 158, 11, 0.9)',   // Âmbar
                    'rgba(236, 72, 153, 0.9)',   // Rosa
                    'rgba(34, 197, 94, 0.9)'     // Verde
                ],
                // Largura da borda dos segmentos
                borderWidth: 1
            }]
        },
        // Opções de configuração do gráfico
        options: {
            // Responsividade do gráfico, plugins, legendas
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#e2e8f0',
                        font: {
                            family: 'Inter, sans-serif',
                            size: 12
                        },
                        padding: 20
                    }
                },
                // Configuração de tooltip para mostrar porcentagens e valores
                tooltip: {
                    backgroundColor: 'rgba(30, 30, 46, 0.95)',
                    titleColor: '#f8fafc',
                    bodyColor: '#e2e8f0',
                    borderColor: 'rgba(96, 165, 250, 0.5)',
                    borderWidth: 1,
                    cornerRadius: 12,
                    titleFont: {
                        family: 'Inter, sans-serif',
                        size: 13,
                        weight: '600'
                    },
                    bodyFont: {
                        family: 'Inter, sans-serif',
                        size: 12
                    },
                    padding: 12,
                    callbacks: {
                        label: function(tooltipItem) {
                            const total = data.reduce((acc, value) => acc + value, 0);
                            const value = tooltipItem.raw;
                            const percentage = ((value / total) * 100).toFixed(2);
                            return `${tooltipItem.label}: R$ ${value.toFixed(2)} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}




document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    
    if (calendarEl) {
        var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            events: '/api/events',
            height: 'auto',
            contentHeight: 'auto',
        });
        calendar.render();
    }
});
