# Gramin-Nyaya: Offline AI Legal Assistant

Gramin-Nyaya is a voice-interactive Agentic RAG (Retrieval-Augmented Generation) system designed to help rural citizens navigate the **Registration Act of 1908** in Hindi. 

### Key Features:
*   **Voice-to-Voice Interface**: Integrated with `Faster-Whisper` for high-accuracy Hindi speech recognition.
*   **Local & Secure**: Powered by `Qwen 2.5 (1.5B)` via Ollama, ensuring all legal data stays 100% offline.
*   **Accurate Legal Retrieval**: Uses `ChromaDB` and `LangChain` to search specific sections of the Registration Act.
*   **Hardware Optimized**: Designed to run efficiently on the **NVIDIA Jetson Orin Nano**.

### Setup:
1. Install dependencies: `pip install -r requirements.txt`
2. Run Ollama and pull the model: `ollama pull qwen2.5:1.5b`
3. Launch the app: `python gramin_nyaya_main.py`
