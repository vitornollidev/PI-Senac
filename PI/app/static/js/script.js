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
            // Configuração em português brasileiro
            locale: 'pt-br',
            
            // Visualização inicial
            initialView: 'dayGridMonth',
            
            // Altura automática
            height: 'auto',
            contentHeight: 'auto',
            
            // Cabeçalho personalizado
            headerToolbar: false,
            
            // Configurações de visualização
            dayMaxEvents: 3,
            moreLinkClick: 'popover',
            
            // Estilo dos dias
            dayCellClassNames: 'calendar-day-cell',
            dayHeaderClassNames: 'calendar-day-header',
            
            // Configurações de eventos
            events: '/api/events',
            eventDisplay: 'block',
            eventClassNames: 'calendar-event',
            
            // Configurações de interação
            selectable: true,
            selectMirror: true,
            editable: true,
            droppable: true,
            
            // Configurações de data
            firstDay: 1, // Segunda-feira como primeiro dia
            
            // Configurações de cores e estilo
            eventColor: '#60a5fa',
            eventTextColor: '#ffffff',
            
            // Configurações de popover
            eventDidMount: function(info) {
                // Adicionar tooltip personalizado
                info.el.setAttribute('title', info.event.title);
                
                // Adicionar classes baseadas no tipo de evento
                if (info.event.title.includes('Receita') || info.event.title.includes('Salário')) {
                    info.el.classList.add('event-income');
                } else if (info.event.title.includes('Despesa') || info.event.title.includes('Conta')) {
                    info.el.classList.add('event-expense');
                } else {
                    info.el.classList.add('event-general');
                }
            },
            
            // Configurações de seleção
            select: function(info) {
                // Aqui você pode adicionar funcionalidade para criar novos eventos
                console.log('Data selecionada:', info.startStr);
            },
            
            // Configurações de clique em evento
            eventClick: function(info) {
                // Aqui você pode adicionar funcionalidade para editar eventos
                console.log('Evento clicado:', info.event.title);
            }
        });
        
        // Renderizar o calendário
        calendar.render();
        
        // Configurar controles personalizados
        setupCalendarControls(calendar);
        
        // Atualizar título do mês
        updateMonthTitle(calendar);
    }
});

// Função para configurar controles personalizados
function setupCalendarControls(calendar) {
    const prevBtn = document.getElementById('prev-month');
    const nextBtn = document.getElementById('next-month');
    
    if (prevBtn) {
        prevBtn.addEventListener('click', function() {
            calendar.prev();
            updateMonthTitle(calendar);
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            calendar.next();
            updateMonthTitle(calendar);
        });
    }
}

// Função para atualizar o título do mês
function updateMonthTitle(calendar) {
    const monthTitle = document.getElementById('current-month');
    if (monthTitle) {
        const currentDate = calendar.getDate();
        const monthNames = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ];
        
        const month = monthNames[currentDate.getMonth()];
        const year = currentDate.getFullYear();
        
        monthTitle.textContent = `${month} ${year}`;
    }
}

// Função moderna para auto-hide das mensagens flash após 5 segundos
function autoHideFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash');
    
    flashMessages.forEach(function(message) {
        // Adicionar transição suave moderna
        message.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
        
        // Adicionar efeito de entrada suave
        message.style.opacity = '0';
        message.style.transform = 'translateY(-20px) scale(0.95)';
        
        // Animar entrada
        setTimeout(function() {
            message.style.opacity = '1';
            message.style.transform = 'translateY(0) scale(1)';
        }, 50);
        
        // Após 5 segundos, fazer a mensagem desaparecer
        setTimeout(function() {
            message.style.opacity = '0';
            message.style.transform = 'translateY(-20px) scale(0.95)';
            message.style.filter = 'blur(2px)';
            
            // Remover o elemento após a animação
            setTimeout(function() {
                if (message.parentNode) {
                    message.parentNode.removeChild(message);
                }
            }, 600); // 600ms para a animação
        }, 5000); // 5 segundos
    });
}

// Executar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    autoHideFlashMessages();
});

// Também executar quando a página for carregada (para casos onde DOMContentLoaded já foi disparado)
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', autoHideFlashMessages);
} else {
    autoHideFlashMessages();
}