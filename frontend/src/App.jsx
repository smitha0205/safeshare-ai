import { useState } from 'react'
import './App.css'

const DOCUMENT_TYPES = [
  'Aadhaar Card',
  'PAN Card',
  'Passport',
  'Resume',
  'Medical Report',
  'Bank Statement',
]

const PLATFORMS = [
  'Government Portal',
  'Banking Website',
  'Job Portal',
  'AI Chatbot',
  'AI Image Generator',
  'Social Media',
]

const API_URL = 'http://127.0.0.1:8000/analyze'

function App() {
  const [documentType, setDocumentType] = useState('')
  const [platform, setPlatform] = useState('')
  const [purpose, setPurpose] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setResult(null)
    setLoading(true)

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ documentType, platform, purpose }),
      })

      if (!response.ok) {
        throw new Error(`Request failed (${response.status})`)
      }

      const data = await response.json()

      setResult({
        riskScore: data.riskScore,
        riskLevel: data.riskLevel,
        explanation: data.explanation,
        recommendation: data.recommendation,
      })
    } catch (err) {
      setError(
        'Could not reach backend. Make sure FastAPI is running on port 8000.'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page">
      <div className="hero">
        <div className="hero-icon">🔍</div>

        <h1 className="hero-title">
          SafeShare AI
        </h1>

        <p className="hero-tagline">
          Think Before You Share
        </p>

        <p className="hero-description">
          AI-powered document safety analysis for digital platforms
        </p>
      </div>

      <form className="card" onSubmit={handleSubmit}>
        <label>
          Document Type
          <select
            value={documentType}
            onChange={(e) => setDocumentType(e.target.value)}
            required
          >
            <option value="">
              Select a document type
            </option>

            {DOCUMENT_TYPES.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </label>

        <label>
          Platform
          <select
            value={platform}
            onChange={(e) => setPlatform(e.target.value)}
            required
          >
            <option value="">
              Select a platform
            </option>

            {PLATFORMS.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </label>

        <label>
          Purpose
          <textarea
            value={purpose}
            onChange={(e) => setPurpose(e.target.value)}
            placeholder="Why are you sharing this document?"
            rows={4}
            required
          />
        </label>

        <button type="submit" disabled={loading}>
          {loading
            ? '🔍 Analyzing document...'
            : 'Check Safety'}
        </button>
      </form>

      {error && (
        <p className="error">
          {error}
        </p>
      )}

      {result && (
        <section className="card results">
          <h2>
            {result.riskLevel === 'Low' && '✅'}
            {result.riskLevel === 'Medium' && '⚠️'}
            {result.riskLevel === 'High' && '🚨'}
            {result.riskLevel === 'Critical' && '⛔'}

            {' '}Safety Analysis
          </h2>

          <div className="metrics">
            <div>
              <span className="label">
                Risk Score
              </span>

              <strong>
                {result.riskScore}
              </strong>
            </div>

            <div>
              <span className="label">
                Risk Level
              </span>

              <div
                className={`risk-badge badge-${result.riskLevel.toLowerCase()}`}
              >
                {result.riskLevel}
              </div>
            </div>
          </div>

          <div className="block">
            <span className="label">
              Explanation
            </span>

            <p>{result.explanation}</p>
          </div>

          <div className="block">
            <span className="label">
              Recommendation
            </span>

            <p>{result.recommendation}</p>
          </div>
        </section>
      )}
    </main>
  )
}

export default App