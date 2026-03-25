const SCORE_COLORS = {
  positive: '#00884a',
  negative: '#e63740',
  neutral: '#C8963A',
}

function TweetCard({ tweet }) {
  const { text, user, username, sentiment, likes, retweets, date, link } = tweet
  const label = sentiment.label
  const absCompound = Math.abs(sentiment.compound)
  const color = SCORE_COLORS[label]

  const displayDate = date
    ? new Date(date).toLocaleString('en-GB', {
        day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'
      })
    : ''

  return (
    <div className={`tweet-card ${label}`}>
      <div className="tweet-header">
        <div className="tweet-user">
          <strong>{user}</strong>{' '}
          <span style={{ color: '#4a5060' }}>@{username}</span>
        </div>
        <span className={`sentiment-badge ${label}`}>{label}</span>
      </div>

      <p className="tweet-text">{text}</p>

      <div className="score-bar">
        <div className="score-fill" style={{
          width: `${absCompound * 100}%`,
          background: color,
          opacity: 0.7,
        }} />
      </div>

      <div className="tweet-meta">
        <span>♥ {likes}</span>
        <span>↺ {retweets}</span>
        <span style={{ marginLeft: 'auto' }}>
          Score: {sentiment.compound > 0 ? '+' : ''}{sentiment.compound}
        </span>
        {displayDate && <span>{displayDate}</span>}
        {link && (
          <a href={`https://twitter.com${link}`} target="_blank" rel="noreferrer"
            style={{ color: '#4a5060', textDecoration: 'none' }}>↗</a>
        )}
      </div>
    </div>
  )
}

export default function TweetFeed({ tweets }) {
  return (
    <div className="card tweet-feed">
      <p className="card-title">
        Live Tweet Feed
        <span style={{ marginLeft: 'auto', color: '#4a5060' }}>{tweets.length} tweets</span>
      </p>
      <div className="tweet-list">
        {tweets.map((tw, i) => <TweetCard key={tw.id || i} tweet={tw} />)}
      </div>
    </div>
  )
}