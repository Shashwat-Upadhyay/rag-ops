"""Aurora Command Theme & Interactive UI Components for RAGOps.
A distinctive, high-end frontier interface combining executive elegance with
tactile micro-interactions, animated telemetry, and real-time observability.
"""
import json
from html import escape

import streamlit as st
import streamlit.components.v1 as components



def script_literal(value):
    """Serialize text safely for an inline script."""
    return json.dumps(str(value)).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def inject_executive_theme():
    """Injects the Aurora Command design system (Syne, Space Grotesk, glassmorphic aurora)."""
    st.markdown(
        """
        <style>

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
        @media (max-width: 768px) {
            .telemetry-strip { flex-wrap: wrap; }
            .msg-query, .msg-answer, .aurora-card { padding: 1rem; }
            h1 { font-size: 1.7rem !important; }
        }
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after { animation: none !important; transition: none !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_audio_briefing(text: str, element_id: str):
    """Renders a sleek voice briefing player with dynamic waveform equalizer."""
    escaped = script_literal(text)
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
                if (!('speechSynthesis' in window)) {{
                    document.getElementById('label-' + id).innerText = 'Speech unavailable in this browser';
                    return;
                }}
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

                const u = new SpeechSynthesisUtterance({escaped});
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
                    label.innerText = 'Playing Audio Briefing... (Click to Stop)';
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
        word = escape(str(t.get("term", "")))
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
    """Celebrate using bundled Streamlit assets."""
    st.balloons()


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
        const duration = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 1 : 900;
        const startTime = performance.now();
        function update(currentTime) {{
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const ease = 1 - Math.pow(1 - progress, 3);
            const current = (target * ease).toFixed({precision});
            document.getElementById('metric-val').innerText = current + {script_literal(suffix)};
            if (progress < 1) requestAnimationFrame(update);
        }}
        requestAnimationFrame(update);
        """
    else:
        js_counter = f"document.getElementById('metric-val').innerText = {script_literal(value)};"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
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
        <div class="label">{escape(str(label))}</div>
        <div class="value" id="metric-val">{escape(str(value))}</div>
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
            @media (prefers-reduced-motion: reduce) {{
              *, *::before, *::after {{ animation: none !important; transition: none !important; }}
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
    """Render an architecture overview without external scripts."""
    st.markdown("**Documents → Validation → Chunking → Retrieval index → Quality gate → API → Assistant**")
    st.caption("Queries feed audit logs and drift monitoring; retraining evaluates a candidate index before promotion.")
    with st.expander("Inspect architecture diagram source"):
        st.code(code, language="mermaid")
