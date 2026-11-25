import { useState } from 'react'
import './App.css'

function App() {
  const [showSearch, setShowSearch] = useState(false)

  const [query, setQuery] = useState('')
  const [medicines, setMedicines] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchError, setSearchError] = useState('')
  const [searched, setSearched] = useState(false)

  const [drugA, setDrugA] = useState('')
  const [drugB, setDrugB] = useState('')
  const [explanation, setExplanation] = useState(null)
  const [interactionLoading, setInteractionLoading] = useState(false)
  const [interactionError, setInteractionError] = useState('')

  async function handleSearch(event) {
    event.preventDefault()

    if (!query.trim()) {
      setSearchError('Please enter a medicine name.')
      return
    }

    setLoading(true)
    setSearchError('')
    setMedicines([])
    setSearched(false)

    try {
      const response = await fetch(
        `/api/drugs/search?query=${encodeURIComponent(query.trim())}`
      )

      if (!response.ok) {
        throw new Error('Unable to search medicines. Please try again.')
      }

      const data = await response.json()

      const results = Array.isArray(data)
        ? data
        : data.results || data.medicines || []

      setMedicines(results)
      setSearched(true)
    } catch (error) {
      setSearchError(error.message || 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  function selectMedicine(medicine, field) {
    const medicineName = medicine.generic_name || medicine.brand_name

    if (field === 'first') {
      setDrugA(medicineName)
    } else {
      setDrugB(medicineName)
    }

    setInteractionError('')
    setExplanation(null)
  }

  async function handleExplain(event) {
    event.preventDefault()

    if (!drugA.trim() || !drugB.trim()) {
      setInteractionError('Please enter both medicine names.')
      return
    }


    if (drugA.trim().toLowerCase() === drugB.trim().toLowerCase()) {
  setInteractionError('Please select two different medicines.')
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
        throw new Error(data.detail || 'Unable to check interaction.')
      }

      setExplanation(data)
    } catch (error) {
      setInteractionError(error.message || 'Something went wrong.')
    } finally {
      setInteractionLoading(false)
    }
  }

  return (
    <div className="app">
      <nav className="navbar">
        <div className="logo">MediGuard</div>

        <div className="nav-links">
          <button type="button" onClick={() => setShowSearch(false)}>
            Home
          </button>

          <button type="button" onClick={() => setShowSearch(true)}>
            Medicine Search
          </button>

          <a href="#about">About</a>
        </div>
      </nav>

      {!showSearch ? (
        <section className="hero-section">
          <h1>Your Medicines. Your Safety.</h1>

          <p className="tagline">
            Understand possible medicine interactions and make
            more informed healthcare decisions.
          </p>

          <p className="hero-description">
            MediGuard is an AI-assisted medicine safety application
            that helps you explore medicine information and possible
            drug interactions.
          </p>

          <button
            className="primary-button"
            type="button"
            onClick={() => setShowSearch(true)}
          >
            Get Started
          </button>

          <p className="disclaimer">
            Educational decision-support tool. Not a substitute
            for professional medical advice.
          </p>
        </section>
      ) : (
        <main className="search-section">
          <h1>Medicine Safety Checker</h1>

          <p>
            Search for a medicine and select medicines to check
            their possible interactions.
          </p>

          <form className="search-form" onSubmit={handleSearch}>
            <input
              type="text"
              placeholder="Enter medicine name..."
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              disabled={loading}
            />

            <button
              className="primary-button"
              type="submit"
              disabled={loading}
            >
              {loading ? 'Searching...' : 'Search Medicine'}
            </button>
          </form>

          {loading && (
            <p className="loading-message" role="status">
              Searching medicines...
            </p>
          )}

          {searchError && (
            <p className="error-message" role="alert">
              {searchError}
            </p>
          )}

          {searched && medicines.length === 0 && !searchError && (
            <p className="empty-message">
              No medicines found. Try another medicine name.
            </p>
          )}

          {medicines.length > 0 && (
            <section className="results-section">
              <h2>Search Results</h2>

              <div className="medicine-list">
                {medicines.map((medicine) => (
                  <div className="medicine-card" key={medicine.id}>
                    <h3>
                      {medicine.brand_name || medicine.generic_name}
                    </h3>

                    <p>
                      <strong>Generic Name:</strong>{' '}
                      {medicine.generic_name || 'Not available'}
                    </p>

                    <p>
                      <strong>Brand Name:</strong>{' '}
                      {medicine.brand_name || 'Not available'}
                    </p>

                    <p>
                      <strong>Active Ingredient:</strong>{' '}
                      {medicine.active_ingredient || 'Not available'}
                    </p>

                    <div className="medicine-actions">
                      <button
                        className="primary-button"
                        type="button"
                        onClick={() => selectMedicine(medicine, 'first')}
                      >
                        Use as First Medicine
                      </button>

                      <button
                        className="primary-button"
                        type="button"
                        onClick={() => selectMedicine(medicine, 'second')}
                      >
                        Use as Second Medicine
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          <section className="interaction-section">
            <h2>AI Interaction Explanation</h2>

            <p>
              Enter two medicines or select them directly from
              the search results above.
            </p>

            <form className="search-form" onSubmit={handleExplain}>
              <input
                type="text"
                placeholder="First medicine"
                value={drugA}
                onChange={(event) => setDrugA(event.target.value)}
                disabled={interactionLoading}
              />

              <input
                type="text"
                placeholder="Second medicine"
                value={drugB}
                onChange={(event) => setDrugB(event.target.value)}
                disabled={interactionLoading}
              />

              <button
                className="primary-button"
                type="submit"
                disabled={interactionLoading}
              >
                {interactionLoading ? 'Checking...' : 'Check Interaction'}
              </button>
            </form>

            {interactionLoading && (
              <p className="loading-message" role="status">
                Checking medicine interaction...
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

                <p>
                  <strong>Medicine 1:</strong> {explanation.drug_a}
                </p>

                <p>
                  <strong>Medicine 2:</strong> {explanation.drug_b}
                </p>

                <p>
                  <strong>Interaction:</strong>{' '}
                  {explanation.interaction?.message ||
                    'No interaction information available.'}
                </p>

                <h3>AI Explanation</h3>

                <p>{explanation.explanation}</p>

                <p>
                  <strong>Provider:</strong> {explanation.provider}
                </p>

                <p>
                  <strong>Fallback Used:</strong>{' '}
                  {String(explanation.used_fallback)}
                </p>

                <p className="disclaimer">
                  {explanation.disclaimer}
                </p>
              </div>
            )}
          </section>

          <button
            className="primary-button"
            type="button"
            onClick={() => setShowSearch(false)}
          >
            Back to Home
          </button>
        </main>
      )}

      <section className="about-section" id="about">
        <h2>About MediGuard</h2>

        <p>
          MediGuard is an AI-assisted medicine safety project
          designed to help users explore medicine information,
          possible drug interactions, and safety explanations.
        </p>

        <p className="disclaimer">
          MediGuard is for educational purposes only. Always
          consult a qualified healthcare professional before
          making medication decisions.
        </p>
      </section>

      <footer>
        <p>© 2026 MediGuard. Educational use only.</p>
      </footer>
    </div>
  )
}

export default App