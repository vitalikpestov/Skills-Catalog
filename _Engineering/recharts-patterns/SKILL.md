---
name: recharts-patterns
description: Reusable patterns for building responsive, accessible, and performant charts with Recharts 3.x in React applications. Use when building dashboards, data visualizations, financial charts, or any chart components with Recharts. Covers composable chart components, ResponsiveContainer, syncable multi-chart dashboards, custom tooltips/legends, gradients, reference lines, brush/zoom, and animations.
---

# Recharts Patterns

Production-ready patterns for Recharts 3.x in React/Next.js applications.

## When to Use

- Building dashboard charts (line, area, bar, pie, radar)
- Financial data visualization (equity curves, drawdowns, gauges)
- Custom tooltips with rich data
- Reference lines for thresholds (e.g., HF floor, LTV targets)
- Synchronized multi-chart dashboards
- Brush/zoom for historical data exploration

## Core Patterns

### 1. ResponsiveContainer (Always Wrap)

```tsx
// ALWAYS wrap charts in ResponsiveContainer
<ResponsiveContainer width="100%" height={300}>
  <LineChart data={data}>
    {/* ... */}
  </LineChart>
</ResponsiveContainer>

// NEVER set fixed width on chart directly
```

### 2. Custom Tooltip

```tsx
function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-card border border-border rounded-lg p-3 shadow-lg">
      <p className="text-sm font-medium">{label}</p>
      {payload.map((entry: any, i: number) => (
        <p key={i} className="text-sm" style={{ color: entry.color }}>
          {entry.name}: {typeof entry.value === 'number'
            ? entry.value.toLocaleString(undefined, { maximumFractionDigits: 2 })
            : entry.value}
        </p>
      ))}
    </div>
  );
}

// Usage
<Tooltip content={<CustomTooltip />} />
```

### 3. Reference Lines for Thresholds

```tsx
<LineChart data={data}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="date" />
  <YAxis />

  {/* HF floor warning line */}
  <ReferenceLine
    y={1.3}
    stroke="#ef4444"
    strokeDasharray="5 5"
    label={{ value: "HF Floor (1.3)", position: "right", fill: "#ef4444", fontSize: 12 }}
  />

  {/* Target LTV line */}
  <ReferenceLine
    y={35}
    stroke="#f59e0b"
    strokeDasharray="5 5"
    label={{ value: "LTV Target (35%)", position: "right", fill: "#f59e0b", fontSize: 12 }}
  />

  <Line type="monotone" dataKey="hf" stroke="#3b82f6" strokeWidth={2} dot={false} />
</LineChart>
```

### 4. Gradient Fills for Zones

```tsx
<AreaChart data={data}>
  <defs>
    {/* Green zone: healthy */}
    <linearGradient id="healthyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stopColor="#10b981" stopOpacity={0.3} />
      <stop offset="100%" stopColor="#10b981" stopOpacity={0} />
    </linearGradient>
    {/* Red zone: danger */}
    <linearGradient id="dangerGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stopColor="#ef4444" stopOpacity={0.3} />
      <stop offset="100%" stopColor="#ef4444" stopOpacity={0} />
    </linearGradient>
  </defs>

  <Area
    type="monotone"
    dataKey="equity"
    stroke="#10b981"
    fill="url(#healthyGrad)"
    strokeWidth={2}
  />
</AreaChart>
```

### 5. Brush for Zoom/Pan on Historical Data

```tsx
<LineChart data={longHistoricalData}>
  <XAxis dataKey="date" />
  <YAxis />
  <Line type="monotone" dataKey="equity" stroke="#3b82f6" dot={false} />

  {/* Interactive brush for selecting date range */}
  <Brush
    dataKey="date"
    height={30}
    stroke="#6b7280"
    startIndex={longHistoricalData.length - 30}  // Show last 30 days by default
  />
</LineChart>
```

### 6. Synchronized Multi-Chart Dashboard

```tsx
// syncId makes hover/zoom sync across charts
<div className="space-y-4">
  <ResponsiveContainer width="100%" height={200}>
    <LineChart data={data} syncId="dashboard">
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip content={<CustomTooltip />} />
      <Line dataKey="equity" stroke="#10b981" dot={false} />
    </LineChart>
  </ResponsiveContainer>

  <ResponsiveContainer width="100%" height={200}>
    <LineChart data={data} syncId="dashboard">
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip content={<CustomTooltip />} />
      <Line dataKey="hf" stroke="#3b82f6" dot={false} />
      <ReferenceLine y={1.3} stroke="#ef4444" strokeDasharray="5 5" />
    </LineChart>
  </ResponsiveContainer>
</div>
```

### 7. Composed Chart (Multiple Types)

```tsx
<ComposedChart data={data}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="date" />
  <YAxis yAxisId="left" />
  <YAxis yAxisId="right" orientation="right" />
  <Tooltip content={<CustomTooltip />} />
  <Legend />

  <Area yAxisId="left" dataKey="equity" fill="url(#healthyGrad)" stroke="#10b981" />
  <Bar yAxisId="right" dataKey="volume" fill="#6b7280" opacity={0.3} />
  <Line yAxisId="left" dataKey="debt" stroke="#ef4444" dot={false} />
</ComposedChart>
```

### 8. Radial/Gauge for Health Score

```tsx
// Simple gauge using RadialBarChart
const gaugeData = [{ name: "Health", value: healthScore, fill: getColor(healthScore) }];

function getColor(score: number) {
  if (score >= 80) return "#10b981";
  if (score >= 50) return "#f59e0b";
  return "#ef4444";
}

<ResponsiveContainer width={200} height={200}>
  <RadialBarChart
    cx="50%" cy="50%"
    innerRadius="60%" outerRadius="90%"
    startAngle={180} endAngle={0}
    data={gaugeData}
  >
    <RadialBar dataKey="value" cornerRadius={10} background />
    <text x="50%" y="50%" textAnchor="middle" dominantBaseline="middle"
      className="text-2xl font-bold fill-foreground">
      {healthScore}
    </text>
  </RadialBarChart>
</ResponsiveContainer>
```

## Performance Tips

- Use `dot={false}` on Line/Area for large datasets (>100 points)
- Use `isAnimationActive={false}` for real-time updating charts
- Memoize data transformations with `useMemo`
- Use `Brush` instead of rendering all data points
- Debounce resize events in ResponsiveContainer

## Dark Theme Integration

```tsx
// Use CSS variables for theme-aware colors
const chartColors = {
  grid: "hsl(var(--border))",
  text: "hsl(var(--muted-foreground))",
  tooltip: {
    bg: "hsl(var(--card))",
    border: "hsl(var(--border))",
  },
};

<CartesianGrid stroke={chartColors.grid} strokeDasharray="3 3" />
<XAxis stroke={chartColors.text} tick={{ fill: chartColors.text, fontSize: 12 }} />
```

## Constraints

### MUST DO
- Always use ResponsiveContainer as wrapper
- Provide accessible labels (aria-label on container)
- Use `toLocaleString()` for number formatting in tooltips
- Test with empty data gracefully (show placeholder)
- Use `dot={false}` for datasets > 50 points

### MUST NOT DO
- Set fixed pixel widths on charts
- Use more than 5-6 colors per chart (cognitive overload)
- Animate real-time updating charts
- Nest ResponsiveContainer inside flex/grid without explicit height
