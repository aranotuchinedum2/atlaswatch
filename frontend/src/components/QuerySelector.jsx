const QUERIES = [
  'Morocco AFCON',
  'Senegal AFCON',
  'AFCON 2025 final',
  'CAF ruling Morocco',
  'AFCON controversy',
  'Morocco champion',
  'Senegal forfeit',
  'AtlasLions AFCON',
]

export default function QuerySelector({ active, onChange, onFetch, onForce, loading, lastFetch }) {
  return (
    <div className="query-bar">
      <span className="query-label">Query →</span>
      {QUERIES.map((q) => (
        <button
          key={q}
          className={`query-btn ${active === q ? 'active' : ''}`}
          onClick={() => onChange(q)}
        >
          {q}
        </button>
      ))}

      <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 8 }}>
        {lastFetch && (
          <button
            className="query-btn"
            onClick={onForce}
            disabled={loading}
            title="Force a fresh scrape, bypassing the 15-min cache"
            style={{ opacity: loading ? 0.4 : 0.7, fontSize: '0.65rem' }}
          >
            ↺ Force refresh
          </button>
        )}
        <button
          className="analyse-btn"
          onClick={onFetch}
          disabled={loading}
        >
          {loading ? '⏳ Scraping…' : '⚡ Analyse'}
        </button>
      </div>

      {lastFetch && (
        <span className="last-fetch">
          Last fetch: {lastFetch.toLocaleTimeString()}
        </span>
      )}
    </div>
  )
}
