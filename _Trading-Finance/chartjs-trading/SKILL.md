---
name: chartjs-trading
description: Chart.js patterns for trading dashboards — equity curves, price charts, regime visualization, PnL bars
---

# Chart.js Trading Dashboard Patterns

Use these patterns when building or updating the bot dashboard (`implement/dashboard.html`).

## Already Loaded
Chart.js is loaded via CDN in dashboard.html:
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

## Useful Plugins (add as needed)
```html
<!-- Zoom & pan -->
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@2.0.1/dist/chartjs-plugin-zoom.min.js"></script>
<!-- Annotations (support/resistance lines) -->
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@3.0.1/dist/chartjs-plugin-annotation.min.js"></script>
<!-- Financial/candlestick charts -->
<script src="https://cdn.jsdelivr.net/npm/chartjs-chart-financial@0.2.0/dist/chartjs-chart-financial.min.js"></script>
```

## Pattern: Real-time Price Line (WebSocket update)
```javascript
const priceChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      label: 'Price',
      data: [],
      borderColor: '#00e5b0',
      borderWidth: 1.5,
      pointRadius: 0,
      tension: 0.1,
      fill: false
    }]
  },
  options: {
    animation: false,  // critical for real-time
    scales: {
      x: { display: false },
      y: { position: 'right' }
    },
    plugins: { legend: { display: false } }
  }
});

// Update from WebSocket
function updatePrice(time, price) {
  priceChart.data.labels.push(time);
  priceChart.data.datasets[0].data.push(price);
  if (priceChart.data.labels.length > 100) {
    priceChart.data.labels.shift();
    priceChart.data.datasets[0].data.shift();
  }
  priceChart.update('none');  // 'none' = no animation for speed
}
```

## Pattern: Equity Curve with Drawdown Fill
```javascript
datasets: [
  { label: 'Equity', data: equityData, borderColor: '#00e5b0', fill: false },
  { label: 'Peak', data: peakData, borderColor: '#4a5568', borderDash: [5,5], fill: false },
  { label: 'Drawdown', data: ddData, backgroundColor: 'rgba(255,61,107,0.15)', fill: true }
]
```

## Pattern: PnL Bar Chart (green/red per trade)
```javascript
backgroundColor: pnlData.map(v => v >= 0 ? '#00e5b0' : '#ff3d6b')
```

## Pattern: Regime Timeline (colored segments)
```javascript
// Use annotation plugin to draw colored background bands
annotation: {
  annotations: regimeData.map(r => ({
    type: 'box',
    xMin: r.start, xMax: r.end,
    backgroundColor: r.regime === 'BULL' ? 'rgba(0,229,176,0.08)' :
                     r.regime === 'BEAR' ? 'rgba(255,61,107,0.08)' : 'rgba(77,139,255,0.05)',
    borderWidth: 0
  }))
}
```

## Guidelines
- Always use `animation: false` for real-time charts
- Use `update('none')` when pushing data via WebSocket
- Keep max 100-200 points visible, shift old data out
- Use `pointRadius: 0` for performance on line charts
- Dark theme colors: green #00e5b0, red #ff3d6b, blue #4d8bff, muted #4a5568
