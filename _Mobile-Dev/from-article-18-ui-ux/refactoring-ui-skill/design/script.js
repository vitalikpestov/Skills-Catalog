/**
 * Dashboard Interactive Functionality
 * Handles tab switching, chart animations, and user interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    initTabSwitching();
    initChartAnimations();
    initNavigation();
    initSearchBox();
});

/**
 * Tab Switching for Chart Period Selection
 */
function initTabSwitching() {
    const tabButtons = document.querySelectorAll('.tab-btn');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all tabs
            tabButtons.forEach(b => b.classList.remove('active'));
            // Add active class to clicked tab
            btn.classList.add('active');

            // Update chart data based on period
            const period = btn.dataset.period;
            updateChartData(period);
        });
    });
}

/**
 * Update chart bars based on selected period
 */
function updateChartData(period) {
    const chartBars = document.querySelectorAll('.chart-bar');

    const data = {
        week: [
            { height: '65%', value: '$32k', label: 'Mon' },
            { height: '45%', value: '$24k', label: 'Tue' },
            { height: '80%', value: '$41k', label: 'Wed' },
            { height: '55%', value: '$28k', label: 'Thu' },
            { height: '90%', value: '$46k', label: 'Fri' },
            { height: '70%', value: '$35k', label: 'Sat' },
            { height: '40%', value: '$20k', label: 'Sun' }
        ],
        month: [
            { height: '75%', value: '$148k', label: 'W1' },
            { height: '60%', value: '$122k', label: 'W2' },
            { height: '85%', value: '$168k', label: 'W3' },
            { height: '70%', value: '$140k', label: 'W4' },
            { height: '55%', value: '$112k', label: '' },
            { height: '0%', value: '', label: '' },
            { height: '0%', value: '', label: '' }
        ],
        year: [
            { height: '45%', value: '$380k', label: 'Q1' },
            { height: '65%', value: '$520k', label: 'Q2' },
            { height: '80%', value: '$640k', label: 'Q3' },
            { height: '70%', value: '$560k', label: 'Q4' },
            { height: '0%', value: '', label: '' },
            { height: '0%', value: '', label: '' },
            { height: '0%', value: '', label: '' }
        ]
    };

    const periodData = data[period];

    chartBars.forEach((bar, index) => {
        if (periodData[index]) {
            bar.style.setProperty('--height', periodData[index].height);
            bar.dataset.value = periodData[index].value;

            const label = bar.querySelector('.bar-label');
            if (label) {
                label.textContent = periodData[index].label;
            }

            // Show/hide bars based on data
            bar.style.display = periodData[index].height === '0%' ? 'none' : 'block';
        }
    });
}

/**
 * Initialize chart entrance animations
 */
function initChartAnimations() {
    const chartBars = document.querySelectorAll('.chart-bar');

    // Animate bars on load
    chartBars.forEach((bar, index) => {
        const height = bar.style.getPropertyValue('--height');
        bar.style.setProperty('--height', '0%');

        setTimeout(() => {
            bar.style.setProperty('--height', height);
        }, 100 + (index * 50));
    });

    // Animate donut chart
    const donutRing = document.querySelector('.donut-ring');
    if (donutRing) {
        donutRing.style.opacity = '0';
        donutRing.style.transform = 'scale(0.8)';

        setTimeout(() => {
            donutRing.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
            donutRing.style.opacity = '1';
            donutRing.style.transform = 'scale(1)';
        }, 300);
    }

    // Animate stat cards
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';

        setTimeout(() => {
            card.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 + (index * 80));
    });
}

/**
 * Navigation active state handling
 */
function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();

            // Remove active class from all items
            navItems.forEach(nav => nav.classList.remove('active'));

            // Add active class to clicked item
            item.classList.add('active');

            // Get page name for potential routing
            const pageName = item.querySelector('span').textContent;
            console.log(`Navigating to: ${pageName}`);
        });
    });
}

/**
 * Search box functionality
 */
function initSearchBox() {
    const searchInput = document.querySelector('.search-input');

    if (searchInput) {
        let debounceTimer;

        searchInput.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);

            debounceTimer = setTimeout(() => {
                const query = e.target.value.trim();
                if (query.length >= 2) {
                    performSearch(query);
                }
            }, 300);
        });

        // Clear search on Escape
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                searchInput.value = '';
                searchInput.blur();
            }
        });
    }
}

/**
 * Perform search (placeholder for actual implementation)
 */
function performSearch(query) {
    console.log(`Searching for: ${query}`);
    // In a real app, this would filter data or make an API call
}

/**
 * Format currency values
 */
function formatCurrency(value, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value);
}

/**
 * Format numbers with commas
 */
function formatNumber(value) {
    return new Intl.NumberFormat('en-US').format(value);
}

/**
 * Calculate percentage change
 */
function calculateChange(current, previous) {
    const change = ((current - previous) / previous) * 100;
    return {
        value: Math.abs(change).toFixed(1),
        isPositive: change >= 0
    };
}
