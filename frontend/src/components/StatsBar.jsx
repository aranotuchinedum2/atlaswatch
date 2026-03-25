export default function StatsBar({ stats }) {
  const { total, positive, negative, neutral,
          positive_pct, negative_pct, neutral_pct,
          avg_compound, overall } = stats

  return (
    <div className="stats-bar">
      <div className="stat-card total">
        <p className="stat-label">Tweets Analysed</p>
        <p className="stat-value">{total}</p>
        <p className="stat-sub">Real scraped tweets</p>
      </div>
      <div className="stat-card positive">
        <p className="stat-label">Positive</p>
        <p className="stat-value">{positive_pct}%</p>
        <p className="stat-sub">{positive} tweets</p>
      </div>
      <div className="stat-card negative">
        <p className="stat-label">Negative</p>
        <p className="stat-value">{negative_pct}%</p>
        <p className="stat-sub">{negative} tweets</p>
      </div>
      <div className="stat-card neutral">
        <p className="stat-label">Neutral</p>
        <p className="stat-value">{neutral_pct}%</p>
        <p className="stat-sub">{neutral} tweets</p>
      </div>
      <div className="stat-card overall">
        <p className="stat-label">Avg Compound Score</p>
        <p className="stat-value" style={{ fontSize: '2rem' }}>
          {avg_compound > 0 ? '+' : ''}{avg_compound}
        </p>
        <p className="stat-sub" style={{ marginTop: 6 }}>{overall}</p>
      </div>
    </div>
  )
}