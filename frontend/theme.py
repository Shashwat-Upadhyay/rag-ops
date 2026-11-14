"""Executive Dark Theme & Interactive UI Components for RAGOps.
Inspired by Linear, Vercel, and Perplexity Pro: Clean, tactile, high data density,
micro-interactions, and real-time observability.
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
    """Injects high-end, professional dark UI styling (Linear/Vercel inspired)."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        /* Color Palette (Zinc / Obsidian / Electric Accents) */
        :root {
            --bg-base: #09090b;
            --bg-surface: #121217;
            --bg-elevated: #18181f;
            --border-subtle: rgba(255, 255, 255, 0.07);
            --border-active: rgba(99, 102, 241, 0.35);
            --accent-indigo: #6366f1;
            --accent-violet: #8b5cf6;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --accent-rose: #f43f5e;
            --accent-sky: #0ea5e9;
            --text-primary: #f4f4f5;
            --text-secondary: #a1a1aa;
            --text-tertiary: #71717a;
        }

        /* Base Application Layout */
        .stApp {
            background-color: var(--bg-base);
            background-image:
                radial-gradient(ellipse at 50% -20%, rgba(99, 102, 241, 0.12), transparent 50%),
                radial-gradient(ellipse at 90% 100%, rgba(16, 185, 129, 0.05), transparent 40%),
                linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
            background-size: 100% 100%, 100% 100%, 32px 32px, 32px 32px;
            color: var(--text-primary);
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        /* Typography */
        h1, h2, h3, h4 {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.03em !important;
            color: var(--text-primary) !important;
        }

        p, span, label, div {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        code, pre, .stCode {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.88rem !important;
        }

        /* Linear-Style Surface Card */
        .pro-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.45);
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }
        .pro-card:hover {
            border-color: rgba(255, 255, 255, 0.14);
            box-shadow: 0 8px 30px -4px rgba(0, 0, 0, 0.6);
        }

        /* Command Ticker / Status Bar */
        .telemetry-strip {
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            padding: 0.65rem 1rem;
            margin-bottom: 1.5rem;
            align-items: center;
        }

        .metric-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            background: var(--bg-elevated);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 6px;
            padding: 0.3rem 0.65rem;
            font-size: 0.82rem;
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-secondary);
        }

        .metric-chip strong {
            color: var(--text-primary);
        }

        .status-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            display: inline-block;
        }
        .status-dot.online {
            background: var(--accent-emerald);
            box-shadow: 0 0 8px rgba(16, 185, 129, 0.6);
        }
        .status-dot.alert {
            background: var(--accent-rose);
            box-shadow: 0 0 8px rgba(244, 63, 94, 0.6);
        }

        /* Buttons & Inputs */
        .stButton>button {
            background: var(--bg-elevated) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 8px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            padding: 0.5rem 1.1rem !important;
            letter-spacing: -0.01em !important;
            transition: all 0.15s ease !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
        }

        .stButton>button:hover {
            background: #22222b !important;
            border-color: rgba(255, 255, 255, 0.2) !important;
            color: #ffffff !important;
            transform: translateY(-1px) !important;
        }

        .stButton>button:active {
            transform: translateY(0px) !important;
        }

        /* Chat Timeline Cards */
        .msg-query {
            background: linear-gradient(180deg, #16161e 0%, #111117 100%);
            border: 1px solid rgba(99, 102, 241, 0.25);
            border-left: 3px solid var(--accent-indigo);
            border-radius: 10px;
            padding: 1rem 1.25rem;
            margin: 0.75rem 0;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }

        .msg-answer {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            margin: 0.75rem 0 1.25rem 0;
            box-shadow: 0 6px 25px -4px rgba(0, 0, 0, 0.5);
        }

        /* Verification Badge */
        .badge-verified {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #34d399;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 5px;
        }

        .badge-warning {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(245, 158, 11, 0.1);
            border: 1px solid rgba(245, 158, 11, 0.3);
            color: #fbbf24;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 5px;
        }

        .badge-refusal {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(244, 63, 94, 0.1);
            border: 1px solid rgba(244, 63, 94, 0.3);
            color: #fb7185;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 5px;
        }

        /* Chunk Evidence Card */
        .chunk-card {
            background: var(--bg-elevated);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 0.85rem 1rem;
            margin-top: 0.6rem;
            font-size: 0.92rem;
            line-height: 1.5;
            transition: border-color 0.15s ease;
        }
        .chunk-card:hover {
            border-color: rgba(99, 102, 241, 0.3);
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0c0c0f !important;
            border-right: 1px solid var(--border-subtle) !important;
        }

        /* Metric Widgets */
        div[data-testid="stMetricValue"] {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 1.45rem !important;
            font-weight: 700 !important;
            color: var(--text-primary) !important;
            letter-spacing: -0.03em;
        }
        div[data-testid="stMetricLabel"] {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 0.82rem !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-tertiary) !important;
        }

        /* Scrollbars */
        ::-webkit-scrollbar {
            width: 7px;
            height: 7px;
        }
        ::-webkit-scrollbar-track {
            background: #09090b;
        }
        ::-webkit-scrollbar-thumb {
            background: #27272a;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #3f3f46;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_audio_briefing(text: str, element_id: str):
    """Renders a sleek, professional voice briefing player (ChatGPT/ElevenLabs style)."""
    escaped = text.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    components.html(
        f"""
        <div style="display: flex; align-items: center; gap: 8px; margin-top: 8px;">
            <button id="btn-{element_id}" onclick="toggleVoice('{element_id}')" style="
                display: inline-flex;
                align-items: center;
                gap: 7px;
                background: #18181f;
                border: 1px solid rgba(255, 255, 255, 0.08);
                color: #e4e4e7;
                padding: 6px 14px;
                border-radius: 6px;
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 0.82rem;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.15s ease;
            ">
                <span id="icon-{element_id}">▶️</span>
                <span id="label-{element_id}">Listen to Executive Voice Briefing</span>
            </button>
            <span id="wave-{element_id}" style="display: none; color: #6366f1; font-family: monospace; font-size: 0.8rem;">
                ● ● ●
            </span>
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
                    icon.innerText = '▶️';
                    label.innerText = 'Listen to Executive Voice Briefing';
                    wave.style.display = 'none';
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
                    icon.innerText = '⏸️';
                    label.innerText = 'Playing Audio Briefing... (Click to Pause)';
                    wave.style.display = 'inline';
                }};
                u.onend = u.onerror = () => {{
                    icon.innerText = '▶️';
                    label.innerText = 'Listen to Executive Voice Briefing';
                    wave.style.display = 'none';
                }};
                window.speechSynthesis.speak(u);
            }}
        </script>
        """,
        height=42,
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
        bg = "rgba(16, 185, 129, 0.15)" if is_pos else "rgba(244, 63, 94, 0.15)"
        border = "rgba(16, 185, 129, 0.35)" if is_pos else "rgba(244, 63, 94, 0.35)"
        color = "#34d399" if is_pos else "#fb7185"
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
                padding: 3px 8px;
                border-radius: 5px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.8rem;
                margin: 2px 4px 2px 0;
            ">
                <strong>{word}</strong> <span style="opacity: 0.75; font-size: 0.75rem;">{sign}{weight:.3f}</span>
            </span>
            """
        )

    st.markdown(
        f"""
        <div style="background: #14141a; border: 1px solid rgba(255, 255, 255, 0.06);
                    border-radius: 8px; padding: 0.85rem 1rem; margin-top: 0.5rem;">
            <div style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase;
                        color: #a1a1aa; margin-bottom: 0.4rem; letter-spacing: 0.05em;">
                Query Token Importance (LIME Surrogate Weights)
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
                    particleCount: 45,
                    spread: 60,
                    origin: { y: 0.65 },
                    colors: ['#6366f1', '#10b981', '#0ea5e9']
                });
            }
        </script>
        """,
        height=0,
    )


def render_mermaid_diagram(code: str, height: int = 560):
    """Renders a graphical Mermaid.js diagram with interactive drag-to-pan & zoom controls."""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <link rel="stylesheet"
            href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700&family=JetBrains+Mono:wght@500&display=swap">
      <style>
        body {{
          margin: 0;
          padding: 0;
          background: #0d0d12;
          color: #f4f4f5;
          font-family: 'Plus Jakarta Sans', sans-serif;
          box-sizing: border-box;
          border: 1px solid rgba(255, 255, 255, 0.08);
          border-radius: 12px;
          overflow: hidden;
          position: relative;
          height: {height}px;
          user-select: none;
        }}
        .toolbar {{
          position: absolute;
          top: 10px;
          right: 12px;
          display: flex;
          align-items: center;
          gap: 6px;
          z-index: 100;
          background: rgba(24, 24, 31, 0.92);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 7px;
          padding: 4px 6px;
          backdrop-filter: blur(8px);
        }}
        .toolbar button {{
          background: #18181f;
          color: #e4e4e7;
          border: 1px solid rgba(255, 255, 255, 0.08);
          border-radius: 5px;
          padding: 3px 9px;
          font-size: 0.78rem;
          font-weight: 600;
          cursor: pointer;
          font-family: 'JetBrains Mono', monospace;
          transition: all 0.15s ease;
        }}
        .toolbar button:hover {{
          background: #27272a;
          color: #ffffff;
          border-color: rgba(255, 255, 255, 0.2);
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
            background: '#0d0d12',
            mainBkg: '#16161e',
            nodeBorder: '#3f3f46',
            clusterBkg: '#101017',
            clusterBorder: '#27272a',
            titleColor: '#e4e4e7',
            textColor: '#f4f4f5',
            lineColor: '#6366f1',
            fontFamily: 'Plus Jakarta Sans, sans-serif',
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
        <span style="font-size: 0.72rem; color: #71717a; padding: 2px 6px; font-family: 'JetBrains Mono';">
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
