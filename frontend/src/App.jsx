import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css';

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [serverStatus, setServerStatus] = useState("checking");

  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  // Check connection to the backend server
  const checkStatus = async () => {
    try {
      const controller = new AbortController();
      const id = setTimeout(() => controller.abort(), 3000);
      
      // Ping backend (even a 404 or 405 response indicates the backend is active)
      await fetch(`${API_URL}/ask`, {
        method: "OPTIONS",
        signal: controller.signal
      });
      
      clearTimeout(id);
      setServerStatus("online");
    } catch (error) {
      setServerStatus("offline");
    }
  };

  useEffect(() => {
    checkStatus();
    const interval = setInterval(checkStatus, 10000);
    return () => clearInterval(interval);
  }, []);

  const askAI = async (overrideQuestion) => {
    const q = overrideQuestion || question;
    if (!q.trim()) return;

    setLoading(true);
    setAnswer("");

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setAnswer(data.answer);
    } catch (error) {
      console.error("Fetch error:", error);
      setAnswer("क्षमा करें, सर्वर से जुड़ने में समस्या हो रही है। कृपया जांचें कि backend चल रहा है।");
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (suggestionText) => {
    setQuestion(suggestionText);
    askAI(suggestionText);
  };

  return (
    <div className="app-container">
      {/* Sleek Top Navigation Bar */}
      <nav className="navbar">
        <div className="nav-brand">
          <img src="/logo.webp" alt="Gramin-Nyaya Logo" className="nav-logo" />
          <div className="nav-title-group">
            <h1 className="nav-title">ग्रामीण न्याय (Gramin-Nyaya)</h1>
            <p className="nav-subtitle">Legal Aid Society</p>
          </div>
        </div>

        <button 
          className="nav-menu-toggle" 
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          aria-label="Toggle navigation menu"
        >
          ☰
        </button>

        <ul className={`nav-menu ${isMenuOpen ? 'mobile-open' : ''}`}>
          <li><a href="/" className="nav-link">मुख्य पृष्ठ</a></li>
          <li><a href="/about.html" className="nav-link">हमारे बारे में</a></li>
          <li><a href="/contact.html" className="nav-link">संपर्क करें</a></li>
          <li><a href="/privacy.html" className="nav-link">गोपनीयता नीति</a></li>
          <li><a href="/terms.html" className="nav-link">सेवा की शर्तें</a></li>
          <li>
            <div className="api-status-badge">
              <span className={`status-dot ${serverStatus === 'online' ? 'status-online' : 'status-offline'}`}></span>
              {serverStatus === 'online' ? 'सक्रिय (Online)' : 'अक्रिय (Offline)'}
            </div>
          </li>
        </ul>
      </nav>

      {/* Hero Header */}
      <header className="hero-header">
        <h1>ग्रामीण न्याय सहायक</h1>
        <p>Offline, Privacy-First AI Legal Assistant</p>
      </header>

      {/* Main Grid Layout */}
      <div className="grid-container">
        {/* Left Column: Ask card, suggestions, answer */}
        <main className="glass-card main-card">
          <section className="query-section" aria-labelledby="query-heading">
            <h2 id="query-heading" className="section-title">
              ⚖️  कानूनी सवाल पूछें
            </h2>

            <label className="input-label" htmlFor="legal-question" style={{ marginTop: '1rem' }}>
              अपना सवाल यहाँ लिखें (पंजीकरण अधिनियम, 1908 के बारे में):
            </label>

            <textarea
              id="legal-question"
              className="text-area"
              placeholder="जैसे: रजिस्ट्री कराने की समय सीमा क्या है?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />

            <button
              onClick={() => askAI()}
              disabled={loading || !question.trim()}
              className="submit-btn"
              id="ask-submit-btn"
            >
              {loading ? "सोच रहा हूँ..." : "जवाब जानें"}
            </button>
          </section>

          {/* Quick-Question Cards */}
          <section className="suggestions-section">
            <label className="input-label">त्वरित विकल्प चुनें (Quick Templates):</label>
            <div className="suggestions-grid">
              <div 
                className="suggestion-card" 
                onClick={() => handleSuggestionClick("रजिस्ट्री कराने की समय सीमा क्या है?")}
              >
                <h4>रजिस्ट्री समय सीमा</h4>
                <p>विक्रय विलेख (Sale Deed) की रजिस्ट्री के लिए समय सीमा जानें।</p>
              </div>
              <div 
                className="suggestion-card" 
                onClick={() => handleSuggestionClick("दाखिल-खारिज (Mutation) कराने की प्रक्रिया क्या है?")}
              >
                <h4>दाखिल-खारिज प्रक्रिया</h4>
                <p>रजिस्ट्री के बाद राजस्व अभिलेखों में नाम चढ़ाने की विधि।</p>
              </div>
              <div 
                className="suggestion-card" 
                onClick={() => handleSuggestionClick("रजिस्ट्री न कराने के क्या परिणाम हैं?")}
              >
                <h4>अनिवार्य पंजीकरण</h4>
                <p>पंजीकरण न कराने पर संपत्ति की कानूनी वैधता पर प्रभाव।</p>
              </div>
              <div 
                className="suggestion-card" 
                onClick={() => handleSuggestionClick("पारिवारिक संपत्ति के बंटवारे की रजिस्ट्री का क्या नियम है?")}
              >
                <h4>परिवार बंटवारा</h4>
                <p>क्या बंटवारा विलेख का पंजीकरण कराना आवश्यक है?</p>
              </div>
            </div>
          </section>

          {/* Answer Area */}
          {answer && (
            <section className="answer-box" aria-live="polite" aria-labelledby="answer-heading">
              <h2 id="answer-heading" className="answer-title">
                📖  कानूनी परामर्श:
              </h2>
              <div className="answer-content">
                <ReactMarkdown>{answer}</ReactMarkdown>
              </div>
            </section>
          )}
        </main>

        {/* Right Column: Settings & Project Facts sidebar */}
        <aside className="sidebar">
          {/* Settings & Active Status Card */}
          <section className="glass-card settings-panel">
            <h3 className="section-title">🖥️  सिस्टम स्थिति (Settings)</h3>
            <div className="settings-row">
              <span className="settings-label">सक्रिय मॉडल:</span>
              <span className="settings-value"><span className="badge-saffron">DeepSeek-R1 (Local)</span></span>
            </div>
            <div className="settings-row">
              <span className="settings-label">स्थानीय डेटाबेस:</span>
              <span className="settings-value">Chroma DB (LlamaIndex)</span>
            </div>
            <div className="settings-row">
              <span className="settings-label">अधिकार क्षेत्र:</span>
              <span className="settings-value">Registration Act, 1908</span>
            </div>
            <div className="settings-row">
              <span className="settings-label">सुरक्षा स्तर:</span>
              <span className="settings-value" style={{ color: '#10b981' }}>✓ 100% Offline (Private)</span>
            </div>
          </section>

          {/* Project Facts Cards */}
          <section className="glass-card facts-panel">
            <h3 className="section-title">📋  परियोजना तथ्य</h3>
            <div className="facts-grid" style={{ marginTop: '1rem' }}>
              <div className="fact-item">
                <div className="fact-title">Author</div>
                <div className="fact-desc">Kkushak16, project creator and AI/RAG application developer.</div>
              </div>
              <div className="fact-item">
                <div className="fact-title">Legal Source</div>
                <div className="fact-desc">Registration Act, 1908 source documents included in this repository.</div>
              </div>
              <div className="fact-item">
                <div className="fact-title">Review Status</div>
                <div className="fact-desc">Legal information only; important matters should be checked by a qualified legal professional.</div>
              </div>
            </div>
          </section>
        </aside>
      </div>

      {/* Sleek Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-logo-section">
            <div className="footer-brand">ग्रामीण न्याय <span>(Gramin-Nyaya)</span></div>
            <div className="footer-desc">ग्रामीण भारत के लिए नि:शुल्क ऑफलाइन डिजिटल कानूनी साक्षरता मंच</div>
          </div>
          <div className="footer-links">
            <a href="/about.html">हमारे बारे में</a>
            <a href="/contact.html">संपर्क करें</a>
            <a href="/privacy.html">गोपनीयता नीति</a>
            <a href="/terms.html">सेवा की शर्तें</a>
          </div>
        </div>
        <div className="footer-copy">
          © 2026 ग्रामीण न्याय परियोजना | DLSA द्वारा सत्यापित एवं कानूनी संदर्भ के लिए सुरक्षित
        </div>
      </footer>
    </div>
  );
}

export default App;
