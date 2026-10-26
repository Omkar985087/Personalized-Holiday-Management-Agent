"""
Personalized Holiday Management Agent — Streamlit Frontend
===========================================================
A premium travel-planning interface that invokes the existing
LangGraph workflow and displays a rich, downloadable itinerary.
"""

import re
import streamlit as st

# ─────────────────────── Page Configuration ──────────────────────
st.set_page_config(
    page_title="Personalized Holiday Management Agent",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────── Custom CSS ──────────────────────────────
st.markdown(
    """
<style>
/* ── Google Fonts ─────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

/* ── CSS Variables ────────────────────────────────────────────── */
:root {
    --bg-primary:    #0b0f19;
    --bg-card:       rgba(255,255,255,0.04);
    --bg-card-hover: rgba(255,255,255,0.07);
    --text-primary:  #f0f2f5;
    --text-secondary:#94a3b8;
    --accent:        #6366f1;
    --accent-light:  #818cf8;
    --accent-glow:   rgba(99,102,241,0.25);
    --success:       #10b981;
    --warning:       #f59e0b;
    --danger:        #ef4444;
    --border:        rgba(255,255,255,0.06);
    --gradient-start:#6366f1;
    --gradient-end:  #a855f7;
    --radius:        16px;
    --radius-sm:     10px;
    --shadow:        0 8px 32px rgba(0,0,0,0.3);
}

/* ── Global Resets ────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }

/* ── Hero Section ─────────────────────────────────────────────── */
.hero-wrapper {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.hero-wrapper::before {
    content: "";
    position: absolute;
    top: -60px; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 600px;
    background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}
.hero-icon {
    font-size: 3.6rem;
    margin-bottom: .4rem;
    position: relative;
    z-index: 1;
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%,100%{ transform: translateY(0) }
    50%{ transform: translateY(-10px) }
}
.hero-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 2.75rem;
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    position: relative;
    z-index: 1;
}
.hero-subtitle {
    font-size: 1.15rem;
    color: var(--text-secondary);
    max-width: 560px;
    margin: .8rem auto 0;
    line-height: 1.6;
    position: relative;
    z-index: 1;
}

/* ── Glass Card ───────────────────────────────────────────────── */
.glass-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 2rem;
    backdrop-filter: blur(12px);
    box-shadow: var(--shadow);
    transition: background .25s;
}
.glass-card:hover { background: var(--bg-card-hover); }

/* ── Section Headers ──────────────────────────────────────────── */
.section-header {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 1.5rem;
    color: var(--text-primary);
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: .55rem;
}

/* ── Streamlit Inputs ─────────────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    padding: .65rem 1rem !important;
    font-size: .95rem !important;
    transition: border .2s;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}

/* Multiselect */
[data-testid="stMultiSelect"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end)) !important;
    border-radius: 6px !important;
    color: #fff !important;
}

/* Select / Radio pill buttons */
div[data-testid="stRadio"] > div {
    gap: .5rem !important;
    flex-wrap: wrap;
}
div[data-testid="stRadio"] label {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    padding: .5rem 1.1rem !important;
    color: var(--text-secondary) !important;
    transition: all .2s;
}
div[data-testid="stRadio"] label[data-checked="true"],
div[data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end)) !important;
    border-color: var(--accent) !important;
    color: #fff !important;
}

/* ── Primary Button ───────────────────────────────────────────── */
[data-testid="stButton"] > button,
button[kind="primary"] {
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    padding: .75rem 2rem !important;
    cursor: pointer !important;
    transition: transform .15s, box-shadow .25s !important;
    width: 100% !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px var(--accent-glow) !important;
}

/* ── Metric / Summary Cards ───────────────────────────────────── */
.metric-row {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
}
.metric-card {
    flex: 1 1 140px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 1.2rem;
    text-align: center;
    transition: transform .2s;
}
.metric-card:hover { transform: translateY(-3px); }
.metric-icon { font-size: 1.6rem; margin-bottom: .3rem; }
.metric-label {
    font-size: .75rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: .06em;
}
.metric-value {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--text-primary);
}

/* ── Day Card ─────────────────────────────────────────────────── */
.day-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem 1.8rem;
    margin-bottom: 1rem;
    transition: background .2s;
}
.day-card:hover { background: var(--bg-card-hover); }
.day-card h3 {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    margin: 0 0 .6rem;
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ── Attraction Chips ─────────────────────────────────────────── */
.attraction-chip {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 8px;
    padding: .35rem .85rem;
    margin: .25rem .3rem .25rem 0;
    font-size: .85rem;
    color: var(--accent-light);
    transition: background .2s;
}
.attraction-chip:hover { background: rgba(99,102,241,0.22); }
.attraction-chip a {
    color: var(--accent-light) !important;
    text-decoration: none;
}
.attraction-chip a:hover { text-decoration: underline; }

/* ── Footer ───────────────────────────────────────────────────── */
.app-footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: var(--text-secondary);
    font-size: .82rem;
}

/* ── Responsive ───────────────────────────────────────────────── */
@media (max-width: 768px) {
    .hero-title  { font-size: 2rem; }
    .hero-subtitle { font-size: 1rem; }
    .metric-row  { flex-direction: column; }
}

/* ── Misc. Streamlit Overrides ────────────────────────────────── */
[data-testid="stMarkdownContainer"] h2 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
}
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    background: var(--bg-card) !important;
}
[data-testid="stExpander"] summary {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
}

/* Download button */
[data-testid="stDownloadButton"] > button {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(255,255,255,0.12) !important;
    border-color: var(--accent) !important;
}

/* Spinner */
[data-testid="stSpinner"] > div { color: var(--accent-light) !important; }

/* Hide hamburger and footer */
#MainMenu, footer { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────── Helper Utilities ────────────────────────

INTEREST_OPTIONS = [
    "🍜 Food",
    "🌿 Nature",
    "🏛️ History",
    "🧗 Adventure",
    "🎌 Anime",
    "🛍️ Shopping",
    "🏖️ Beaches",
    "🎭 Local Culture",
]

BUDGET_OPTIONS = ["Budget-friendly", "Moderate", "Luxury"]
BUDGET_ICONS = {"Budget-friendly": "💰", "Moderate": "💳", "Luxury": "👑"}

STYLE_OPTIONS = ["Relaxed", "Balanced", "Packed"]
STYLE_ICONS = {"Relaxed": "🧘", "Balanced": "⚖️", "Packed": "🚀"}


def clean_interest(label: str) -> str:
    """Strip the emoji prefix from an interest label."""
    return re.sub(r"^[^\w]+", "", label).strip()


def split_itinerary_into_days(md_text: str) -> list[tuple[str, str]]:
    """Split Markdown itinerary into (heading, body) tuples per day."""
    pattern = r"(#{1,6}\s+\**Day\s+\d+.*)"
    parts = re.split(pattern, md_text, flags=re.IGNORECASE)

    days: list[tuple[str, str]] = []
    i = 1
    while i < len(parts):
        heading = parts[i].strip().lstrip("#").strip()
        body = parts[i + 1].strip() if (i + 1) < len(parts) else ""
        days.append((heading, body))
        i += 2

    return days


# ─────────────────────── Session-State Defaults ──────────────────
for key, default in [
    ("itinerary_result", None),
    ("planning_error", None),
    ("is_planning", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ═══════════════════════ UI — Hero Section ═══════════════════════
st.markdown(
    """
<div class="hero-wrapper">
    <div class="hero-icon">🌍</div>
    <h1 class="hero-title">Personalized Holiday Management Agent</h1>
    <p class="hero-subtitle">
        Your next adventure, thoughtfully planned.
        Powered by AI research and real-world data from OpenStreetMap.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# ═══════════════════════ UI — Planning Form ══════════════════════
if st.session_state.itinerary_result is None:
    # Centered form column
    _, col_form, _ = st.columns([1, 2, 1])

    with col_form:
        st.markdown(
            '<div class="section-header">✈️ Plan Your Trip</div>',
            unsafe_allow_html=True,
        )

        with st.container():
            destination = st.text_input(
                "Destination",
                placeholder="e.g. Mumbai, India",
                help="City or region you'd like to visit.",
            )

            interests = st.multiselect(
                "Interests",
                options=INTEREST_OPTIONS,
                default=["🍜 Food", "🏛️ History"],
                help="Select one or more interests to personalise your trip.",
            )

            col_days, col_budget, col_style = st.columns(3)

            with col_days:
                days = st.number_input(
                    "Trip Duration (days)",
                    min_value=1,
                    max_value=30,
                    value=3,
                    step=1,
                )

            with col_budget:
                budget = st.radio(
                    "Budget",
                    BUDGET_OPTIONS,
                    index=1,
                    horizontal=True,
                )

            with col_style:
                travel_style = st.radio(
                    "Travel Style",
                    STYLE_OPTIONS,
                    index=1,
                    horizontal=True,
                )

            st.markdown("")  # spacer

            generate_clicked = st.button(
                "✨  Generate My Itinerary",
                type="primary",
                use_container_width=True,
            )

    # ── Handle submission ────────────────────────────────────────
    if generate_clicked:
        # Validate
        if not destination or not destination.strip():
            st.error("🚫 Please enter a destination.")
            st.stop()

        if not interests:
            st.error("🚫 Please select at least one interest.")
            st.stop()

        interests_str = ", ".join(clean_interest(i) for i in interests)

        with st.spinner("🔍  Researching destinations & crafting your personalized adventure…"):
            try:
                from main import plan_holiday  # lazy import avoids circular issues

                result = plan_holiday(
                    destination=destination.strip(),
                    interests=interests_str,
                    days=int(days),
                    budget=budget,
                    travel_style=travel_style,
                )

                st.session_state.itinerary_result = result
                st.session_state.planning_error = None
                st.rerun()

            except Exception as exc:
                st.session_state.planning_error = str(exc)
                st.error(
                    f"⚠️ Something went wrong while generating your itinerary:\n\n`{exc}`\n\n"
                    "Please check your API key in `.env` and try again."
                )

# ═══════════════════════ UI — Results ════════════════════════════
else:
    result = st.session_state.itinerary_result

    # ── Summary Metrics ──────────────────────────────────────────
    destination_display = result.get("destination", "—")
    days_display = result.get("days", "—")
    budget_display = result.get("budget", "Moderate")
    style_display = result.get("travel_style", "Balanced")
    attractions = result.get("attractions", [])

    st.markdown(
        f"""
<div class="metric-row">
    <div class="metric-card">
        <div class="metric-icon">📍</div>
        <div class="metric-label">Destination</div>
        <div class="metric-value">{destination_display}</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">📅</div>
        <div class="metric-label">Duration</div>
        <div class="metric-value">{days_display} Day{"s" if days_display != 1 else ""}</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">{BUDGET_ICONS.get(budget_display, "💳")}</div>
        <div class="metric-label">Budget</div>
        <div class="metric-value">{budget_display}</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">{STYLE_ICONS.get(style_display, "⚖️")}</div>
        <div class="metric-label">Travel Style</div>
        <div class="metric-value">{style_display}</div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── Researched Attractions ───────────────────────────────────
    if attractions:
        st.markdown(
            '<div class="section-header">🗺️ Researched Attractions</div>',
            unsafe_allow_html=True,
        )
        chips_html = ""
        for att in attractions:
            name = att.get("name", "Unknown")
            url = att.get("url", "")
            cat = att.get("category", "attraction").title()
            if url:
                chips_html += (
                    f'<span class="attraction-chip">'
                    f'📌 <a href="{url}" target="_blank" rel="noopener">{name}</a>'
                    f' <small>({cat})</small></span>'
                )
            else:
                chips_html += (
                    f'<span class="attraction-chip">📌 {name}'
                    f' <small>({cat})</small></span>'
                )
        st.markdown(chips_html, unsafe_allow_html=True)
        st.markdown("")
    else:
        st.info(
            "ℹ️ Live attraction research was unavailable for this destination. "
            "The itinerary below is based on the AI's general knowledge."
        )

    # ── Day-by-Day Itinerary ─────────────────────────────────────
    itinerary_md = result.get("itinerary", "")

    if itinerary_md:
        st.markdown(
            '<div class="section-header">🗓️ Your Itinerary</div>',
            unsafe_allow_html=True,
        )

        day_sections = split_itinerary_into_days(itinerary_md)

        if day_sections:
            for heading, body in day_sections:
                with st.expander(f"📌 {heading}", expanded=True):
                    st.markdown(body, unsafe_allow_html=False)
        else:
            # Fallback: render the entire markdown if splitting failed
            st.markdown(itinerary_md, unsafe_allow_html=False)

    else:
        st.warning("The agent returned an empty itinerary. Please try again.")

    # ── Actions ──────────────────────────────────────────────────
    st.markdown("---")
    col_new, col_dl = st.columns(2)

    with col_new:
        if st.button("🔄  Plan Another Trip", use_container_width=True):
            st.session_state.itinerary_result = None
            st.session_state.planning_error = None
            st.rerun()

    with col_dl:
        download_content = f"# {destination_display} — {days_display}-Day Itinerary\n\n"
        download_content += f"**Budget:** {budget_display}  |  **Style:** {style_display}\n\n"
        if attractions:
            download_content += "## Researched Attractions\n\n"
            for att in attractions:
                name = att.get("name", "Unknown")
                url = att.get("url", "")
                download_content += f"- [{name}]({url})\n" if url else f"- {name}\n"
            download_content += "\n"
        download_content += itinerary_md

        st.download_button(
            "📥  Download Itinerary (.md)",
            data=download_content,
            file_name=f"{destination_display.replace(' ', '_')}_itinerary.md",
            mime="text/markdown",
            use_container_width=True,
        )

# ═══════════════════════ Footer ══════════════════════════════════
st.markdown(
    """
<div class="app-footer">
    Personalized Holiday Management Agent &nbsp;·&nbsp;
    Powered by Groq, LangGraph & OpenStreetMap
</div>
""",
    unsafe_allow_html=True,
)
