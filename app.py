import os
import time
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv

# Load local .env if available
load_dotenv()

# -----------------------------------------------------------------------------
# Streamlit Page Configuration & Modern Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NexusAI | Multi-Persona Chatbot",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished, responsive aesthetic
st.markdown("""
<style>
    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #94A3B8;
        font-size: 1.05rem;
        margin-bottom: 1.2rem;
    }
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-persona {
        background-color: #312E81;
        color: #C7D2FE;
        border: 1px solid #4338CA;
    }
    .badge-model {
        background-color: #064E3B;
        color: #A7F3D0;
        border: 1px solid #059669;
    }
    .badge-status {
        background-color: #1E293B;
        color: #94A3B8;
        border: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Personas & System Prompts Configuration
# -----------------------------------------------------------------------------
PERSONAS = {
    "🎓 Academic Tutor (Prof. Isaac)": {
        "id": "tutor",
        "avatar": "🎓",
        "title": "Professor Isaac - Concept Explainer",
        "description": "Explains complex ideas with intuitive analogies, structured breakdowns, and ELI5 clarity.",
        "system_prompt": (
            "You are Professor Isaac, an elite academic tutor and intuitive educator. "
            "Your mission: make any complex concept crystal clear for learners. "
            "Guidelines:\n"
            "- Use vivid, intuitive real-world analogies (explain like I'm 5 when helpful).\n"
            "- Structure long explanations into numbered steps or bite-sized sections.\n"
            "- Provide concise, practical examples.\n"
            "- End your response with a quick, friendly thought-provoking question to reinforce learning.\n"
            "- Maintain an encouraging, patient, and intellectually curious demeanor."
        ),
        "starter_prompts": [
            "Explain Quantum Computing using a simple analogy.",
            "How does recursion work in programming? (ELI5)",
            "What is Big-O notation and why do developers care?",
            "Explain how Transformers and Attention mechanisms work."
        ]
    },
    "💻 Senior Code Architect (DevForge)": {
        "id": "code",
        "avatar": "💻",
        "title": "DevForge - Senior Software Architect",
        "description": "Writes production-grade code, squashes bugs, and teaches architectural best practices.",
        "system_prompt": (
            "You are DevForge, a pragmatic Principal Software Engineer and coding mentor. "
            "Your mission: deliver clean, modular, production-grade code and debug complex problems. "
            "Guidelines:\n"
            "- Always format code in fenced markdown blocks with explicit language tags.\n"
            "- Provide brief, actionable explanations of logic and design patterns.\n"
            "- Highlight time/space complexity, edge cases, and security considerations.\n"
            "- Recommend modern best practices, idiomatic patterns, and testability.\n"
            "- Keep fluff to a minimum; be direct, technical, and precise."
        ),
        "starter_prompts": [
            "Write an idiomatic Python script to process a REST API with error handling.",
            "Explain the difference between SQL and NoSQL with a trade-off matrix.",
            "How do I optimize database queries and avoid the N+1 problem?",
            "Review this concept: implementing Clean Architecture in Python."
        ]
    },
    "💡 Creative Ideator (Spark)": {
        "id": "creative",
        "avatar": "💡",
        "title": "Spark - Innovation & Writing Partner",
        "description": "Sparks out-of-the-box ideas, catchy copy, project concepts, and compelling stories.",
        "system_prompt": (
            "You are Spark, a boundless creative strategist, storyteller, and brainstorming partner. "
            "Your mission: ignite imagination, break creative blocks, and craft compelling narratives. "
            "Guidelines:\n"
            "- Generate bold, innovative ideas spanning practical, disruptive, and playful angles.\n"
            "- Use punchy formatting, evocative headlines, and memorable phrasing.\n"
            "- Propose unexpected combinations and cross-disciplinary inspiration.\n"
            "- Bring vibrant enthusiasm, positivity, and creative momentum."
        ),
        "starter_prompts": [
            "Brainstorm 3 novel AI-powered micro-SaaS ideas for students.",
            "Draft a compelling 60-second elevator pitch for an open-source project.",
            "Give me a creative sci-fi plot hook involving rogue AI and botany.",
            "Suggest 5 punchy brand names and taglines for an eco-friendly tech startup."
        ]
    },
    "🌟 Friendly Life Companion (Aura)": {
        "id": "companion",
        "avatar": "🌟",
        "title": "Aura - Empathetic Companion",
        "description": "Warm, conversational buddy for daily reflection, motivation, and thoughtful chats.",
        "system_prompt": (
            "You are Aura, a warm, supportive, and empathetic AI friend. "
            "Your mission: provide uplifting conversation, thoughtful reflection, and balanced motivation. "
            "Guidelines:\n"
            "- Communicate with genuine warmth, active listening, and gentle wit.\n"
            "- Offer supportive perspectives without being overly preachy.\n"
            "- Help the user reflect, de-stress, or organize thoughts positively.\n"
            "- Keep conversations engaging, natural, and human."
        ),
        "starter_prompts": [
            "How can I overcome procrastination when starting a big project?",
            "Suggest a relaxing 5-minute wind-down routine after hours of coding.",
            "What are some simple daily habits that significantly improve focus?",
            "Tell me an intriguing, uplifting fact about science or human history."
        ]
    }
}

AVAILABLE_MODELS = [
    "gemini-3.6-flash",
    "gemini-2.0-flash",
]

# -----------------------------------------------------------------------------
# API Key Management
# -----------------------------------------------------------------------------
def get_configured_api_key():
    """Retrieve Gemini API key across secrets, environment, or user session."""
    # 1. User manual input in sidebar
    if st.session_state.get("user_api_key"):
        return st.session_state["user_api_key"].strip()

    # 2. Streamlit secrets
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"].strip()
    except Exception:
        pass

    # 3. Local environment variable (.env)
    env_key = os.getenv("GEMINI_API_KEY")
    if env_key:
        return env_key.strip()

    return None

# -----------------------------------------------------------------------------
# Initialize Session State
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "interaction_id" not in st.session_state:
    st.session_state.interaction_id = None

if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = list(PERSONAS.keys())[0]

if "last_persona" not in st.session_state:
    st.session_state.last_persona = st.session_state.selected_persona

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

if "selected_model" not in st.session_state:
    st.session_state.selected_model = AVAILABLE_MODELS[0]

# -----------------------------------------------------------------------------
# Sidebar: Settings & Controls
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://api.iconify.design/lucide:bot.svg?color=%236366f1", width=48)
    st.title("NexusAI Settings")
    st.caption("Customizable AI Chatbot | μLearn #cl-ai-chatbot")
    st.markdown("---")

    # Persona Selection
    st.subheader("🎭 Persona Mode")
    chosen_persona_label = st.selectbox(
        "Choose Assistant Persona:",
        options=list(PERSONAS.keys()),
        index=list(PERSONAS.keys()).index(st.session_state.selected_persona),
        help="Selects the tone, domain expertise, and system instructions for the chatbot."
    )
    st.session_state.selected_persona = chosen_persona_label
    
    # If persona switched, reset interaction ID so new system prompt takes effect
    if st.session_state.last_persona != chosen_persona_label:
        st.session_state.last_persona = chosen_persona_label
        st.session_state.interaction_id = None

    current_persona = PERSONAS[chosen_persona_label]
    st.info(f"**{current_persona['title']}**\n\n{current_persona['description']}")

    st.markdown("---")

    # Model & Generation Parameters
    st.subheader("⚙️ Model Configuration")
    st.session_state.selected_model = st.selectbox(
        "Gemini Model:",
        options=AVAILABLE_MODELS,
        index=AVAILABLE_MODELS.index(st.session_state.selected_model),
        help="Select the underlying Google Gemini generative model."
    )

    st.markdown("---")

    # API Key Configuration
    st.subheader("🔑 Google Gemini API Key")
    active_key = get_configured_api_key()

    if active_key:
        st.success("🟢 API Key Active & Connected")
        with st.expander("Update API Key"):
            new_key = st.text_input("Enter new key:", type="password", key="new_key_input")
            if st.button("Save New Key"):
                st.session_state["user_api_key"] = new_key
                st.rerun()
    else:
        st.warning("🟡 No API Key Detected (Demo Mode Active)")
        user_key_input = st.text_input(
            "Paste Gemini API Key:",
            type="password",
            placeholder="AIzaSy... / AQ...",
            help="Your key is stored only in your active browser session."
        )
        if user_key_input:
            st.session_state["user_api_key"] = user_key_input
            st.rerun()

        st.markdown(
            "[👉 Get a free Gemini API Key](https://aistudio.google.com/app/apikey) from Google AI Studio in 30 seconds."
        )

    st.markdown("---")

    # Session Management & Export
    st.subheader("🛠️ Session Actions")
    col_clear, col_export = st.columns(2)

    with col_clear:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.interaction_id = None
            st.rerun()

    with col_export:
        if st.session_state.messages:
            # Build markdown export transcript
            export_text = f"# NexusAI Chat Transcript\n"
            export_text += f"- **Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            export_text += f"- **Persona**: {current_persona['title']}\n"
            export_text += f"- **Model**: {st.session_state.selected_model}\n\n---\n\n"
            for m in st.session_state.messages:
                role_title = "User" if m["role"] == "user" else current_persona["title"]
                export_text += f"### {role_title}\n{m['content']}\n\n"

            st.download_button(
                label="📥 Export Chat",
                data=export_text,
                file_name=f"nexusai_chat_{int(time.time())}.md",
                mime="text/markdown",
                use_container_width=True
            )
        else:
            st.button("📥 Export Chat", disabled=True, use_container_width=True)

    # Session stats
    st.markdown("---")
    st.caption(
        f"📊 **Messages**: {len(st.session_state.messages)} | "
        f"**Mode**: {'Live Gemini' if active_key else 'Simulated Demo'}"
    )
    st.caption("Built for **μLearn Foundation** | `#cl-ai-chatbot`")

# -----------------------------------------------------------------------------
# Main Chat Header & Badges
# -----------------------------------------------------------------------------
st.markdown('<div class="main-header">⚡ NexusAI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Your adaptive, multi-persona AI conversational companion for learning, code & creativity.</div>',
    unsafe_allow_html=True
)

# Badges Display
badge_mode = "🟢 Live API" if active_key else "🟡 Offline / Demo Mode"
st.markdown(
    f'<span class="badge-pill badge-persona">{current_persona["avatar"]} {current_persona["title"]}</span>'
    f'<span class="badge-pill badge-model">🧠 {st.session_state.selected_model}</span>'
    f'<span class="badge-pill badge-status">{badge_mode}</span>',
    unsafe_allow_html=True
)
st.write("")

# -----------------------------------------------------------------------------
# Interactive Starter Prompts (When Chat is Fresh)
# -----------------------------------------------------------------------------
prompt_to_send = None

if len(st.session_state.messages) == 0:
    st.markdown("#### 💡 Quick Starters")
    st.caption("Click any prompt to start the conversation with the active persona:")

    chip_cols = st.columns(2)
    for idx, prompt_text in enumerate(current_persona["starter_prompts"]):
        col = chip_cols[idx % 2]
        with col:
            if st.button(f"{current_persona['avatar']} {prompt_text}", key=f"chip_{idx}", use_container_width=True):
                prompt_to_send = prompt_text

# -----------------------------------------------------------------------------
# Render Chat History
# -----------------------------------------------------------------------------
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(message["content"])
    else:
        persona_avatar = message.get("avatar", current_persona["avatar"])
        with st.chat_message("assistant", avatar=persona_avatar):
            st.markdown(message["content"])

# -----------------------------------------------------------------------------
# Chat Input & Response Generation
# -----------------------------------------------------------------------------
user_chat_input = st.chat_input(f"Message {current_persona['title']}...")

final_prompt = prompt_to_send or user_chat_input

if final_prompt:
    # 1. Append & display user message
    st.session_state.messages.append({
        "role": "user",
        "content": final_prompt
    })
    with st.chat_message("user", avatar="👤"):
        st.markdown(final_prompt)

    # 2. Assistant Response Container
    with st.chat_message("assistant", avatar=current_persona["avatar"]):
        # Check if live Gemini API is configured
        if active_key:
            try:
                from google import genai

                client = genai.Client(api_key=active_key)

                # Use Google GenAI Interactions API with multi-turn continuity
                if st.session_state.interaction_id is None:
                    interaction = client.interactions.create(
                        model=st.session_state.selected_model,
                        input=final_prompt,
                        system_instruction=current_persona["system_prompt"]
                    )
                else:
                    interaction = client.interactions.create(
                        model=st.session_state.selected_model,
                        input=final_prompt,
                        previous_interaction_id=st.session_state.interaction_id
                    )

                st.session_state.interaction_id = interaction.id
                raw_response = interaction.output_text

                # Stream response words for polished UX
                def stream_words():
                    for word in raw_response.split(" "):
                        yield word + " "
                        time.sleep(0.012)

                bot_response = st.write_stream(stream_words())

            except Exception as exc:
                bot_response = (
                    f"⚠️ **API Communication Error**: `{exc}`\n\n"
                    "Please verify your Gemini API key or check network connectivity."
                )
                st.error(bot_response)

        else:
            # Simulated / Demo Fallback Mode
            # Provides an immediate, helpful response and instructions to connect live API
            def demo_generator():
                simulated_intro = (
                    f"**[{current_persona['title']} - Demo Mode]**\n\n"
                    f"Hello! I received your query:\n> *\"{final_prompt}\"*\n\n"
                )
                if current_persona["id"] == "tutor":
                    simulated_body = (
                        "In full live mode with your Gemini API key, I analyze this deeply using "
                        "analogies and step-by-step educational explanations!\n\n"
                        "💡 **Key Insight:** Understanding any core concept starts with simplifying the foundations "
                        "into mental models before diving into the complex equations or details."
                    )
                elif current_persona["id"] == "code":
                    simulated_body = (
                        "In full live mode with your Gemini API key, I generate production-ready code snippets, "
                        "analyze asymptotic complexity (Big-O), and refactor algorithms with unit test patterns.\n\n"
                        "```python\n# Example architectural pattern\ndef execute_task(query: str) -> dict:\n    return {'status': 'processed', 'query': query}\n```"
                    )
                elif current_persona["id"] == "creative":
                    simulated_body = (
                        "In full live mode with your Gemini API key, I craft viral elevator pitches, "
                        "generate fresh startup ideas, and draft captivating storytelling arcs!\n\n"
                        "✨ **Spark Idea:** Connect two contrasting domains (e.g. AI + Urban Gardening) "
                        "to unlock an entirely fresh creative angle."
                    )
                else:
                    simulated_body = (
                        "In full live mode with your Gemini API key, I hold thoughtful, supportive, "
                        "and encouraging daily conversations to help keep you motivated and relaxed!\n\n"
                        "🌟 **Reminder:** Celebrate small progress steps every day. Consistency beats intensity."
                    )

                simulated_footer = (
                    "\n\n---\n\n"
                    "🔑 **Want live AI responses?**\n"
                    "Enter your free Gemini API key in the sidebar, or set `GEMINI_API_KEY` in your `.env` file! "
                    "[Get a free API key here](https://aistudio.google.com/app/apikey)."
                )

                full_text = simulated_intro + simulated_body + simulated_footer
                # Simulate streaming effect
                for word in full_text.split(" "):
                    yield word + " "
                    time.sleep(0.015)

            bot_response = st.write_stream(demo_generator())

    # 3. Store response in session state
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response,
        "avatar": current_persona["avatar"]
    })
