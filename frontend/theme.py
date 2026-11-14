"""Aurora Command Theme & Interactive UI Components for RAGOps.
A distinctive, high-end frontier interface combining executive elegance with
tactile micro-interactions, animated telemetry, and real-time observability.
"""
import os
import sys

import streamlit as st
import streamlit.components.v1 as components

# Ensure local packages site-packages is on sys.path
_LOCAL_CACHE = (
    r"C:\Users\HP\AppData\Local\Packages"
    r"\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages"
)
if os.path.exists(_LOCAL_CACHE) and _LOCAL_CACHE not in sys.path:
    sys.path.append(_LOCAL_CACHE)


def inject_executive_theme():
    """Injects the Aurora Command design system (Syne, Space Grotesk, glassmorphic aurora)."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Syne:wght@600;700;800&display=swap');

        /* ── Aurora Command Design Tokens ───────────────────────────────── */
        :root {
            --bg-base: #060608;
            --bg-surface: #0c0c13;
            --bg-elevated: #13131e;
            --bg-overlay: rgba(18, 18, 28, 0.75);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-active: rgba(124, 58, 237, 0.45);
            --border-aurora: linear-gradient(135deg, rgba(124, 58, 237, 0.5), rgba(0, 212, 255, 0.5));
            --accent-violet: #7c3aed;
            --accent-cyan: #00d4ff;
            --accent-coral: #ff4d6d;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-tertiary: #64748b;
        }

        /* ── Background & Ambient Lighting ──────────────────────────────── */
        .stApp {
            background-color: var(--bg-base);
            background-image:
                radial-gradient(circle at 18% 10%, rgba(124, 58, 237, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 82% 85%, rgba(0, 212, 255, 0.08) 0%, transparent 45%),
                radial-gradient(circle at 92% 15%, rgba(255, 77, 109, 0.07) 0%, transparent 35%),
                linear-gradient(rgba(255, 255, 255, 0.012) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.012) 1px, transparent 1px);
            background-size: 100% 100%, 100% 100%, 100% 100%, 36px 36px, 36px 36px;
            color: var(--text-primary);
            font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        /* ── Typography Scale ───────────────────────────────────────────── */
        h1, h2, h3, h4 {
            font-family: 'Syne', sans-serif !important;
            font-weight: 800 !important;
            letter-spacing: -0.035em !important;
            color: var(--text-primary) !important;
        }

        p, span, label, div {
            font-family: 'Space Grotesk', sans-serif;
        }

        code, pre, .stCode {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.86rem !important;
        }

        .gradient-heading {
            background: linear-gradient(135deg, #ffffff 10%, #c084fc 45%, #00d4ff 90%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-family: 'Syne', sans-serif !important;
            font-weight: 800 !important;
            letter-spacing: -0.04em !important;
            margin: 0;
            display: inline-block;
        }

        /* ── High-Impact Bento & Aurora Cards ───────────────────────────── */
        .aurora-card {
            background: linear-gradient(145deg, rgba(19, 19, 30, 0.8), rgba(12, 12, 19, 0.9));
            border: 1px solid rgba(124, 58, 237, 0.35);
            border-radius: 14px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.6), 0 0 20px -3px rgba(124, 58, 237, 0.15);
            backdrop-filter: blur(14px);
            position: relative;
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        }
        .aurora-card:hover {
            border-color: rgba(0, 212, 255, 0.5);
            box-shadow: 0 14px 40px -5px rgba(0, 0, 0, 0.7), 0 0 25px -3px rgba(0, 212, 255, 0.25);
            transform: translateY(-2px);
        }

        .pro-card {
            background: rgba(12, 12, 19, 0.85);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 6px 24px -4px rgba(0, 0, 0, 0.55);
            backdrop-filter: blur(12px);
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }
        .pro-card:hover {
            border-color: rgba(255, 255, 255, 0.18);
            box-shadow: 0 10px 32px -4px rgba(0, 0, 0, 0.7);
        }

        /* ── Command Ticker / Status Bar ────────────────────────────────── */
        .telemetry-strip {
            display: flex;
            flex-wrap: wrap;
            gap: 0.65rem;
            background: rgba(12, 12, 19, 0.85);
            border: 1px solid rgba(124, 58, 237, 0.25);
            border-radius: 12px;
            padding: 0.75rem 1.15rem;
            margin-bottom: 1.5rem;
            align-items: center;
            box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(12px);
        }

        .metric-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(20, 20, 32, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 7px;
            padding: 0.35rem 0.75rem;
            font-size: 0.82rem;
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-secondary);
        }
        .metric-chip strong {
            color: var(--text-primary);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
        }
        .status-dot.online {
            background: #10b981;
            box-shadow: 0 0 10px #10b981;
        }
        .status-dot.alert {
            background: #ff4d6d;
            box-shadow: 0 0 10px #ff4d6d;
        }

        /* ── Buttons & Interactive Elements ─────────────────────────────── */
        .stButton>button {
            background: linear-gradient(145deg, #161624, #0f0f18) !important;
            color: var(--text-primary) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 8px !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            padding: 0.52rem 1.2rem !important;
            letter-spacing: -0.01em !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
        }
        .stButton>button:hover {
            background: linear-gradient(145deg, #222236, #161624) !important;
            border-color: rgba(124, 58, 237, 0.6) !important;
            color: #ffffff !important;
            box-shadow: 0 0 15px rgba(124, 58, 237, 0.3) !important;
            transform: translateY(-1.5px) !important;
        }
        .stButton>button:active {
            transform: translateY(0px) !important;
        }

        /* ── Chat Timeline Messages ─────────────────────────────────────── */
        .msg-query {
            background: linear-gradient(135deg, rgba(22, 22, 35, 0.85) 0%, rgba(15, 15, 24, 0.95) 100%);
            border: 1px solid rgba(124, 58, 237, 0.3);
            border-left: 4px solid var(--accent-violet);
            border-radius: 12px;
            padding: 1.1rem 1.4rem;
            margin: 0.85rem 0;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
        }

        .msg-answer {
            background: linear-gradient(145deg, rgba(15, 15, 24, 0.9) 0%, rgba(10, 10, 16, 0.95) 100%);
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 14px;
            padding: 1.35rem 1.6rem;
            margin: 0.85rem 0 1.35rem 0;
            box-shadow: 0 10px 30px -4px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.05);
            position: relative;
        }
        .msg-answer::before {
            content: '';
            position: absolute;
            top: 0;
            left: 20px;
            right: 20px;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(124, 58, 237, 0.6), rgba(0, 212, 255, 0.6), transparent);
        }

        /* ── Groundedness Badges ─────────────────────────────────────────── */
        .badge-verified {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.4);
            color: #34d399;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 6px;
            box-shadow: 0 0 12px rgba(16, 185, 129, 0.15);
        }

        .badge-warning {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(245, 158, 11, 0.12);
            border: 1px solid rgba(245, 158, 11, 0.4);
            color: #fbbf24;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 6px;
        }

        .badge-refusal {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255, 77, 109, 0.12);
            border: 1px solid rgba(255, 77, 109, 0.4);
            color: #ff4d6d;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 6px;
        }

        /* ── Chunk Evidence Card ────────────────────────────────────────── */
        .chunk-card {
            background: rgba(18, 18, 28, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 9px;
            padding: 0.95rem 1.15rem;
            margin-top: 0.65rem;
            font-size: 0.92rem;
            line-height: 1.55;
            transition: all 0.2s ease;
        }
        .chunk-card:hover {
            border-color: rgba(124, 58, 237, 0.4);
            background: rgba(22, 22, 34, 0.8);
        }

        /* ── Command Bar Input Override ─────────────────────────────────── */
        [data-testid="stChatInput"] {
            border-color: rgba(124, 58, 237, 0.35) !important;
            border-radius: 12px !important;
            background: rgba(12, 12, 19, 0.95) !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5) !important;
        }
        [data-testid="stChatInput"]:focus-within {
            border-color: rgba(0, 212, 255, 0.6) !important;
            box-shadow: 0 0 25px rgba(124, 58, 237, 0.3) !important;
        }

        /* ── Tabs Styling ───────────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            background-color: transparent;
        }
        .stTabs [data-baseweb="tab"] {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
            color: var(--text-secondary) !important;
            border-radius: 8px 8px 0 0 !important;
            padding: 8px 16px !important;
        }
        .stTabs [aria-selected="true"] {
            color: #ffffff !important;
            border-bottom: 2px solid var(--accent-violet) !important;
        }

        /* ── Sidebar Styling ────────────────────────────────────────────── */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #07070b 0%, #0a0a10 100%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        /* ── Scrollbars ─────────────────────────────────────────────────── */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #060608;
        }
        ::-webkit-scrollbar-thumb {
            background: #252538;
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #7c3aed;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_audio_briefing(text: str, element_id: str):
    """Renders a sleek voice briefing player with dynamic waveform equalizer."""
    escaped = text.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    components.html(
        f"""
        <style>
            @keyframes pulse-wave {{
                0%   {{ height: 4px; }}
                50%  {{ height: 16px; }}
                100% {{ height: 4px; }}
            }}
            .wave-bar {{
                display: inline-block;
                width: 3px;
                height: 4px;
                background: #00d4ff;
                border-radius: 2px;
                margin: 0 1px;
            }}
            .active-wave .w1 {{ animation: pulse-wave 0.6s infinite ease-in-out; }}
            .active-wave .w2 {{ animation: pulse-wave 0.8s infinite ease-in-out 0.2s; }}
            .active-wave .w3 {{ animation: pulse-wave 0.5s infinite ease-in-out 0.4s; }}
            .active-wave .w4 {{ animation: pulse-wave 0.7s infinite ease-in-out 0.1s; }}
        </style>
        <div style="display: flex; align-items: center; gap: 10px; margin-top: 10px;">
            <button id="btn-{element_id}" onclick="toggleVoice('{element_id}')" style="
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background: linear-gradient(145deg, #141422, #0d0d17);
                border: 1px solid rgba(124, 58, 237, 0.35);
                color: #f4f4f5;
                padding: 6px 14px;
                border-radius: 7px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.8rem;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
                box-shadow: 0 2px 8px rgba(0,0,0,0.4);
            ">
                <span id="icon-{element_id}" style="color: #00d4ff;">▶</span>
                <span id="label-{element_id}">Listen to Executive Voice Briefing</span>
            </button>
            <div id="wave-{element_id}" style="display: none; height: 16px; align-items: center;">
                <span class="wave-bar w1"></span>
                <span class="wave-bar w2"></span>
                <span class="wave-bar w3"></span>
                <span class="wave-bar w4"></span>
            </div>
        </div>
        <script>
            function toggleVoice(id) {{
                if (!('speechSynthesis' in window)) return;
                const btn = document.getElementById('btn-' + id);
                const icon = document.getElementById('icon-' + id);
                const label = document.getElementById('label-' + id);
                const wave = document.getElementById('wave-' + id);

                if (window.speechSynthesis.speaking) {{
                    window.speechSynthesis.cancel();
                    icon.innerText = '▶';
                    icon.style.color = '#00d4ff';
                    label.innerText = 'Listen to Executive Voice Briefing';
                    wave.style.display = 'none';
                    wave.classList.remove('active-wave');
                    return;
                }}

                const u = new SpeechSynthesisUtterance("{escaped}");
                u.rate = 1.0;
                u.pitch = 1.0;
                const voices = window.speechSynthesis.getVoices();
                const pref = voices.find(v => v.lang.includes('en') && (
                    v.name.includes('Natural') || v.name.includes('Google') ||
                    v.name.includes('Daniel') || v.name.includes('Samantha')
                ));
                if (pref) u.voice = pref;

                u.onstart = () => {{
                    icon.innerText = '⏸';
                    icon.style.color = '#ff4d6d';
                    label.innerText = 'Playing Audio Briefing... (Click to Pause)';
                    wave.style.display = 'flex';
                    wave.classList.add('active-wave');
                }};
                u.onend = u.onerror = () => {{
                    icon.innerText = '▶';
                    icon.style.color = '#00d4ff';
                    label.innerText = 'Listen to Executive Voice Briefing';
                    wave.style.display = 'none';
                    wave.classList.remove('active-wave');
                }};
                window.speechSynthesis.speak(u);
            }}
        </script>
        """,
        height=48,
    )


def render_token_influence_heatmap(terms: list[dict]):
    """Renders an interactive token heat-map with hoverable tokens and contribution bars."""
    if not terms:
        return

    chips_html = []
    for t in terms:
        word = t.get("term", "")
        weight = float(t.get("weight", 0.0))
        is_pos = weight >= 0
        bg = "rgba(16, 185, 129, 0.14)" if is_pos else "rgba(255, 77, 109, 0.14)"
        border = "rgba(16, 185, 129, 0.4)" if is_pos else "rgba(255, 77, 109, 0.4)"
        color = "#34d399" if is_pos else "#ff4d6d"
        sign = "+" if is_pos else ""

        chips_html.append(
            f"""
            <span style="
                display: inline-flex;
                align-items: center;
                gap: 5px;
                background: {bg};
                border: 1px solid {border};
                color: {color};
                padding: 3px 9px;
                border-radius: 6px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.82rem;
                margin: 2px 4px 2px 0;
            ">
                <strong>{word}</strong> <span style="opacity: 0.75; font-size: 0.74rem;">{sign}{weight:.3f}</span>
            </span>
            """
        )

    st.markdown(
        f"""
        <div style="background: rgba(14, 14, 22, 0.9); border: 1px solid rgba(124, 58, 237, 0.25);
                    border-radius: 10px; padding: 0.95rem 1.15rem; margin-top: 0.6rem;">
            <div style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase;
                        color: #c084fc; margin-bottom: 0.5rem; letter-spacing: 0.06em; font-family: 'Syne', sans-serif;">
                Query Token Influence (LIME Surrogate Weights)
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                {''.join(chips_html)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_confetti():
    """Subtle celebration particle feedback."""
    components.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
            if (window.confetti) {
                confetti({
                    particleCount: 50,
                    spread: 70,
                    origin: { y: 0.65 },
                    colors: ['#7c3aed', '#00d4ff', '#ff4d6d', '#10b981']
                });
            }
        </script>
        """,
        height=0,
    )


def render_animated_metric(
    label: str,
    value,
    accent_color: str | None = None,
    suffix: str = "",
    accent: str | None = None,
):
    """Renders a bento-style animated counter card with Syne numerals and easing."""
    color_palette = {
        "emerald": "#10b981",
        "violet": "#7c3aed",
        "cyan": "#00d4ff",
        "coral": "#ff4d6d",
        "amber": "#f59e0b",
        "rose": "#f43f5e",
        "indigo": "#6366f1",
    }
    raw_color = accent or accent_color or "#7c3aed"
    chosen_accent = color_palette.get(str(raw_color).lower(), raw_color)

    num_str = str(value).replace("ms", "").replace("%", "").strip()
    try:
        is_float = "." in num_str
        target_num = float(num_str)
    except ValueError:
        target_num = None

    js_counter = ""
    if target_num is not None:
        precision = 1 if is_float else 0
        js_counter = f"""
        let start = 0;
        const target = {target_num};
        const duration = 900;
        const startTime = performance.now();
        function update(currentTime) {{
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const ease = 1 - Math.pow(1 - progress, 3);
            const current = (target * ease).toFixed({precision});
            document.getElementById('metric-val').innerText = current + '{suffix}';
            if (progress < 1) requestAnimationFrame(update);
        }}
        requestAnimationFrame(update);
        """
    else:
        js_counter = f"document.getElementById('metric-val').innerText = '{value}';"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <link rel="stylesheet"
            href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@600&family=Space+Grotesk:wght@500;600&family=Syne:wght@800&display=swap">
      <style>
        body {{
          margin: 0;
          padding: 0;
          background: transparent;
          font-family: 'Space Grotesk', sans-serif;
          user-select: none;
        }}
        .card {{
          background: rgba(14, 14, 22, 0.85);
          border: 1px solid rgba(255, 255, 255, 0.08);
          border-left: 3px solid {chosen_accent};
          border-radius: 9px;
          padding: 10px 14px;
          box-sizing: border-box;
          box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
          transition: border-color 0.2s;
        }}
        .card:hover {{
          border-color: {chosen_accent};
        }}
        .label {{
          font-size: 0.72rem;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: #94a3b8;
          font-weight: 600;
          margin-bottom: 2px;
        }}
        .value {{
          font-family: 'Syne', sans-serif;
          font-size: 1.35rem;
          font-weight: 800;
          color: #f8fafc;
          letter-spacing: -0.02em;
        }}
      </style>
    </head>
    <body>
      <div class="card">
        <div class="label">{label}</div>
        <div class="value" id="metric-val">{value}</div>
      </div>
      <script>
        {js_counter}
      </script>
    </body>
    </html>
    """
    components.html(html_content, height=72)


def render_status_ring(is_online: bool):
    """Renders a live pulsing radar beacon widget."""
    color = "#10b981" if is_online else "#ff4d6d"
    text = "SYSTEM ONLINE" if is_online else "SYSTEM DEGRADED"
    components.html(
        f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <link rel="stylesheet"
                href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700&display=swap">
          <style>
            body {{
              margin: 0;
              padding: 0;
              background: transparent;
              display: flex;
              align-items: center;
              justify-content: flex-end;
              height: 48px;
              font-family: 'JetBrains Mono', monospace;
            }}
            .beacon-wrap {{
              display: inline-flex;
              align-items: center;
              gap: 10px;
              background: rgba(14, 14, 22, 0.85);
              border: 1px solid rgba(255, 255, 255, 0.08);
              padding: 5px 12px;
              border-radius: 20px;
              box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
            }}
            .radar-core {{
              position: relative;
              width: 10px;
              height: 10px;
            }}
            .radar-dot {{
              width: 10px;
              height: 10px;
              background: {color};
              border-radius: 50%;
              box-shadow: 0 0 10px {color};
            }}
            .radar-pulse {{
              position: absolute;
              top: -5px;
              left: -5px;
              width: 20px;
              height: 20px;
              border: 2px solid {color};
              border-radius: 50%;
              animation: ripple 1.6s ease-out infinite;
              opacity: 0;
            }}
            @keyframes ripple {{
              0%   {{ transform: scale(0.4); opacity: 1; }}
              100% {{ transform: scale(1.6); opacity: 0; }}
            }}
            .radar-text {{
              font-size: 0.72rem;
              font-weight: 700;
              color: {color};
              letter-spacing: 0.08em;
            }}
          </style>
        </head>
        <body>
          <div class="beacon-wrap">
            <div class="radar-core">
              <div class="radar-pulse"></div>
              <div class="radar-dot"></div>
            </div>
            <span class="radar-text">{text}</span>
          </div>
        </body>
        </html>
        """,
        height=48,
    )


def render_mermaid_diagram(code: str, height: int = 560):
    """Renders a graphical Mermaid.js diagram with interactive drag-to-pan & zoom controls."""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <link rel="stylesheet"
            href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@600&family=Space+Grotesk:wght@600&family=Syne:wght@700&display=swap">
      <style>
        body {{
          margin: 0;
          padding: 0;
          background: #09090f;
          color: #f8fafc;
          font-family: 'Space Grotesk', sans-serif;
          box-sizing: border-box;
          border: 1px solid rgba(124, 58, 237, 0.25);
          border-radius: 14px;
          overflow: hidden;
          position: relative;
          height: {height}px;
          user-select: none;
        }}
        .toolbar {{
          position: absolute;
          top: 12px;
          right: 14px;
          display: flex;
          align-items: center;
          gap: 6px;
          z-index: 100;
          background: rgba(15, 15, 24, 0.92);
          border: 1px solid rgba(255, 255, 255, 0.12);
          border-radius: 8px;
          padding: 4px 8px;
          backdrop-filter: blur(10px);
          box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        }}
        .toolbar button {{
          background: #141422;
          color: #e2e8f0;
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 6px;
          padding: 4px 10px;
          font-size: 0.78rem;
          font-weight: 600;
          cursor: pointer;
          font-family: 'JetBrains Mono', monospace;
          transition: all 0.15s ease;
        }}
        .toolbar button:hover {{
          background: #7c3aed;
          color: #ffffff;
          border-color: #7c3aed;
          box-shadow: 0 0 10px rgba(124, 58, 237, 0.4);
        }}
        #viewport {{
          width: 100%;
          height: 100%;
          cursor: grab;
          display: flex;
          justify-content: center;
          align-items: center;
          overflow: hidden;
        }}
        #viewport:active {{
          cursor: grabbing;
        }}
        #container {{
          transform-origin: center center;
          transition: transform 0.05s ease-out;
          width: 100%;
          display: flex;
          justify-content: center;
        }}
        .mermaid {{
          width: 95%;
          display: flex;
          justify-content: center;
        }}
        .mermaid svg {{
          max-width: 100% !important;
          height: auto !important;
        }}
      </style>
      <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
      <script>
        mermaid.initialize({{
          startOnLoad: true,
          theme: 'dark',
          themeVariables: {{
            darkMode: true,
            background: '#09090f',
            mainBkg: '#12121c',
            nodeBorder: '#3b3b54',
            clusterBkg: '#0d0d16',
            clusterBorder: '#27273a',
            titleColor: '#e2e8f0',
            textColor: '#f8fafc',
            lineColor: '#00d4ff',
            fontFamily: 'Space Grotesk, sans-serif',
            fontSize: '12px'
          }}
        }});

        let scale = 1.0;
        let pointX = 0;
        let pointY = 0;
        let start = {{ x: 0, y: 0 }};
        let isPanning = false;

        function updateTransform() {{
          const container = document.getElementById('container');
          container.style.transform = `translate(${{pointX}}px, ${{pointY}}px) scale(${{scale}})`;
        }}

        function zoom(delta) {{
          scale = Math.min(Math.max(0.4, scale + delta), 2.5);
          updateTransform();
        }}

        function resetView() {{
          scale = 1.0;
          pointX = 0;
          pointY = 0;
          updateTransform();
        }}

        window.addEventListener('DOMContentLoaded', () => {{
          const viewport = document.getElementById('viewport');

          viewport.addEventListener('mousedown', (e) => {{
            if (e.target.closest('.toolbar')) return;
            isPanning = true;
            start = {{ x: e.clientX - pointX, y: e.clientY - pointY }};
          }});

          window.addEventListener('mousemove', (e) => {{
            if (!isPanning) return;
            pointX = e.clientX - start.x;
            pointY = e.clientY - start.y;
            updateTransform();
          }});

          window.addEventListener('mouseup', () => {{
            isPanning = false;
          }});

          viewport.addEventListener('wheel', (e) => {{
            e.preventDefault();
            const delta = e.deltaY < 0 ? 0.08 : -0.08;
            zoom(delta);
          }}, {{ passive: false }});
        }});
      </script>
    </head>
    <body>
      <div class="toolbar">
        <button onclick="zoom(0.15)">＋ Zoom In</button>
        <button onclick="zoom(-0.15)">－ Zoom Out</button>
        <button onclick="resetView()">↺ Reset</button>
        <span style="font-size: 0.72rem; color: #94a3b8; padding: 2px 6px; font-family: 'JetBrains Mono';">
          Pan & Wheel Zoom
        </span>
      </div>
      <div id="viewport">
        <div id="container">
          <div class="mermaid">
            {code}
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    components.html(html_content, height=height + 20)
