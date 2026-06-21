import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css';

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  const askAI = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
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

  return (
    <div className="app-container">
      <header className="header">
        <h1>ग्रामीण न्याय (Gramin-Nyaya)</h1>
        <p>आपका डिजिटल कानूनी सहायक</p>
      </header>

      <main className="main-card">
        <section className="query-section" aria-labelledby="query-heading">
          <h2 id="query-heading" className="section-title">कानूनी सवाल पूछें</h2>

          <label className="input-label" htmlFor="legal-question">
            अपना सवाल यहाँ लिखें:
          </label>

          <textarea
            id="legal-question"
            className="text-area"
            placeholder="जैसे: रजिस्ट्री के लिए क्या चाहिए?"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />

          <button
            onClick={askAI}
            disabled={loading || !question.trim()}
            className="submit-btn"
          >
            {loading ? "सोच रहा हूँ..." : "जवाब जानें"}
          </button>
        </section>

        <section className="facts-section" aria-labelledby="facts-heading">
          <h2 id="facts-heading" className="section-title">परियोजना तथ्य</h2>
          <dl className="facts-list">
            <div>
              <dt>Author:</dt>
              <dd>Kkushak16, project creator and AI/RAG application developer.</dd>
            </div>
            <div>
              <dt>Legal source:</dt>
              <dd>Registration Act, 1908 source documents included in this repository.</dd>
            </div>
            <div>
              <dt>Review status:</dt>
              <dd>Legal information only; important matters should be checked by a qualified legal professional.</dd>
            </div>
          </dl>
        </section>

        {answer && (
          <section className="answer-box" aria-live="polite" aria-labelledby="answer-heading">
            <h2 id="answer-heading" className="answer-title">कानूनी परामर्श:</h2>
            <div className="answer-content">
              <ReactMarkdown>{answer}</ReactMarkdown>
            </div>
          </section>
        )}
      </main>

      <footer className="footer">
        © 2026 ग्रामीण न्याय परियोजना | कानूनी जानकारी के लिए सुरक्षित
      </footer>
    </div>
  );
}

export default App;
