# ⚡ NexusAI — Multi-Persona Intelligent Chatbot

> **μLearn Task**: Build a Simple Chatbot ⭐ **250 Karma Points**  
> **Hashtag**: `#cl-ai-chatbot` | **Domain**: Artificial Intelligence  

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Google GenAI](https://img.shields.io/badge/LLM-Google%20Gemini-4285F4.svg)](https://aistudio.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Overview

**NexusAI** is an adaptive, multi-persona conversational AI web application engineered with **Python**, **Streamlit**, and the state-of-the-art **Google Gemini GenAI SDK**. 

Unlike rigid or single-purpose chatbots, NexusAI provides dynamically tailored AI assistants with distinct system architectures, customizable creativity levels (temperature), multi-source API credential management, interactive starter prompts, real-time token streaming, and session export capabilities.

---

## 💡 What Makes NexusAI Unique?

| Feature | NexusAI | Conventional Basic Chatbots |
| :--- | :--- | :--- |
| **Multi-Persona Engine** | 4 specialized personas (Tutor, Senior Engineer, Ideator, Companion) | Single static prompt |
| **Model Selection** | Support for `gemini-3.6-flash` & `gemini-2.0-flash` | Hardcoded single model |
| **Streaming UX** | Real-time token streaming (`st.write_stream`) | Buffering / waiting delay |
| **Credential Flexibility** | Streamlit Secrets + `.env` + Direct in-app secure input | Crash on missing config |
| **Offline / Demo Mode** | Simulated intelligent fallback for instant evaluator testing | Crashes if no API key is supplied |
| **Quick Starters** | Dynamic one-click prompt chips per persona | Empty screen on start |
| **Session Control** | 1-click Markdown transcript export & conversation reset | No export option |

---

## 🎭 Persona System

NexusAI adapts its cognitive framing, tone, and formatting depending on the chosen persona:

1. **🎓 Academic Tutor (`Prof. Isaac`)**:
   - Specializes in breaking down complex concepts in computer science, mathematics, and science using intuitive analogies and ELI5 explanations.
   - Ends responses with reinforcement questions to solidify learning.

2. **💻 Senior Code Architect (`DevForge`)**:
   - Focuses on production-grade code, clean architecture, debugging, algorithmic efficiency (Big-O analysis), and best practices.

3. **💡 Creative Ideator (`Spark`)**:
   - High-energy brainstormer for startup ideas, storytelling, naming, copy, and cross-disciplinary innovation.

4. **🌟 Friendly Life Companion (`Aura`)**:
   - Empathetic conversational partner for mindfulness, study motivation, daily reflection, and stress management.

---

## 🚀 Quickstart & Local Setup

Follow these steps to run NexusAI locally on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/gauthamkrishnars/chatbot.git
cd chatbot
```

### 2. Create and Activate a Virtual Environment
- **Windows**:
  ```powershell
  python -m venv .venv
  .venv\Scripts\activate
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Your Gemini API Key *(Optional but Recommended)*
You can acquire a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

Choose any of the following methods:
- **Option A (Environment Variable)**:
  Copy `.env.example` to `.env` and set your key:
  ```env
  GEMINI_API_KEY=AIzaSyYourKeyHere...
  ```
- **Option B (Streamlit Secrets)**:
  Create `.streamlit/secrets.toml`:
  ```toml
  GEMINI_API_KEY = "AIzaSyYourKeyHere..."
  ```
- **Option C (In-App Sidebar)**:
  Launch the app directly and paste your key into the sidebar password field.

*(Note: If no API key is provided, NexusAI automatically runs in **Offline Demo Mode**, allowing you to explore the interface and sample responses without errors!)*

### 5. Launch the Application
```bash
streamlit run app.py
```
The interface will automatically open in your browser at `http://localhost:8501`.

---

---

## 🛠️ Tech Stack & Architecture

- **Frontend / Framework**: [Streamlit](https://streamlit.io/) (modern reactive chat components)
- **Language**: Python 3.10+
- **LLM Provider**: [Google GenAI SDK](https://github.com/google-gemini/generative-ai-python) (`google-genai`)
- **Supported Models**: `gemini-3.6-flash` (default), `gemini-2.0-flash`
- **Configuration & Security**: `python-dotenv`, Streamlit session secrets, client-side session state isolation

---

## 🧠 Creative Process & Challenges

### Creative Approach
Our goal was to design a chatbot that goes beyond the standard "single prompt question-and-answer box". We wanted an assistant that can accompany a user throughout their entire workflow—whether they are learning theoretical foundations as a student, writing code as a developer, brainstorming product ideas, or taking a mental break.

### Challenges Faced & Solutions
1. **Handling Missing API Keys Gracefully**:
   - *Challenge*: Most chatbot apps crash immediately or produce unhandled exceptions if the user has not configured API secrets.
   - *Solution*: Implemented a fallback cascading lookup (`Sidebar Input` -> `st.secrets` -> `.env`) coupled with an **Offline / Simulated Demo Mode** so reviewers can test the UI without getting blocked.
2. **Context Retention Across Conversations**:
   - *Challenge*: Maintaining coherent multi-turn conversation memory without token bloat or context fragmentation.
   - *Solution*: Formatted conversation history using the `google.genai.types.Content` schema and tied it to Streamlit's `st.session_state`.
3. **Response Latency & User Experience**:
   - *Challenge*: Long LLM responses can feel sluggish if buffered entirely before rendering.
   - *Solution*: Implemented token streaming with `client.models.generate_content_stream()` and `st.write_stream()`, offering instant visual feedback.

---

## 📦 Deliverables & μLearn Submission Checklist

- [x] Complete source code in public GitHub repository
- [x] Comprehensive documentation in `README.md`
- [x] Interactive web interface with Streamlit
- [x] Support for generative AI models + fallback handling
- [x] Ready for Discord submission:

```text
Task: Build a Simple Chatbot
Hashtag: #cl-ai-chatbot
Repository: https://github.com/gauthamkrishnars/chatbot
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
