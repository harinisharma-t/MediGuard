
import { useState } from 'react'
import './App.css'

function App() {
  const [showSearch, setShowSearch] = useState(false)
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [searched, setSearched] = useState(false)

  const [drugA, setDrugA] = useState('')
  const [drugB, setDrugB] = useState('')
  const [explanation, setExplanation] = useState(null)
  const [interactionLoading, setInteractionLoading] = useState(false)
  const [interactionError, setInteractionError] = useState('')

  async function handleSearch(event) {
    event.preventDefault()

    if (!query.trim()) {
      setError('Please enter a medicine name.')
      setResults([])
      setSearched(false)
      return
    }

    setLoading(true)
    setError('')
    setResults([])
    setSearched(true)

    try {
      const response = await fetch(
        `/api/drugs/search?query=${encodeURIComponent(query.trim())}`
      )
      const data = await response.json()

      if (!response.ok) {
        throw new Error('Search failed')
      }

      setResults(data.results || [])
    } catch {
      setError('Unable to connect to the medicine database. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  async function handleExplain(event) {
    event.preventDefault()

    if (!drugA.trim() || !drugB.trim()) {
      setInteractionError('Please enter both medicine names.')
      setExplanation(null)
      return
    }

    setInteractionLoading(true)
    setInteractionError('')
    setExplanation(null)

    try {
      const response = await fetch('/api/interactions/explain', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          drug_a: drugA.trim(),
          drug_b: drugB.trim(),
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error('Unable to generate explanation.')
      }

      setExplanation(data)
    } catch {
      setInteractionError(
        'Unable to check the interaction. Please try again.'
      )
    } finally {
      setInteractionLoading(false)
    }
  }

  function selectFirstMedicine(medicine) {
    setDrugA(medicine.generic_name)
    setInteractionError('')
    setExplanation(null)
  }

  return (
    <div className="app">
      <header className="navbar">
        <h2 className="logo">MediGuard</h2>
        <nav>
          <a href="#" onClick={(e) => {
            e.preventDefault()
            setShowSearch(false)
          }}>Home</a>
          <a href="#" onClick={(e) => {
            e.preventDefault()
            setShowSearch(true)
          }}>Medicine Search</a>
          <a href="#about">About</a>
        </nav>
      </header>

      <main>
        {!showSearch ? (
          <section className="hero-section" id="home">
            <p className="tagline">SMARTER MEDICATION AWARENESS</p>
            <h1>
              Your Medication Safety,
              <br />
              <span>Our Priority.</span>
            </h1>
            <p className="hero-description">
              Understand potential drug interactions and allergy risks
              with AI-assisted medication safety information.
            </p>
            <button
              className="primary-button"
              type="button"
              onClick={() => setShowSearch(true)}
            >
              Get Started
            </button>
            <p className="disclaimer">
              Educational support only. Not a substitute for professional
              medical advice.
            </p>
          </section>
        ) : (
          <section className="search-section" id="search">
            <h2>Medicine Search</h2>
            <p>
              Search our database to find available medicine information.
            </p>

            <form className="search-form" onSubmit={handleSearch}>
              <input
                type="text"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Enter medicine name..."
                aria-label="Medicine name"
                disabled={loading}
              />
              <button type="submit" disabled={loading}>
                {loading ? 'Searching...' : 'Search'}
              </button>
            </form>

            {loading && (
              <p className="loading-message" role="status">
                Searching the medicine database. Please wait...
              </p>
            )}

            {error && <p className="error-message" role="alert">{error}</p>}

            {searched && !loading && !error && results.length === 0 && (
              <p className="empty-message">
                No matching medicines found in the database. Try another name.
              </p>
            )}

            {results.length > 0 && (
              <div className="results-section">
                <h3>Search Results ({results.length})</h3>
                <div className="medicine-list">
                  {results.map((medicine) => (
                    <div className="medicine-card" key={medicine.id}>
                      <h3>{medicine.generic_name}</h3>
                      <p>
                        <strong>Brand Name:</strong>{' '}
                        {medicine.brand_name || 'Not available'}
                      </p>
                      <p>
                        <strong>Active Ingredient:</strong>{' '}
                        {medicine.active_ingredient || 'Not available'}
                      </p>
                      <button
                        className="primary-button"
                        type="button"
                        onClick={() => selectFirstMedicine(medicine)}
                      >
                        Use as First Medicine
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="results-section">
              <h2>AI Interaction Explanation</h2>
              <p>
                Enter two medicine names to check available interaction
                information and receive an easy-to-understand explanation.
              </p>

              <form className="search-form" onSubmit={handleExplain}>
                <input
                  type="text"
                  value={drugA}
                  onChange={(event) => setDrugA(event.target.value)}
                  placeholder="First medicine name"
                  aria-label="First medicine name"
                  disabled={interactionLoading}
                />
                <input
                  type="text"
                  value={drugB}
                  onChange={(event) => setDrugB(event.target.value)}
                  placeholder="Second medicine name"
                  aria-label="Second medicine name"
                  disabled={interactionLoading}
                />
                <button type="submit" disabled={interactionLoading}>
                  {interactionLoading ? 'Checking...' : 'Check Interaction'}
                </button>
              </form>

              {interactionLoading && (
                <p className="loading-message" role="status">
                  Checking available interaction information. Please wait...
                </p>
              )}

              {interactionError && (
                <p className="error-message" role="alert">
                  {interactionError}
                </p>
              )}

              {explanation && (
                <div className="medicine-card">
                  <h3>Interaction Result</h3>
                  <p><strong>Medicine 1:</strong> {explanation.drug_a}</p>
                  <p><strong>Medicine 2:</strong> {explanation.drug_b}</p>
                  <p>
                    <strong>Database Result:</strong>{' '}
                    {explanation.interaction?.message || 'No details available'}
                  </p>
                  <p><strong>Explanation:</strong></p>
                  <p>{explanation.explanation}</p>
                  <p>
                    <strong>Explanation Provider:</strong> {explanation.provider}
                  </p>
                  {explanation.used_fallback && (
                    <p>
                      Rule-based explanation used because AI service was unavailable.
                    </p>
                  )}
                  <p className="disclaimer">{explanation.disclaimer}</p>
                </div>
              )}
            </div>

            <button
              className="primary-button"
              type="button"
              onClick={() => setShowSearch(false)}
            >
              Back to Home
            </button>
          </section>
        )}

        <section className="about-section" id="about">
          <h2>About MediGuard</h2>
          <p>
            MediGuard helps patients and caregivers understand potential
            medication risks by checking drug interactions and recorded allergies.
          </p>
        </section>
      </main>

      <footer>
        <p>© 2026 MediGuard | Medication Safety Awareness</p>
      </footer>
    </div>
  )
}

export default App
