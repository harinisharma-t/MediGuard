
import './App.css'

function App() {
  return (
    <div className="app">
      <header className="navbar">
        <h2 className="logo">MediGuard</h2>

        <nav>
          <a href="#home">Home</a>
          <a href="#about">About</a>
        </nav>
      </header>

      <main>
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

          <button className="primary-button" type="button">
            Get Started
          </button>

          <p className="disclaimer">
            Educational support only. Not a substitute for professional
            medical advice.
          </p>
        </section>

        <section className="about-section" id="about">
          <h2>About MediGuard</h2>
          <p>
            MediGuard helps patients and caregivers understand
            potential medication risks by checking drug interactions
            and recorded allergies.
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
