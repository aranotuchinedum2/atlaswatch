import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
  Tooltip, ReferenceLine, ResponsiveContainer
} from 'recharts'

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload[0]) {
    const val = payload[0].value
    const color = val >= 0.05 ? '#00884a' : val <= -0.05 ? '#e63740' : '#C8963A'
    return (
      <div style={{
        background: '#111820', border: '1px solid rgba(255,255,255,0.1)',
        padding: '10px 14px', borderRadius: 4,
        fontFamily: "'Space Mono', monospace", fontSize: '0.7rem',
      }}>
        <p style={{ color: '#8a8f9b' }}>Batch {label}</p>
        <p style={{ color, fontWeight: 700 }}>Score: {val > 0 ? '+' : ''}{val}</p>
      </div>
    )
  }
  return null
}

export default function SentimentTimeline({ timeline }) {
  if (!timeline || !timeline.length) return null

  return (
    <div className="card">
      <p className="card-title">Sentiment Over Time (tweet batches of 5)</p>
      <ResponsiveContainer width="100%" height={280}>
        <AreaChart data={timeline} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <defs>
            <linearGradient id="sentGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%"  stopColor="#00884a" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#00884a" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
          <XAxis dataKey="batch"
            tick={{ fontFamily: "'Space Mono'", fontSize: 10, fill: '#4a5060' }}
            axisLine={{ stroke: 'rgba(255,255,255,0.07)' }} tickLine={false} />
          <YAxis domain={[-1, 1]}
            tick={{ fontFamily: "'Space Mono'", fontSize: 10, fill: '#4a5060' }}
            axisLine={false} tickLine={false} />
          <Tooltip content={<CustomTooltip />} />
          <ReferenceLine y={0}    stroke="rgba(255,255,255,0.15)" strokeDasharray="4 4" />
          <ReferenceLine y={0.05} stroke="rgba(0,136,74,0.2)"    strokeDasharray="2 4" />
          <ReferenceLine y={-0.05} stroke="rgba(230,55,64,0.2)"  strokeDasharray="2 4" />
          <Area type="monotone" dataKey="avg" stroke="#00884a" strokeWidth={2}
            fill="url(#sentGrad)"
            dot={{ fill: '#00884a', r: 3, strokeWidth: 0 }}
            activeDot={{ r: 5, fill: '#f0b84a' }} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}