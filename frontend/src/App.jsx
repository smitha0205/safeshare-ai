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

const LANGUAGES = [
  'English',
  'Hindi',
  'Telugu',
]

const API_URL = 'http://127.0.0.1:8000/analyze'

function App() {
  const [documentType, setDocumentType] = useState('')
  const [platform, setPlatform] = useState('')
  const [purpose, setPurpose] = useState('')
  const [language, setLanguage] = useState('English')
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
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          documentType,
          platform,
          purpose,
          language,
        }),
      })

      if (!response.ok) {
        throw new Error(`Request failed (${response.status})`)
      }

      const data = await response.json()

      setResult({
        riskScore: data.riskScore,
        riskLevel: data.riskLevel,
        breakdown: data.breakdown,
        explanation: data.explanation,
        recommendation: data.recommendation,
      })
    } catch (err) {
      const isNetworkError =
        err instanceof TypeError ||
        (err instanceof Error &&
          /failed to fetch|networkerror/i.test(err.message))

      setError(
        isNetworkError
          ? 'Could not reach the backend. Make sure it is running at http://127.0.0.1:8000.'
          : err instanceof Error
            ? err.message
            : 'Could not check safety. Please try again.'
      )
    } finally {
      setLoading(false)
    }
  }

  const riskClass = result?.riskLevel
    ? `risk-${String(result.riskLevel)
        .toLowerCase()
        .replace(/\s+/g, '-')}`
    : ''

  return (
    <main className="page">
      <header className="hero">
        <div className="hero-icon">🔍</div>

        <h1 className="hero-title">
          SafeShare AI
        </h1>

        <p className="hero-tagline">
          Think Before You Share
        </p>

        <p className="hero-description">
          Check whether sharing a document on a platform is likely to be safe.
        </p>
      </header>

      <form className="card" onSubmit={handleSubmit}>
        <label htmlFor="documentType">
          Document Type
          <select
            id="documentType"
            value={documentType}
            onChange={(e) => setDocumentType(e.target.value)}
            required
          >
            <option value="" disabled>
              Select a document type
            </option>

            {DOCUMENT_TYPES.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </label>

        <label htmlFor="platform">
          Platform
          <select
            id="platform"
            value={platform}
            onChange={(e) => setPlatform(e.target.value)}
            required
          >
            <option value="" disabled>
              Select a platform
            </option>

            {PLATFORMS.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </label>

        <label htmlFor="language">
          Language
          <select
            id="language"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
          >
            {LANGUAGES.map((lang) => (
              <option key={lang} value={lang}>
                {lang}
              </option>
            ))}
          </select>
        </label>

        <label htmlFor="purpose">
          Purpose
          <textarea
            id="purpose"
            value={purpose}
            onChange={(e) => setPurpose(e.target.value)}
            placeholder="Why are you sharing this document?"
            rows={4}
            required
          />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing Document...' : 'Check Safety'}
        </button>
      </form>

      {error && (
        <p className="error">
          {error}
        </p>
      )}

      {result && (
        <section
          className={`card results ${riskClass}`}
          aria-live="polite"
        >
          <h2>Safety Result</h2>

          <div className="metrics">
            <div>
              <span className="label">Risk Score</span>
              <strong>{result.riskScore}/100</strong>
            </div>

            <div>
              <span className="label">Risk Level</span>
              <strong>{result.riskLevel}</strong>
            </div>
          </div>

          <div className="block breakdown">
            <span className="label">📊 Clear Score Breakdown</span>

            <div className="breakdown-item">
              <div>
                <span>Document Sensitivity</span>
                <strong>
                  {result.breakdown.documentSensitivity}/40
                </strong>
              </div>

              <div className="breakdown-bar">
                <div
                  style={{
                    width: `${
                      (result.breakdown.documentSensitivity / 40) * 100
                    }%`,
                  }}
                />
              </div>
            </div>

            <div className="breakdown-item">
              <div>
                <span>Platform Risk</span>
                <strong>
                  {result.breakdown.platformRisk}/30
                </strong>
              </div>

              <div className="breakdown-bar">
                <div
                  style={{
                    width: `${
                      (result.breakdown.platformRisk / 30) * 100
                    }%`,
                  }}
                />
              </div>
            </div>

            <div className="breakdown-item">
              <div>
                <span>Purpose Risk</span>
                <strong>
                  {result.breakdown.purposeRisk}/30
                </strong>
              </div>

              <div className="breakdown-bar">
                <div
                  style={{
                    width: `${
                      (result.breakdown.purposeRisk / 30) * 100
                    }%`,
                  }}
                />
              </div>
            </div>

            <div className="breakdown-total">
              <span>Total</span>
              <strong>{result.riskScore}/100</strong>
            </div>
          </div>

          <div className="block">
            <span className="label">Explanation</span>
            <p>{result.explanation}</p>
          </div>

          <div className="block">
            <span className="label">Recommendation</span>
            <p>{result.recommendation}</p>
          </div>
        </section>
      )}
    </main>
  )
}

export default App