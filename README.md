# ⚖️ Gramin-Nyaya: Premium AI Legal Assistant (Offline)

**Gramin-Nyaya** (Rural Justice) is an offline-first, privacy-preserving Single Page Application (SPA) designed to bridge the legal information gap for rural populations in India. By leveraging a local vector store and offline LLM orchestration, the system provides grounded, simplified legal guidance from the **Registration Act, 1908** in high-quality **Hindi** and **English**.

---

## 📸 Redesigned UI/UX Showcase
The platform has been completely overhauled with a state-of-the-art dark theme, premium gold branding accents, and clean layout cards, designed strictly to replicate accessible, village-friendly terminal interfaces.

### 🌟 Key Enhancements
* **Unified Single Page Application**: Seamlessly switch between the **Landing Hero Page**, **Legal Knowledge Library**, and **AI Assistant Chat Panel** without page refreshes.
* **Instant Dual-Language Support (HI / EN)**: Fully functional localization toggle which instantly swaps all headings, categories, prompts, recent queries, search placeholders, and context panels between Hindi and English.
* **Smart Voice Integration**:
  - **Speech-to-Text (STT)**: Microphone voice typing button with live recording effects, mapping to `hi-IN` and `en-US` depending on your selected language.
  - **Text-to-Speech (TTS)**: Clean audio narration reading legal advice aloud using appropriate local pitch and speed parameters.
* **Intelligent Vector store Persistency**: Optimized loading checkpoints which skip costly CPU document re-embeddings on restart if a persistent index already exists, reducing boot time to **under 1 second**.
* **Zero Cloud/API Dependencies**: Runs entirely offline on local hardware via Ollama and sentence-transformers. No user data ever leaves the device—ensuring absolute privacy and compliance.

---

## 📂 Project Structure

```text
Gramin-Nyaya/
├── legal_docs/             # Statutory Source PDF (Registration Act 1908 in Hindi)
├── chroma_db/              # Compiled offline vector collections checkpoint
├── api.py                  # Humanized FastAPI Backend Gateway
├── rag_logic.py            # Optimized RAG context search & LLM Orchestration
├── stt_service.py          # Voice Speech-to-Text transcription library
├── gramin_nyaya_main.py    # Command-line diagnostics tool
├── index.html              # Redesigned Single Page App Kiosk Interface
├── requirements.txt        # Local python dependency list
└── README.md               # Product documentation
```

---

## 🛠️ Technical Stack
* **Frontend**: Vanilla HTML5, premium CSS3 (featuring Google Fonts *Outfit* & *Inter*), and humanized JavaScript.
* **Backend**: FastAPI (Python 3.10+) with robust error-handling mechanisms.
* **Embeddings**: HuggingFace Multilingual-MiniLM-L12-v2.
* **Vector Store**: ChromaDB.
* **Local LLM**: Dual-model RAG orchestration via Ollama:
  - **DeepSeek-R1 (1.5B)**: Precision factual researcher agent (configured with temperature `0.0`).
  - **Qwen 2.5 (1.5B)**: Communicator agent localized for conversational rural dialect styling (configured with temperature `0.1`).

---

## 🚀 Setting Up Locally

### Prerequisites
1. Install [Ollama](https://ollama.com/) on your local machine.
2. Pull both required local language models:
   ```bash
   ollama pull deepseek-r1:1.5b
   ollama pull qwen2.5:1.5b
   ```

### Installation
1. Navigate to the project directory:
   ```bash
   cd D:\antigravity\gramin-nyaya
   ```
2. Set up your virtual environment and install packages:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Platform
1. **Boot the API Server**:
   ```bash
   python api.py
   ```
   The backend will check for existing Chroma vectors, automatically ingest the source legal PDF if necessary, and start the local API gateway at `http://localhost:8000`.

2. **Launch the Kiosk Interface**:
   Simply open **`index.html`** in your favorite browser. Click **"शुरू करें"** or **"Get Started"** to explore the offline legal assistant!
