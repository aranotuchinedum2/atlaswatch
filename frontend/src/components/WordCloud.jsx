export default function WordCloud({ keywords }) {
  if (!keywords || !keywords.length) return null
  const maxCount = keywords[0]?.count || 1

  return (
    <div className="card">
      <p className="card-title">Top Keywords</p>
      <div className="word-list">
        {keywords.map(({ word, count }) => {
          const ratio = count / maxCount
          const size = 0.65 + ratio * 0.7
          const opacity = 0.4 + ratio * 0.6
          return (
            <span key={word} className="word-tag"
              title={`${count} mentions`}
              style={{ '--tag-size': `${size}rem`, opacity }}>
              {word}
              <span style={{
                marginLeft: 5, fontFamily: "'Space Mono', monospace",
                fontSize: '0.55rem', color: 'rgba(255,255,255,0.25)',
              }}>{count}</span>
            </span>
          )
        })}
      </div>
    </div>
  )
}