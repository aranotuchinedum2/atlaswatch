import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'

const COLORS = { positive: '#00884a', negative: '#e63740', neutral: '#C8963A' }

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload[0]) {
    const { name, value } = payload[0]
    return (
      <div style={{
        background: '#111820', border: '1px solid rgba(255,255,255,0.1)',
        padding: '10px 14px', borderRadius: 4,
        fontFamily: "'Space Mono', monospace", fontSize: '0.72rem',
        color: COLORS[name] || '#f0ede6'
      }}>
        <strong style={{ textTransform: 'uppercase', letterSpacing: '0.1em' }}>{name}</strong>
        <br />{value} tweets
      </div>
    )
  }
  return null
}

export default function SentimentDonut({ stats }) {
  const data = [
    { name: 'positive', value: stats.positive },
    { name: 'negative', value: stats.negative },
    { name: 'neutral',  value: stats.neutral  },
  ].filter(d => d.value > 0)

  return (
    <div className="card">
      <p className="card-title">Sentiment Breakdown</p>
      <ResponsiveContainer width="100%" height={220}>
        <PieChart>
          <Pie data={data} cx="50%" cy="50%" innerRadius={65} outerRadius={95}
            paddingAngle={3} dataKey="value" stroke="none">
            {data.map(entry => (
              <Cell key={entry.name} fill={COLORS[entry.name]} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
        </PieChart>
      </ResponsiveContainer>

      <div className="donut-legend">
        {[
          { key: 'positive', label: 'Positive', pct: stats.positive_pct },
          { key: 'negative', label: 'Negative', pct: stats.negative_pct },
          { key: 'neutral',  label: 'Neutral',  pct: stats.neutral_pct  },
        ].map(({ key, label, pct }) => (
          <div className="legend-row" key={key}>
            <div className="legend-dot" style={{ background: COLORS[key] }} />
            <span className="legend-label">{label}</span>
            <span className="legend-pct">{pct}%</span>
            <div style={{ height: 4, flex: 3, borderRadius: 2,
              background: 'rgba(255,255,255,0.05)', overflow: 'hidden' }}>
              <div style={{ height: '100%', width: `${pct}%`,
                background: COLORS[key], borderRadius: 2,
                transition: 'width 0.6s ease' }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}