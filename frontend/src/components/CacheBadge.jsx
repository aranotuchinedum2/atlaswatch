export default function CacheBadge({ info, isDemo }) {
  if (!info) return null

  // Demo mode
  if (isDemo) {
    return (
      <div style={{
        display: 'inline-flex', alignItems: 'center', gap: 8,
        padding: '6px 14px', borderRadius: 3,
        border: '1px solid rgba(150,100,200,0.3)',
        background: 'rgba(150,100,200,0.08)',
        marginBottom: 20,
        fontFamily: "'Space Mono', monospace",
        fontSize: '0.65rem', letterSpacing: '0.08em',
        color: '#b48aff',
      }}>
        <span style={{ width: 6, height: 6, borderRadius: '50%',
          background: '#b48aff', flexShrink: 0 }} />
        🎭 Demo mode — Nitter scraping unavailable. Showing representative data.
      </div>
    )
  }

  const isLive = !info.hit
  const isStale = info.stale

  const label = isLive
    ? '⚡ Live data'
    : isStale
    ? `⚠ Stale cache · ${_age(info.age_seconds)} old`
    : `📦 Cached · ${_age(info.age_seconds)} old · refreshes in ${_age(info.expires_in)}`

  const color = isLive ? 'var(--green-bright)' : isStale ? 'var(--red)' : 'var(--gold)'
  const bg = isLive ? 'rgba(0,136,74,0.08)' : isStale ? 'rgba(193,39,45,0.08)' : 'rgba(200,150,58,0.08)'

  return (
    <div style={{
      display: 'inline-flex', alignItems: 'center', gap: 8,
      padding: '6px 14px', borderRadius: 3,
      border: `1px solid ${color}30`, background: bg, marginBottom: 20,
      fontFamily: "'Space Mono', monospace",
      fontSize: '0.65rem', letterSpacing: '0.08em', color,
    }}>
      <span style={{ width: 6, height: 6, borderRadius: '50%',
        background: color, flexShrink: 0,
        animation: isLive ? 'pulse 1.5s infinite' : 'none' }} />
      {label}
    </div>
  )
}

function _age(seconds) {
  if (!seconds || seconds < 60) return `${seconds}s`
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return s > 0 ? `${m}m ${s}s` : `${m}m`
}