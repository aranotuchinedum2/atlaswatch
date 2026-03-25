// This app was built by CeeJay for Chinedum Aranotu – 2026
import { useState, useCallback } from 'react'
import Header from './components/Header'
import StatsBar from './components/StatsBar'
import SentimentDonut from './components/SentimentDonut'
import SentimentTimeline from './components/SentimentTimeline'
import TweetFeed from './components/TweetFeed'
import WordCloud from './components/WordCloud'
import QuerySelector from './components/QuerySelector'
import Footer from './components/Footer'
import CacheBadge from './components/CacheBadge'
import './app.css'

const API = import.meta.env.VITE_API_URL || ''

export default function App() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [query, setQuery] = useState('Morocco AFCON')
  const [lastFetch, setLastFetch] = useState(null)
  const [cacheInfo, setCacheInfo] = useState(null)

  const fetchTweets = useCallback(async (q = query, force = false) => {
    setLoading(true)
    setError(null)
    try {
      const url = `${API}/api/tweets?query=${encodeURIComponent(q)}&count=60${force ? '&force=true' : ''}`
      const res = await fetch(url)
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || `HTTP ${res.status}`)
      }
      const json = await res.json()
      setCacheInfo(json._cache || null)
      setData(json)
      setLastFetch(new Date())
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [query])

  const handleQueryChange = (q) => {
    setQuery(q)
    setData(null)
    setError(null)
    setCacheInfo(null)
  }

  return (
    <div className="app">
      <div className="grain" aria-hidden />
      <Header />

      <main className="main">
        <QuerySelector
          active={query}
          onChange={handleQueryChange}
          onFetch={() => fetchTweets(query, false)}
          onForce={() => fetchTweets(query, true)}
          loading={loading}
          lastFetch={lastFetch}
        />

        {(cacheInfo || data?._demo) && (
          <CacheBadge info={cacheInfo} isDemo={data?._demo} />
    )}

        {error && (
          <div className="error-banner">
            <span className="error-icon">⚠</span>
            <div>
              <strong>Scraping unavailable</strong>
              <p>{error}</p>
              <small>Nitter instances may be overloaded. Wait 60 s and retry — or cached data will serve automatically once available.</small>
            </div>
          </div>
        )}

        {loading && (
          <div className="loading-state">
            <div className="spinner" />
            <p>Scraping live tweets and analysing sentiment…</p>
          </div>
        )}

        {data && !loading && (
          <>
            <StatsBar stats={data.stats} />
            <div className="charts-grid">
              <SentimentDonut stats={data.stats} />
              <SentimentTimeline timeline={data.timeline} />
            </div>
            <div className="bottom-grid">
              <TweetFeed tweets={data.tweets} />
              <WordCloud keywords={data.keywords} />
            </div>
          </>
        )}

        {!data && !loading && !error && (
          <div className="empty-state">
            <div className="flag-icon">🇲🇦</div>
            <h2>Select a query and hit <em>Analyse</em></h2>
            <p>AtlasWatch scrapes real tweets and scores them live. Results cache for 15 min.</p>
          </div>
        )}
      </main>

      <Footer />
    </div>
  )
}
