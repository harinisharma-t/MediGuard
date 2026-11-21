
import { useState } from 'react'
import './App.css'

function App() {
  const [showSearch, setShowSearch] = useState(false)
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [searched, setSearched] = useState(false)

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

  return (
    <div className="app">
      <header className="navbar">
        <h2 className="logo">MediGuard</h2>
        <nav>
          <a href="#home" onClick={(event) => {
            event.preventDefault()
            setShowSearch(false)
          }}>Home</a>
          <a href="#search" onClick={(event) => {
            event.preventDefault()
            setShowSearch(true)
          }}>Medicine Search</a>
          <a href="#about">About</a>
        </nav>
      </header>

      <main>
        {!showSearch ? (
          <section className="hero-section" id="home">
            <p className="tagline">SMARTER MEDICATION AWARENESS</p>
            <h1>Your Medication Safety,<br /><span>Our Priority.</span></h1>
            <p className="hero-description">
              Understand potential drug interactions and allergy risks
              with AI-assisted medication safety information.
            </p>
            <button className="primary-button" type="button"
              onClick={() => setShowSearch(true)}>
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
            <p>Search our database to find available medicine information.</p>

            <form className="search-form" onSubmit={handleSearch}>
              <input
                type="text"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Enter medicine name..."
                aria-label="Medicine name"
              />
              <button type="submit" disabled={loading}>
                {loading ? 'Searching...' : 'Search'}
              </button>
            </form>

            {error && <p className="error-message">{error}</p>}

            {loading && (
              <p className="loading-message">Searching the medicine database...</p>
            )}

            {searched && !loading && !error && results.length === 0 && (
              <div className="empty-message">
                <h3>No medicines found</h3>
                <p>Try another medicine name or check the spelling.</p>
              </div>
            )}

            {results.length > 0 && (
              <div className="results-section">
                <div className="results-heading">
                  <h3>Medicine Search Results</h3>
                  <span>{results.length} found</span>
                </div>

                <div className="medicine-list">
                  {results.map((medicine) => (
                    <article className="medicine-card" key={medicine.id}>
                      <div className="medicine-card-header">
                        <div>
                          <p className="medicine-label">MEDICINE</p>
                          <h3>{medicine.generic_name}</h3>
                        </div>
                        <span className="medicine-id">ID: {medicine.id}</span>
                      </div>

                      <div className="medicine-details">
                        <div>
                          <span>Brand Name</span>
                          <strong>{medicine.brand_name || 'Not available'}</strong>
                        </div>
                        <div>
                          <span>Active Ingredient</span>
                          <strong>{medicine.active_ingredient || 'Not available'}</strong>
                        </div>
                      </div>
                    </article>
                  ))}
                </div>

                <p className="results-note">
                  These results are based on the medicines available in the
                  MediGuard database. Missing information does not mean a
                  medicine is safe or risk-free.
                </p>
              </div>
            )}

            <button className="primary-button back-button" type="button"
              onClick={() => {
                setShowSearch(false)
                setError('')
              }}>
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
