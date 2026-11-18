import html
import os
from datetime import datetime

import streamlit as st

BRAND_NAME = "Briefly"
BRAND_SUFFIX = "Reports"
TAGLINE = "Research, Briefly."
HERO_SUBTITLE = (
    "Give Briefly a topic. A team of AI agents searches the web, reads the best source, "
    "writes a structured report and critiques it, all in minutes."
)
CONTACT_EMAIL = ""   
GITHUB_URL = "https://github.com/utsxvv/Multi-Agent-AI-Research-System"      
EXAMPLE_TOPICS = [
    ("Handwriting recognition", "Advances in handwritten text recognition"),
    ("Open-source LLMs", "State of open-source large language models"),
    ("AI in drug discovery", "Impact of AI on drug discovery"),
]

st.set_page_config(
    page_title=f"{BRAND_NAME} {BRAND_SUFFIX} — {TAGLINE}",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"About": f"{BRAND_NAME} {BRAND_SUFFIX}: {TAGLINE}"},
)

try:
    for _key, _value in st.secrets.items():
        if isinstance(_value, str) and _key not in os.environ:
            os.environ[_key] = _value
except Exception:
    pass

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain 


def flat_html(markup: str) -> str:
    """Strip indentation and blank lines so Markdown never treats HTML as a code block."""
    return "\n".join(line.strip() for line in markup.splitlines() if line.strip())


# ---------------------------------------------------------------------------
# Styling (dark theme)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Fraunces:opsz,wght@9..144,500;9..144,600&display=swap');

        :root {
            --ink: #e6e8ee;
            --ink-subtle: #cbd5e1;
            --muted: #8b93a7;
            --line: #232733;
            --line-light: #2e3446;
            --bg: #0b0d12;
            --card: #12151c;
            --card-hover: #171b24;
            --accent: #818cf8;
            --accent-strong: #6366f1;
            --accent-soft: rgba(129, 140, 248, 0.12);
            --accent-border: rgba(129, 140, 248, 0.25);
        }

        html, body, [class*="css"], .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--ink);
            background-color: var(--bg);
        }
        .stApp {
            background-color: var(--bg);
        }
        html {
            scroll-behavior: smooth;
        }

        /* Streamlit chrome cleanup */
        #MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {
            display: none !important;
        }
        header[data-testid="stHeader"] {
            background: transparent !important;
            height: 0 !important;
            min-height: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            border: none !important;
            visibility: hidden;
        }
        .block-container {
            max-width: 1040px;
            padding-top: 1.25rem !important;
            padding-bottom: 3.5rem !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
        }
        div[data-testid="stVerticalBlock"] {
            gap: 0.75rem;
        }

        /* ---------- Navbar ---------- */
        .nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.9rem 0;
            border-bottom: 1px solid var(--line);
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            font-weight: 600;
            font-size: 1.08rem;
            line-height: 1;
            letter-spacing: -0.01em;
        }
        .brand-mark {
            width: 28px;
            height: 28px;
            border-radius: 8px;
            flex-shrink: 0;
            background: linear-gradient(135deg, #6366f1 0%, #c084fc 100%);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            font-size: 0.82rem;
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.35);
        }
        .brand .suffix {
            color: var(--muted);
            font-weight: 500;
        }
        .nav-links {
            display: flex;
            gap: 1.75rem;
        }
        .nav-links a {
            color: var(--muted);
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            transition: color 0.15s ease;
        }
        .nav-links a:hover {
            color: var(--ink);
        }

        /* ---------- Hero ---------- */
        .hero {
            text-align: center;
            padding: 3.5rem 0 1rem;
        }
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.32rem 0.9rem;
            border-radius: 999px;
            background: var(--accent-soft);
            color: #a5b4fc;
            border: 1px solid var(--accent-border);
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            margin-bottom: 1.3rem;
        }
        .hero h1 {
            font-family: 'Fraunces', serif;
            font-weight: 600;
            font-size: clamp(2.4rem, 4.5vw, 3.6rem);
            padding: 0;
            line-height: 1.15;
            letter-spacing: -0.025em;
            margin: 0 0 1.1rem;
            color: var(--ink);
        }
        .hero h1 em {
            font-style: italic;
            color: var(--accent);
        }
        .hero p {
            color: var(--muted);
            font-size: 1.06rem;
            line-height: 1.65;
            max-width: 620px;
            margin: 0 auto;
        }

        /* ---------- Search Form (Centered & Aligned) ---------- */
        div[data-testid="stForm"] {
            max-width: 680px;
            width: 100% !important;
            margin: 1.35rem auto 0 !important;
            border: none !important;
            padding: 0 !important;
            background: transparent !important;
        }
        div[data-testid="stForm"] > div[data-testid="stVerticalBlock"] {
            gap: 0.65rem;
            width: 100% !important;
        }
        div[data-testid="stTextInput"] {
            width: 100% !important;
        }
        div[data-testid="stTextInput"] div[data-baseweb="base-input"],
        div[data-testid="stTextInput"] div[data-baseweb="input"] {
            height: 3.35rem !important;
            border-radius: 14px !important;
            border: 1px solid var(--line) !important;
            background: var(--card) !important;
            box-shadow: 0 8px 30px rgba(0,0,0,0.35);
            overflow: hidden;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }
        div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2) !important;
        }
        div[data-testid="stTextInput"] input {
            background: transparent !important;
            color: var(--ink) !important;
            font-size: 1rem !important;
            padding: 0 1.15rem !important;
            height: 100% !important;
        }
        div[data-testid="stTextInput"] input::placeholder {
            color: var(--muted) !important;
            opacity: 0.85;
        }

        /* Submit Button */
        div[data-testid="stFormSubmitButton"] {
            width: 100% !important;
            margin-top: 0.25rem;
        }
        div[data-testid="stFormSubmitButton"] button {
            width: 100% !important;
            height: 3.15rem !important;
            border-radius: 12px !important;
            border: none !important;
            background: var(--accent-strong) !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 0.98rem !important;
            cursor: pointer !important;
            box-shadow: 0 4px 18px rgba(99, 102, 241, 0.3) !important;
            transition: all 0.2s ease !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        div[data-testid="stFormSubmitButton"] button:hover {
            background: var(--accent) !important;
            color: #0b0d12 !important;
            box-shadow: 0 6px 24px rgba(129, 140, 248, 0.4) !important;
            transform: translateY(-1px);
        }
        div[data-testid="stFormSubmitButton"] button:active {
            transform: translateY(0);
        }
        div[data-testid="stFormSubmitButton"] button p {
            color: inherit !important;
            font-size: 0.98rem !important;
            font-weight: 600 !important;
            margin: 0 !important;
        }

        /* ---------- Example Chips ---------- */
        .chips-label {
            text-align: center;
            color: var(--muted);
            font-size: 0.8rem;
            font-weight: 500;
            margin: 0.85rem 0 0.45rem;
            letter-spacing: 0.01em;
        }
        div[data-testid="stHorizontalBlock"] {
            max-width: 680px;
            margin: 0 auto;
            gap: 0.6rem;
        }
        div[data-testid="stHorizontalBlock"] button {
            width: 100% !important;
            min-height: 2.25rem !important;
            border-radius: 999px !important;
            border: 1px solid var(--line) !important;
            background: var(--card) !important;
            color: var(--muted) !important;
            padding: 0.25rem 0.85rem !important;
            transition: all 0.15s ease !important;
            cursor: pointer !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        div[data-testid="stHorizontalBlock"] button p {
            font-size: 0.82rem !important;
            font-weight: 500 !important;
            color: inherit !important;
            margin: 0 !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }
        div[data-testid="stHorizontalBlock"] button:hover {
            border-color: var(--accent) !important;
            color: var(--accent) !important;
            background: var(--card-hover) !important;
        }
        div[data-testid="stHorizontalBlock"] button:focus,
        div[data-testid="stHorizontalBlock"] button:focus-visible {
            outline: none !important;
            box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.25) !important;
        }

        /* ---------- Live Status Boxes & Alerts ---------- */
        div[data-testid="stStatusWidget"] {
            max-width: 680px !important;
            margin: 0.5rem auto !important;
            background: var(--card) !important;
            border: 1px solid var(--line) !important;
            border-radius: 12px !important;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0,0,0,0.25) !important;
        }
        div[data-testid="stStatusWidget"] details {
            background: transparent !important;
            border: none !important;
        }
        div[data-testid="stStatusWidget"] summary {
            padding: 0.75rem 1rem !important;
            color: var(--ink) !important;
            font-size: 0.92rem !important;
            font-weight: 500 !important;
            cursor: pointer !important;
        }
        div[data-testid="stStatusWidget"] summary:hover {
            color: var(--accent) !important;
        }
        div[data-testid="stAlert"] {
            max-width: 680px !important;
            margin: 1rem auto !important;
            border-radius: 12px !important;
            border: 1px solid var(--line) !important;
            background: var(--card) !important;
        }

        /* ---------- Sections ---------- */
        .section {
            padding: 4.5rem 0 0.5rem;
            scroll-margin-top: 1.5rem;
        }
        .eyebrow {
            color: var(--accent);
            font-size: 0.76rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            text-align: center;
            margin-bottom: 0.6rem;
        }
        .section h2 {
            font-family: 'Fraunces', serif;
            font-weight: 600;
            font-size: 2.1rem;
            padding: 0;
            letter-spacing: -0.02em;
            text-align: center;
            margin: 0 0 2rem;
            color: var(--ink);
        }
        .grid {
            display: grid;
            gap: 1rem;
            align-items: stretch;
        }
        .grid-4 {
            grid-template-columns: repeat(4, 1fr);
        }
        .grid-3 {
            grid-template-columns: repeat(3, 1fr);
        }
        .card {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 1.4rem;
            display: flex;
            flex-direction: column;
            transition: border-color 0.2s ease, background 0.2s ease, transform 0.2s ease;
        }
        .card:hover {
            border-color: #343a4d;
            background: var(--card-hover);
            transform: translateY(-2px);
        }
        .card .num {
            width: 30px;
            height: 30px;
            border-radius: 9px;
            background: var(--accent-soft);
            color: var(--accent);
            font-weight: 600;
            font-size: 0.85rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 0.9rem;
            flex-shrink: 0;
        }
        .card h3 {
            font-size: 1.02rem;
            font-weight: 600;
            margin: 0 0 0.4rem;
            padding: 0;
            color: var(--ink);
        }
        .card p {
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1.55;
            margin: 0;
        }

        /* ---------- Results & Tabs ---------- */
        .topic-chip-wrapper {
            margin-bottom: 0.6rem;
        }
        .topic-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.32rem 0.9rem;
            border-radius: 999px;
            background: var(--accent-soft);
            color: #a5b4fc;
            font-size: 0.85rem;
            font-weight: 500;
            border: 1px solid rgba(129,140,248,.25);
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 1.75rem;
            border-bottom: 1px solid var(--line);
            background: transparent;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 0.65rem 0.2rem;
            font-weight: 500;
            font-size: 0.95rem;
            color: var(--muted);
            background: transparent !important;
            border: none !important;
            transition: color 0.15s ease;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: var(--ink);
        }
        .stTabs [aria-selected="true"] {
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        .stTabs [data-baseweb="tab-highlight"] {
            background-color: var(--accent) !important;
            height: 2px !important;
            border-radius: 2px !important;
        }
        div[data-baseweb="tab-panel"] {
            padding: 1.5rem 0 0.5rem !important;
        }
        div[data-testid="stDownloadButton"] {
            margin-top: 1.25rem !important;
        }
        div[data-testid="stDownloadButton"] button {
            border-radius: 10px !important;
            border: 1px solid var(--line) !important;
            background: var(--card) !important;
            color: var(--ink) !important;
            font-weight: 500 !important;
            font-size: 0.9rem !important;
            padding: 0.5rem 1.25rem !important;
            transition: all 0.15s ease !important;
            cursor: pointer !important;
        }
        div[data-testid="stDownloadButton"] button:hover {
            border-color: var(--accent) !important;
            color: var(--accent) !important;
            background: var(--card-hover) !important;
        }
        div[data-testid="stDownloadButton"] button p {
            color: inherit !important;
            font-weight: 500 !important;
            margin: 0 !important;
        }
        div[data-testid="stCaptionContainer"] {
            color: var(--muted) !important;
            font-size: 0.82rem !important;
            margin-top: 0.4rem !important;
        }
        hr {
            border: none !important;
            border-top: 1px solid var(--line) !important;
            margin: 2.25rem 0 1.25rem !important;
        }

        /* Sources Card */
        .source-card {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 1.15rem 1.25rem;
            margin-bottom: 0.85rem;
            transition: border-color 0.15s ease;
        }
        .source-card:hover {
            border-color: #343a4d;
        }
        .source-title {
            font-weight: 600;
            font-size: 0.98rem;
            color: var(--ink);
            margin-bottom: 0.3rem;
        }
        .source-url {
            font-size: 0.82rem;
            margin-bottom: 0.45rem;
        }
        .source-url a {
            color: var(--accent);
            text-decoration: underline;
            text-underline-offset: 2px;
            word-break: break-all;
        }
        .source-snippet {
            font-size: 0.88rem;
            line-height: 1.55;
            color: var(--muted);
        }

        /* Markdown Typography inside Results */
        div[data-baseweb="tab-panel"] div[data-testid="stMarkdownContainer"] h1 {
            font-family: 'Fraunces', serif;
            font-size: 1.75rem;
            color: var(--ink);
            margin: 1.25rem 0 0.75rem;
        }
        div[data-baseweb="tab-panel"] div[data-testid="stMarkdownContainer"] h2 {
            font-family: 'Fraunces', serif;
            font-size: 1.4rem;
            color: var(--ink);
            margin: 1.15rem 0 0.6rem;
        }
        div[data-baseweb="tab-panel"] div[data-testid="stMarkdownContainer"] h3 {
            font-family: 'Fraunces', serif;
            font-size: 1.15rem;
            color: var(--ink);
            margin: 1rem 0 0.5rem;
        }
        div[data-baseweb="tab-panel"] div[data-testid="stMarkdownContainer"] p,
        div[data-baseweb="tab-panel"] div[data-testid="stMarkdownContainer"] li {
            font-size: 0.96rem;
            line-height: 1.7;
            color: #d1d5db;
        }
        div[data-baseweb="tab-panel"] div[data-testid="stMarkdownContainer"] a {
            color: var(--accent);
            text-decoration: underline;
            text-underline-offset: 3px;
        }

        /* Expanders (FAQ and error details) */
        div[data-testid="stExpander"] {
            max-width: 720px;
            margin: 0 auto 0.6rem;
        }
        div[data-testid="stExpander"] details {
            background: var(--card) !important;
            border: 1px solid var(--line) !important;
            border-radius: 12px !important;
            overflow: hidden;
            transition: border-color 0.15s ease;
        }
        div[data-testid="stExpander"] details:hover {
            border-color: #343a4d !important;
        }
        div[data-testid="stExpander"] summary {
            padding: 0.85rem 1.15rem !important;
            color: var(--ink) !important;
            font-weight: 500 !important;
            font-size: 0.95rem !important;
            cursor: pointer !important;
        }
        div[data-testid="stExpander"] summary:hover {
            color: var(--accent) !important;
        }
        div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {
            padding: 0 1.15rem 1rem !important;
            color: var(--muted) !important;
            font-size: 0.92rem !important;
            line-height: 1.6 !important;
        }

        /* ---------- Footer ---------- */
        .footer {
            margin-top: 5rem;
            padding-top: 2rem;
            border-top: 1px solid var(--line);
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 1.5rem;
            align-items: start;
        }
        .footer .about {
            max-width: 420px;
            color: var(--muted);
            font-size: 0.85rem;
            line-height: 1.6;
            margin-top: 0.8rem;
        }
        .footer .links {
            display: flex;
            gap: 1.5rem;
            padding-top: 0.35rem;
        }
        .footer .links a {
            color: var(--muted);
            text-decoration: none;
            font-size: 0.88rem;
            font-weight: 500;
            transition: color 0.15s ease;
        }
        .footer .links a:hover {
            color: var(--ink);
        }
        .copyright {
            grid-column: 1 / -1;
            color: var(--muted);
            font-size: 0.8rem;
            padding-top: 1.25rem;
            margin-top: 0.5rem;
            border-top: 1px solid var(--line);
        }

        /* ---------- Responsive ---------- */
        @media (max-width: 960px) and (min-width: 641px) {
            .grid-4 {grid-template-columns: repeat(2, 1fr);}
        }

        @media (max-width: 640px) {
            .grid-4, .grid-3 {grid-template-columns: 1fr;}
            .hero {padding-top: 2.25rem;}
            .nav-links {display: none;}
            .footer {grid-template-columns: 1fr;}
            div[data-testid="stHorizontalBlock"] {
                flex-direction: column !important;
                gap: 0.5rem !important;
            }
            div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Pipeline helpers
# ---------------------------------------------------------------------------
def to_text(content) -> str:
    """Normalize LangChain output (str, message, or list of blocks) to a string."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if hasattr(content, "content"):
        return to_text(content.content)
    if isinstance(content, list):
        parts = [
            item.get("text", "") if isinstance(item, dict) else to_text(item)
            for item in content
        ]
        return "\n".join(p for p in parts if p)
    return str(content)


@st.cache_resource(show_spinner=False)
def get_agents():
    """Build agents once per server process instead of on every run."""
    return build_search_agent(), build_reader_agent()


def run_pipeline(topic: str) -> dict:
    """Same logic as pipeline.py, with live progress shown in the UI."""
    search_agent, reader_agent = get_agents()
    state = {}

    with st.status("Searching the web…", expanded=False) as status:
        result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        state["search_results"] = to_text(result["messages"][-1].content)
        status.update(label="Search complete", state="complete")

    with st.status("Reading the best source…", expanded=False) as status:
        result = reader_agent.invoke({
            "messages": [(
                "user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content. \n\n"
                f"Search Results:\n{state['search_results'][:800]}",
            )]
        })
        state["scraped_content"] = to_text(result["messages"][-1].content)
        status.update(label="Source read", state="complete")

    with st.status("Writing the report…", expanded=False) as status:
        research_combined = (
            f"SEARCH RESULTS:\n{state['search_results']}\n\n"
            f"SCRAPED CONTENT:\n{state['scraped_content']}\n\n"
        )
        state["report"] = to_text(writer_chain.invoke({
            "topic": topic,
            "research": research_combined,
        }))
        status.update(label="Report written", state="complete")

    with st.status("Reviewing the report…", expanded=False) as status:
        state["feedback"] = to_text(critic_chain.invoke({"report": state["report"]}))
        status.update(label="Review complete", state="complete")

    return state


def set_example(text: str):
    st.session_state["topic_input"] = text
    st.session_state.pop("result", None)


# ---------------------------------------------------------------------------
# Navbar
# ---------------------------------------------------------------------------
_brand = (
    f'<div class="brand"><div class="brand-mark">✦</div>'
    f'<div>{html.escape(BRAND_NAME)} <span class="suffix">{html.escape(BRAND_SUFFIX)}</span></div></div>'
)

st.markdown(
    flat_html(
        f"""
        <div class="nav">
            {_brand}
            <div class="nav-links">
                <a href="#how-it-works" target="_self">How it works</a>
                <a href="#features" target="_self">Features</a>
                <a href="#faq" target="_self">FAQ</a>
            </div>
        </div>
        """
    ),
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Hero + input
# ---------------------------------------------------------------------------
_tag_main = TAGLINE.split(",")[0]
_tag_em = TAGLINE.split(",")[-1].strip().rstrip(".")

st.markdown(
    flat_html(
        f"""
        <div class="hero">
            <div class="badge">✦ Multi-agent AI research</div>
            <h1>{html.escape(_tag_main)}, <em>{html.escape(_tag_em)}.</em></h1>
            <p>{html.escape(HERO_SUBTITLE)}</p>
        </div>
        """
    ),
    unsafe_allow_html=True,
)

with st.form("research_form", border=False):
    topic_input = st.text_input(
        "Topic",
        key="topic_input",
        placeholder="What would you like to research?",
        label_visibility="collapsed",
        max_chars=300,
    )
    submitted = st.form_submit_button("Generate report", use_container_width=True)

st.markdown('<div class="chips-label">Try an example</div>', unsafe_allow_html=True)
_cols = st.columns(len(EXAMPLE_TOPICS))
for _i, (_label, _topic) in enumerate(EXAMPLE_TOPICS):
    _cols[_i].button(_label, key=f"example_{_i}", on_click=set_example, args=(_topic,), use_container_width=True)

if submitted:
    topic = topic_input.strip()
    if len(topic) < 3:
        st.warning("Please enter a topic (at least 3 characters).")
    else:
        st.session_state.pop("result", None)
        try:
            st.session_state["result"] = run_pipeline(topic)
            st.session_state["topic"] = topic
        except Exception as exc:
            st.error(
                "The research run failed. Please check your API keys and network "
                "connection, then try again."
            )
            with st.expander("Error details"):
                st.code(f"{type(exc).__name__}: {exc}")

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
result = st.session_state.get("result")
if result:
    st.divider()
    st.markdown(
        f'<div class="topic-chip-wrapper"><span class="topic-chip">✦ {html.escape(st.session_state.get("topic", ""))}</span></div>',
        unsafe_allow_html=True,
    )

    tab_report, tab_review, tab_sources = st.tabs(["Report", "Review", "Sources"])

    with tab_report:
        st.markdown(result["report"])
        st.download_button(
            "Download report (.md)",
            data=result["report"],
            file_name="research_report.md",
            mime="text/markdown",
        )
        st.caption("AI-generated content. Verify important facts against the original sources.")

    with tab_review:
        st.markdown(result["feedback"])

    with tab_sources:
        st.subheader("Search results")
        raw_sr = result.get("search_results", "")
        if raw_sr:
            blocks = raw_sr.strip().split("\n\n")
            has_structured = any("Title:" in b and "URL:" in b for b in blocks)
            if has_structured:
                for block in blocks:
                    lines = block.strip().splitlines()
                    title, url_val, snippet_parts = "", "", []
                    current_field = None
                    for line in lines:
                        if line.startswith("Title:"):
                            title = line.replace("Title:", "", 1).strip()
                            current_field = "title"
                        elif line.startswith("URL:"):
                            url_val = line.replace("URL:", "", 1).strip()
                            current_field = "url"
                        elif line.startswith("Snippet:"):
                            snippet_parts.append(line.replace("Snippet:", "", 1).strip())
                            current_field = "snippet"
                        elif current_field == "snippet":
                            snippet_parts.append(line.strip())
                    snippet = " ".join(snippet_parts)
                    if title or url_val:
                        card_html = '<div class="source-card">'
                        if title:
                            card_html += f'<div class="source-title">{html.escape(title)}</div>'
                        if url_val:
                            card_html += f'<div class="source-url"><a href="{html.escape(url_val)}" target="_blank" rel="noopener noreferrer">{html.escape(url_val)}</a></div>'
                        if snippet:
                            card_html += f'<div class="source-snippet">{html.escape(snippet)}</div>'
                        card_html += '</div>'
                        st.markdown(card_html, unsafe_allow_html=True)
                    elif block.strip():
                        st.markdown(block)
            else:
                st.markdown(raw_sr)
        else:
            st.caption("No search results recorded.")

        st.subheader("Scraped content")
        scraped = result.get("scraped_content", "")
        if scraped:
            with st.expander("View scraped content", expanded=False):
                st.text(scraped)
        else:
            st.caption("No scraped content recorded.")

# ---------------------------------------------------------------------------
# How it works / Features / FAQ
# ---------------------------------------------------------------------------
st.markdown(
    flat_html(
        """
        <div class="section" id="how-it-works">
            <div class="eyebrow">How it works</div>
            <h2>Four agents, one polished report</h2>
            <div class="grid grid-4">
                <div class="card"><div class="num">1</div><h3>Search</h3>
                    <p>The search agent finds recent, reliable sources on your topic.</p></div>
                <div class="card"><div class="num">2</div><h3>Read</h3>
                    <p>The reader agent picks the most relevant page and extracts deeper content.</p></div>
                <div class="card"><div class="num">3</div><h3>Write</h3>
                    <p>The writer turns the research into a clear, structured report.</p></div>
                <div class="card"><div class="num">4</div><h3>Review</h3>
                    <p>The critic evaluates the draft and flags gaps and improvements.</p></div>
            </div>
        </div>
        <div class="section" id="features">
            <div class="eyebrow">Features</div>
            <h2>Built for focused, trustworthy research</h2>
            <div class="grid grid-3">
                <div class="card"><h3>Transparent process</h3>
                    <p>Follow each stage live and inspect the raw search results and scraped content.</p></div>
                <div class="card"><h3>Built-in critique</h3>
                    <p>Every report is reviewed by a separate agent before you read it.</p></div>
                <div class="card"><h3>Export ready</h3>
                    <p>Download your report as Markdown and drop it into your notes or documents.</p></div>
            </div>
        </div>
        <div class="section" id="faq" style="padding-bottom: 0;">
            <div class="eyebrow">FAQ</div>
            <h2 style="margin-bottom: 1.25rem;">Common questions</h2>
        </div>
        """
    ),
    unsafe_allow_html=True,
)

with st.expander("How accurate are the reports?"):
    st.write(
        "Reports are generated by AI from live web sources. They are a strong starting point, "
        "but you should verify important facts using the Sources tab."
    )
with st.expander("How long does a report take?"):
    st.write("Usually a few minutes, depending on the topic and the sources the agents find.")
with st.expander("Is my data stored?"):
    st.write(
        "Your topic and results live only in your current browser session and are cleared "
        "when you close or refresh the page."
    )
with st.expander("What topics can I research?"):
    st.write("Anything with publicly available information on the web: technology, science, business and more.")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
_links = [
    '<a href="#how-it-works" target="_self">How it works</a>',
    '<a href="#features" target="_self">Features</a>',
    '<a href="#faq" target="_self">FAQ</a>',
]
if GITHUB_URL:
    _links.append(f'<a href="{html.escape(GITHUB_URL)}" target="_blank" rel="noopener noreferrer">GitHub</a>')
if CONTACT_EMAIL:
    _links.append(f'<a href="mailto:{html.escape(CONTACT_EMAIL)}">Contact</a>')
_links_html = f'<div class="links">{"".join(_links)}</div>'

st.markdown(
    flat_html(
        f"""
        <div class="footer">
            <div>
                {_brand}
                <div class="about">An AI-powered research assistant that searches, reads, writes and reviews so you can
                focus on insight. Outputs are AI-generated; please verify critical information.</div>
            </div>
            {_links_html}
        </div>
        """
    ),
    unsafe_allow_html=True,
)
