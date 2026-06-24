import streamlit as st
import pandas as pd
import subprocess
import time
import os
import sys

# ──────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TalentDNA AI — EduBotX",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────────────────────────
# GLOBAL STYLES
# ──────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }
html {
    scroll-behavior: smooth;
    font-size: 19.5px !important;
}

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ── App background – light theme with indigo/violet radial glows ── */
.stApp {
    background:
        radial-gradient(ellipse 80% 40% at 15%  0%, rgba(99,102,241,.08) 0%, transparent 55%),
        radial-gradient(ellipse 60% 50% at 85% 100%, rgba(139,92,246,.08) 0%, transparent 55%),
        linear-gradient(180deg, #f8fafc 0%, #f1f5f9 60%, #e2e8f0 100%);
    min-height: 100vh;
    color: #0f172a;
}

/* ── Hide default chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 2.75rem 6rem !important;
    max-width: 1200px;
    margin: 0 auto;
}

/* ── Custom scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(99,102,241,.25);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,.5); }

/* ── Custom primary button styling ── */
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border: none !important;
    color: white !important;
    padding: 0.85rem 2.4rem !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3) !important;
}

/* ══════════════════════════════════════════
   NAV BAR
   ══════════════════════════════════════════ */
.nav-wrap {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
    padding: 1.35rem 0 1.1rem;
    border-bottom: 1px solid rgba(99,102,241,.12);
    margin-bottom: .5rem;
    animation: fadeDown .5s ease-out both;
}
.nav-logo {
    font-size: 1.15rem;
    font-weight: 900;
    letter-spacing: -.03em;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 55%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    white-space: nowrap;
}
.nav-center { display: flex; gap: 0.8rem; }
.nav-link {
    font-size: .8rem;
    font-weight: 600;
    color: #475569;
    text-decoration: none;
    letter-spacing: .04em;
    text-transform: uppercase;
    transition: color .2s;
    cursor: pointer;
}
.nav-link:hover { color: #4f46e5; }
.nav-badge {
    background: rgba(99,102,241,.08);
    border: 1px solid rgba(99,102,241,.2);
    border-radius: 999px;
    padding: .25rem .75rem;
    font-size: .68rem;
    font-weight: 700;
    color: #4f46e5;
    letter-spacing: .05em;
    white-space: nowrap;
}

/* ══════════════════════════════════════════
   HERO
   ══════════════════════════════════════════ */
.hero {
    text-align: center;
    padding: 4.5rem 2rem 3.5rem;
    position: relative;
    animation: fadeUp .8s ease-out .1s both;
}
.hero-glow {
    position: absolute;
    top: 8%; left: 50%;
    transform: translateX(-50%);
    width: 640px; height: 320px;
    background: radial-gradient(ellipse, rgba(99,102,241,.06) 0%, transparent 70%);
    pointer-events: none;
    animation: glowPulse 6s ease-in-out infinite;
}
.hero-eyebrow {
    display: inline-block;
    background: rgba(99,102,241,.08);
    border: 1px solid rgba(99,102,241,.2);
    border-radius: 999px;
    padding: .35rem 1.25rem;
    font-size: .8rem;
    font-weight: 700;
    color: #4f46e5;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-bottom: 1.6rem;
}
.hero-title {
    font-size: clamp(2.6rem, 5vw, 4.2rem);
    font-weight: 900;
    letter-spacing: -.04em;
    line-height: 1.04;
    margin: 0 0 1.3rem;
    background: linear-gradient(145deg, #0f172a 0%, #312e81 48%, #4f46e5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1.25rem;
    color: #334155;
    max-width: 820px;
    margin: 0 auto 2.0rem;
    line-height: 1.75;
    font-weight: 400;
}
.hero-chips {
    display: flex;
    justify-content: center;
    gap: 1.0rem;
    flex-wrap: wrap;
    margin-bottom: 2.25rem;
}
.hero-chip {
    background: rgba(255,255,255,.6);
    border: 1px solid rgba(99,102,241,.15);
    border-radius: 8px;
    padding: .4rem 1rem;
    font-size: .9rem;
    color: #475569;
    transition: all .2s ease;
    cursor: default;
}
.hero-chip:hover {
    background: rgba(255,255,255,.85);
    border-color: rgba(99,102,241,.35);
    color: #4f46e5;
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(99,102,241,.06);
}
    font-weight: 500;
    box-shadow: 0 2px 8px rgba(99,102,241,.04);
}

/* ── STATS ── */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.1rem;
    margin: 0 0 3rem;
    animation: fadeUp .9s ease-out .25s both;
}
.stat-card {
    background: rgba(255,255,255,.75);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(99,102,241,.16);
    border-radius: 18px;
    padding: 1.75rem 1.1rem 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    cursor: default;
    transition: all .35s cubic-bezier(.4,0,.2,1);
    box-shadow: 0 4px 20px -2px rgba(99,102,241,.06);
}
.stat-card::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(99,102,241,.04), transparent);
    opacity: 0;
    transition: opacity .3s;
}
.stat-card:hover {
    border-color: rgba(99,102,241,.35);
    transform: translateY(-6px);
    box-shadow: 0 20px 45px -10px rgba(99,102,241,.15);
}
.stat-card:hover::after { opacity: 1; }
.stat-shimmer {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #38bdf8);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform .45s ease;
}
.stat-card:hover .stat-shimmer { transform: scaleX(1); }
.stat-val {
    font-size: 2.3rem;
    font-weight: 800;
    letter-spacing: -.03em;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: .45rem;
}
.stat-lbl {
    font-size: .85rem;
    color: #475569;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .07em;
}

/* ══════════════════════════════════════════
   SECTION HEADER
   ══════════════════════════════════════════ */
.sec-head {
    display: flex;
    align-items: center;
    gap: .65rem;
    margin: 3.5rem 0 1.75rem;
    font-size: 1.65rem;
    font-weight: 800;
    color: #1e293b;
    letter-spacing: -.02em;
    animation: fadeLeft .55s ease-out both;
}
.sh-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(99,102,241,.28) 0%, transparent 100%);
    margin-left: .4rem;
}

/* ══════════════════════════════════════════
   PROBLEM
   ══════════════════════════════════════════ */
.problem-card {
    background: rgba(239,68,68,.02);
    border: 1px solid rgba(239,68,68,.14);
    border-left: 3px solid rgba(239,68,68,.55);
    border-radius: 16px;
    padding: 1.85rem 2.25rem;
    animation: fadeUp .65s ease-out both;
    box-shadow: 0 4px 18px rgba(239,68,68,.02);
}
.prob-label {
    font-size: .8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: #ef4444;
    margin-bottom: 1.1rem;
}
.prob-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: .55rem 3rem;
}
.prob-item {
    display: flex;
    align-items: flex-start;
    gap: .7rem;
    padding: .4rem 0;
    color: #334155;
    font-size: 1.05rem;
    line-height: 1.55;
    border-bottom: 1px solid rgba(0,0,0,.035);
}
.prob-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #ef4444;
    box-shadow: 0 0 7px rgba(239,68,68,.4);
    margin-top: .56rem;
    flex-shrink: 0;
}

/* ══════════════════════════════════════════
   PIPELINE
   ══════════════════════════════════════════ */
.pipeline-wrap {
    display: flex;
    align-items: flex-start;
    gap: 2.25rem;
    margin: 1.5rem 0;
    animation: fadeUp .7s ease-out both;
}
.pipe-col {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: stretch;
}
.pipe-step {
    background: rgba(255,255,255,.65);
    border: 1px solid rgba(99,102,241,.15);
    border-radius: 10px;
    padding: .75rem 1.35rem;
    margin: 3px 0;
    font-size: .98rem;
    font-weight: 500;
    color: #334155;
    display: flex;
    align-items: center;
    gap: .65rem;
    transition: all .25s ease;
    cursor: default;
    box-shadow: 0 2px 8px rgba(99,102,241,.03);
}
.pipe-step:hover {
    background: rgba(99,102,241,.06);
    border-color: rgba(99,102,241,.35);
    color: #4f46e5;
    transform: translateX(5px);
}
.pipe-num {
    font-size: .8rem;
    font-weight: 700;
    color: #4f46e5;
    font-family: 'JetBrains Mono', monospace;
    min-width: 1.6rem;
    text-align: right;
    opacity: .7;
}
.pipe-arrow {
    text-align: center;
    color: rgba(99,102,241,.28);
    font-size: .9rem;
    padding: 2px 0;
    line-height: 1;
    user-select: none;
}
.pipe-info {
    flex: 0 0 310px;
    background: rgba(99,102,241,.03);
    border: 1px solid rgba(99,102,241,.14);
    border-radius: 16px;
    padding: 1.75rem 1.6rem;
    display: flex;
    flex-direction: column;
    gap: 0;
    box-shadow: 0 4px 15px rgba(99,102,241,.02);
}
.pipe-info-title {
    font-size: .8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .09em;
    color: #4f46e5;
    margin-bottom: 1.1rem;
}
.pipe-fact {
    display: flex;
    gap: .7rem;
    padding: .7rem 0;
    font-size: .95rem;
    color: #334155;
    line-height: 1.55;
    border-bottom: 1px solid rgba(0,0,0,.035);
}
.pipe-fact:last-child { border-bottom: none; }
.pf-icon { flex-shrink: 0; }

/* ══════════════════════════════════════════
   INNOVATION CARDS
   ══════════════════════════════════════════ */
.innov-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.15rem;
    animation: fadeUp .7s ease-out both;
}
.innov-card {
    border-radius: 18px;
    padding: 1.75rem;
    border: 1px solid;
    transition: all .32s cubic-bezier(.4,0,.2,1);
    position: relative;
    overflow: hidden;
    cursor: default;
    background: rgba(255,255,255,.65);
    box-shadow: 0 4px 18px rgba(0,0,0,.02);
}
.innov-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(145deg, rgba(255,255,255,.4) 0%, transparent 55%);
    pointer-events: none;
}
.innov-card:hover {
    transform: translateY(-7px);
    box-shadow: 0 24px 50px -10px var(--cs);
}
.ic-green  { border-color: rgba(16,185,129,.18);  --cs: rgba(16,185,129,.08); background: rgba(16,185,129,.02); }
.ic-blue   { border-color: rgba(59,130,246,.18);  --cs: rgba(59,130,246,.08); background: rgba(59,130,246,.02); }
.ic-amber  { border-color: rgba(245,158,11,.18);  --cs: rgba(245,158,11,.06); background: rgba(245,158,11,.015); }
.ic-purple { border-color: rgba(139,92,246,.18);  --cs: rgba(139,92,246,.08); background: rgba(139,92,246,.02); }
.ic-green:hover  { border-color: rgba(16,185,129,.4); }
.ic-blue:hover   { border-color: rgba(59,130,246,.4); }
.ic-amber:hover  { border-color: rgba(245,158,11,.35); }
.ic-purple:hover { border-color: rgba(139,92,246,.4); }

.innov-head {
    display: flex;
    align-items: center;
    gap: .65rem;
    margin-bottom: 1rem;
}
.ic-icon { font-size: 1.55rem; }
.ic-name {
    font-size: 1.15rem;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -.01em;
    flex: 1;
}
.ic-badge {
    font-size: .7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .06em;
    padding: .2rem .65rem;
    border-radius: 5px;
}
.ic-green  .ic-badge { background: rgba(16,185,129,.1); color: #047857; }
.ic-blue   .ic-badge { background: rgba(59,130,246,.1); color: #1d4ed8; }
.ic-amber  .ic-badge { background: rgba(245,158,11,.1); color: #b45309; }
.ic-purple .ic-badge { background: rgba(139,92,246,.1); color: #6d28d9; }

.ic-list { list-style: none; padding: 0; margin: 0; }
.ic-list li {
    padding: .4rem 0;
    color: #475569;
    font-size: 1.0rem;
    display: flex;
    align-items: center;
    gap: .6rem;
    border-bottom: 1px solid rgba(0,0,0,.035);
    transition: color .2s;
}
.ic-list li:last-child { border-bottom: none; }
.innov-card:hover .ic-list li { color: #1e293b; }
.ic-list li::before {
    content: '';
    width: 5px; height: 5px;
    border-radius: 50%;
    flex-shrink: 0;
}
.ic-green  .ic-list li::before { background: #10b981; }
.ic-blue   .ic-list li::before { background: #3b82f6; }
.ic-amber  .ic-list li::before { background: #f59e0b; }
.ic-purple .ic-list li::before { background: #8b5cf6; }

/* ══════════════════════════════════════════
   BENCHMARK
   ══════════════════════════════════════════ */
.bench-card {
    background: rgba(99,102,241,.03);
    border: 1px solid rgba(99,102,241,.15);
    border-radius: 18px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.35rem;
    animation: fadeUp .7s ease-out both;
    box-shadow: 0 4px 15px rgba(99,102,241,.02);
}
.bench-tag {
    font-size: .85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: #4f46e5;
    margin-bottom: .45rem;
}
.bench-desc {
    color: #334155;
    font-size: 1.05rem;
    line-height: 1.65;
}
.bench-desc code {
    background: rgba(99,102,241,.08);
    border-radius: 4px;
    padding: .1rem .4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .9rem;
    color: #4f46e5;
}

/* ── Run button ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #7c3aed 100%) !important;
    color: #fff !important;
    border: 1px solid rgba(139,92,246,.3) !important;
    border-radius: 12px !important;
    padding: .85rem 2.2rem !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: .025em !important;
    width: 100% !important;
    transition: all .3s ease !important;
    box-shadow: 0 4px 22px rgba(99,102,241,.2) !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #4f46e5 0%, #6d28d9 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(99,102,241,.35) !important;
    border-color: rgba(139,92,246,.5) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Progress steps ── */
.prog-list { margin-top: 1.1rem; }
.prog-step {
    display: flex;
    align-items: center;
    gap: .8rem;
    padding: .65rem 1.2rem;
    border-radius: 9px;
    font-size: 1.0rem;
    margin: .28rem 0;
    transition: all .3s ease;
    border: 1px solid transparent;
}
.prog-step.pending { color: #475569; background: rgba(0,0,0,.015); border-color: rgba(0,0,0,.03); }
.prog-step.active  { color: #4f46e5; background: rgba(99,102,241,.06);    border-color: rgba(99,102,241,.18); }
.prog-step.done    { color: #047857; background: rgba(16,185,129,.05);   border-color: rgba(16,185,129,.18);  }
.prog-step.failed  { color: #ef4444; background: rgba(239,68,68,.05);    border-color: rgba(239,68,68,.18);  }
.prog-icon { min-width: 1.1rem; font-size: 1.05rem; }

.spinner-inline {
    display: inline-block;
    width: 0.95rem;
    height: 0.95rem;
    border: 2px solid rgba(79, 70, 229, 0.2);
    border-top-color: #4f46e5;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    vertical-align: middle;
}
@keyframes spin {
    to { transform: rotate(360deg); }
}

/* ── Success banner ── */
.success-banner {
    background: rgba(16,185,129,.05);
    border: 1px solid rgba(16,185,129,.18);
    border-radius: 11px;
    padding: .9rem 1.3rem;
    margin-top: 1.1rem;
    color: #047857;
    font-size: 1.0rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: .6rem;
}

/* ── DataFrame ── */
div[data-testid="stDataFrame"] > div {
    border-radius: 12px;
    border: 1px solid rgba(99,102,241,.14) !important;
    overflow: hidden;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: transparent !important;
    color: #4f46e5 !important;
    border: 1px solid rgba(99,102,241,.25) !important;
    border-radius: 10px !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    transition: all .25s ease !important;
}
.stDownloadButton > button:hover {
    background: rgba(99,102,241,.06) !important;
    border-color: rgba(99,102,241,.45) !important;
    transform: translateY(-1px) !important;
}

/* ══════════════════════════════════════════
   TECH STACK
   ══════════════════════════════════════════ */
.tech-row {
    display: flex;
    flex-wrap: wrap;
    gap: .65rem;
    margin: 1rem 0;
    animation: fadeUp .65s ease-out both;
}
.tech-pill {
    background: rgba(0,0,0,.015);
    border: 1px solid rgba(99,102,241,.14);
    border-radius: 999px;
    padding: .42rem 1rem;
    font-size: 0.9rem;
    font-weight: 500;
    color: #475569;
    font-family: 'JetBrains Mono', monospace;
    display: flex;
    align-items: center;
    gap: .5rem;
    transition: all .22s ease;
    cursor: default;
}
.tech-pill:hover {
    background: rgba(99,102,241,.06);
    border-color: rgba(99,102,241,.35);
    color: #4f46e5;
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(99,102,241,.08);
}

/* ══════════════════════════════════════════
   COMPLIANCE
   ══════════════════════════════════════════ */
.comply-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: .85rem;
    margin: 1rem 0;
    animation: fadeUp .65s ease-out both;
}
.comply-item {
    background: rgba(16,185,129,.03);
    border: 1px solid rgba(16,185,129,.16);
    border-radius: 11px;
    padding: .9rem 1.1rem;
    display: flex;
    align-items: center;
    gap: .65rem;
    color: #047857;
    font-size: 0.98rem;
    font-weight: 500;
    transition: all .25s ease;
    cursor: default;
}
.comply-item:hover {
    background: rgba(16,185,129,.06);
    border-color: rgba(16,185,129,.28);
}
.comply-check { color: #10b981; font-size: 1rem; flex-shrink: 0; }

/* ══════════════════════════════════════════
   DIVIDER
   ══════════════════════════════════════════ */
.div-line {
    border: none;
    border-top: 1px solid rgba(99,102,241,.12);
    margin: 2.75rem 0;
}

/* ══════════════════════════════════════════
   FOOTER
   ══════════════════════════════════════════ */
.footer {
    text-align: center;
    padding: 2.75rem 0 1.5rem;
    border-top: 1px solid rgba(99,102,241,.09);
}
.footer-logo {
    font-size: 1.15rem;
    font-weight: 900;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: .35rem;
}
.footer-sub { font-size: .85rem; color: #475569; }

/* ══════════════════════════════════════════
   KEYFRAMES
   ══════════════════════════════════════════ */
@keyframes glowPulse {
    0%, 100% { opacity: .55; transform: translateX(-50%) scale(1);    }
    50%       { opacity: 1;   transform: translateX(-50%) scale(1.12); }
}
@keyframes fadeDown {
    from { opacity: 0; transform: translateY(-14px); }
    to   { opacity: 1; transform: translateY(0);     }
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(22px); }
    to   { opacity: 1; transform: translateY(0);    }
}
@keyframes fadeLeft {
    from { opacity: 0; transform: translateX(-16px); }
    to   { opacity: 1; transform: translateX(0);     }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
.nav-link.active-nav {
    color: #4f46e5;
    position: relative;
}
.nav-link.active-nav::after {
    content: '';
    position: absolute;
    bottom: -4px; left: 0; right: 0; height: 2px;
    background: #4f46e5; border-radius: 2px;
}
.animate-on-scroll {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}
.animate-on-scroll.is-visible {
    opacity: 1;
    transform: translateY(0);
}
.fade-in-results {
    animation: fadeIn 1s ease-in-out both;
}
.error-card {
    background: rgba(239,68,68,.05); border: 1px solid rgba(239,68,68,.2);
    border-radius: 12px; padding: 1.5rem; margin-top: 1.5rem;
}
.error-title { color: #ef4444; font-weight: 700; font-size: 1.1rem; margin-bottom: .5rem; }
.error-details { color: #475569; font-size: 0.95rem; font-family: 'JetBrains Mono', monospace; }
</style>
""",
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────
# NAV BAR
# ──────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="nav-wrap">
  <span class="nav-logo">TalentDNA AI</span>
  <nav class="nav-center">
    <a href="#problem" class="nav-link">Constraints</a>
    <a href="#architecture" class="nav-link">Architecture</a>
    <a href="#innovation" class="nav-link">Capabilities</a>
    <a href="#benchmark-results" class="nav-link">Evaluation</a>
  </nav>
  <span class="nav-badge">Track One Candidate Discovery Challenge</span>
</div>
""",
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────
# HERO
# ──────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="hero">
  <div class="hero-glow"></div>
  <div class="hero-eyebrow">Track One Candidate Discovery Challenge</div>
  <div class="hero-title">Intelligent Candidate Discovery Engine</div>
  <div class="hero-sub">
    An offline candidate ranking system utilizing semantic vector embeddings,
    career progression analysis, and automated signal validation.
  </div>
  <div class="hero-chips">
    <span class="hero-chip">Vector Embeddings</span>
    <span class="hero-chip">Career Progression</span>
    <span class="hero-chip">Data Validation</span>
    <span class="hero-chip">Scoring Attribution</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

_, col_hero_btn, _ = st.columns([1, 1.8, 1])
with col_hero_btn:
    if st.button("Run Candidate Evaluation", key="hero_run_btn", type="primary", use_container_width=True):
        st.session_state.run_analysis = True

# ──────────────────────────────────────────────────────────────────
# STATS
# ──────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-val">100K</div>
    <div class="stat-lbl">Candidates Indexed</div>
    <div class="stat-shimmer"></div>
  </div>
  <div class="stat-card">
    <div class="stat-val">1,000</div>
    <div class="stat-lbl">Candidates Retrieved via FAISS</div>
    <div class="stat-shimmer"></div>
  </div>
  <div class="stat-card">
    <div class="stat-val">Top 100</div>
    <div class="stat-lbl">Ranked Candidates</div>
    <div class="stat-shimmer"></div>
  </div>
  <div class="stat-card">
    <div class="stat-val">CPU</div>
    <div class="stat-lbl">CPU-Only Scoring</div>
    <div class="stat-shimmer"></div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<hr class="div-line">', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────
# PROBLEM
# ──────────────────────────────────────────────────────────────────
st.markdown('<div id="problem"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sec-head">Candidate Discovery Challenges<div class="sh-line"></div></div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
<div class="problem-card">
  <div class="prob-label">Target challenges in profile indexing & filtering</div>
  <div class="prob-grid">
    <div class="prob-item"><div class="prob-dot"></div>High processing overhead on raw unstructured profiles</div>
    <div class="prob-item"><div class="prob-dot"></div>Omission of historical career growth and progression metrics</div>
    <div class="prob-item"><div class="prob-dot"></div>Exact-match queries fail to capture candidate expertise</div>
    <div class="prob-item"><div class="prob-dot"></div>Outdated or structural anomalies skew candidate distribution</div>
    <div class="prob-item"><div class="prob-dot"></div>Boilerplate text patterns inflate automated retrieval scores</div>
    <div class="prob-item"><div class="prob-dot"></div>Lack of transparent matching attribution in standard search</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────
# ARCHITECTURE
# ──────────────────────────────────────────────────────────────────
st.markdown('<div id="architecture"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sec-head">System Architecture<div class="sh-line"></div></div>',
    unsafe_allow_html=True,
)

_PIPE_STEPS = [
    ("01", "Candidate Dataset"),
    ("02", "Candidate Parser"),
    ("03", "Career Intelligence"),
    ("04", "Embedding Engine"),
    ("05", "FAISS Vector Retrieval"),
    ("06", "Role Intelligence"),
    ("07", "Evidence Match"),
    ("08", "Signal Engine"),
    ("09", "Integrity Engine"),
    ("10", "Hybrid Ranker"),
    ("11", "Explainability Layer"),
    ("12", "Top 100 Output"),
]

_pipe_html = '<div class="pipeline-wrap"><div class="pipe-col">'
for i, (n, lbl) in enumerate(_PIPE_STEPS):
    _pipe_html += f'<div class="pipe-step"><span class="pipe-num">{n}</span>{lbl}</div>'
    if i < len(_PIPE_STEPS) - 1:
        _pipe_html += '<div class="pipe-arrow">↓</div>'
_pipe_html += "</div>"
_pipe_html += """
<div class="pipe-info">
  <div class="pipe-info-title">Design Principles</div>
  <div class="pipe-fact"><span class="pf-icon">•</span>Multi-signal aggregation — aggregates semantic similarity, career history, and role-fit metrics into a single score.</div>
  <div class="pipe-fact"><span class="pf-icon">•</span>Data validation filters structural anomalies and boilerplate profiles during scoring.</div>
  <div class="pipe-fact"><span class="pf-icon">•</span>FAISS retrieval reduces candidates from 100K to 1,000 using vector search prior to detailed ranking.</div>
  <div class="pipe-fact"><span class="pf-icon">•</span>Scoring attribution extracts matching evidence and output logs for each ranked profile.</div>
  <div class="pipe-fact"><span class="pf-icon">•</span>Deterministic output — guarantees reproducible rank scores under identical search parameters.</div>
</div>
"""
_pipe_html += "</div>"
st.markdown(_pipe_html, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────
# CORE CAPABILITIES
# ──────────────────────────────────────────────────────────────────
st.markdown('<div id="innovation"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sec-head">Core Capabilities<div class="sh-line"></div></div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
<div class="innov-grid">

  <div class="innov-card ic-green">
    <div class="innov-head">
      <span class="ic-icon">◆</span>
      <span class="ic-name">Career History Analysis</span>
      <span class="ic-badge">Core</span>
    </div>
    <ul class="ic-list">
      <li>Current vs historical title alignment</li>
      <li>Experience depth and career progression</li>
      <li>Career trajectory keyword extraction</li>
      <li>Total experience duration verification</li>
    </ul>
  </div>

  <div class="innov-card ic-blue">
    <div class="innov-head">
      <span class="ic-icon">✦</span>
      <span class="ic-name">Latent Profile Retrieval</span>
      <span class="ic-badge">Retrieval</span>
    </div>
    <ul class="ic-list">
      <li>Identifies profiles via semantic matches instead of exact titles</li>
      <li>Dense vector representation search</li>
      <li>Detects career trajectory signals</li>
      <li>Aggregates non-standard matching indicators</li>
    </ul>
  </div>

  <div class="innov-card ic-amber">
    <div class="innov-head">
      <span class="ic-icon">■</span>
      <span class="ic-name">Data Validation &amp; Quality</span>
      <span class="ic-badge">Validation</span>
    </div>
    <ul class="ic-list">
      <li>Identifies and discounts outdated profile records</li>
      <li>Flags career sequences that do not align with direct-hire roles</li>
      <li>Flags boilerplate structure patterns</li>
    </ul>
  </div>

  <div class="innov-card ic-purple">
    <div class="innov-head">
      <span class="ic-icon">▲</span>
      <span class="ic-name">Scoring Attribution</span>
      <span class="ic-badge">Attribution</span>
    </div>
    <ul class="ic-list">
      <li>Evidence-backed score breakdown</li>
      <li>Role alignment metrics</li>
      <li>Weight distribution transparency</li>
      <li>Human-readable matching summaries</li>
    </ul>
  </div>

</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<hr class="div-line">', unsafe_allow_html=True)
# PERFORMANCE & COMPLIANCE
# ──────────────────────────────────────────────────────────────────
st.markdown('<div id="benchmark-results"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sec-head">System Performance & Compliance<div class="sh-line"></div></div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
<div class="stats-grid" style="grid-template-columns: repeat(4, 1fr); gap: 1rem;">
  <div class="stat-card">
    <div class="stat-val">100,000</div>
    <div class="stat-lbl">Candidates Indexed</div>
    <div class="stat-shimmer"></div>
  </div>
  <div class="stat-card">
    <div class="stat-val">1,000</div>
    <div class="stat-lbl">Candidates Retrieved via FAISS</div>
    <div class="stat-shimmer"></div>
  </div>
  <div class="stat-card">
    <div class="stat-val">Top 100</div>
    <div class="stat-lbl">Ranked Candidates</div>
    <div class="stat-shimmer"></div>
  </div>
  <div class="stat-card">
    <div class="stat-val">CPU-Only</div>
    <div class="stat-lbl">Execution Environment</div>
    <div class="stat-shimmer"></div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

_COMPLY = [
    "Runtime < 5 Minutes",
    "Memory < 16 GB",
    "CPU Only Execution",
    "No External Network Calls",
    "Deterministic Score Generation",
    "Top 100 Output Submission Format",
]
_items = "".join(
    f'<div class="comply-item"><span class="comply-check">✓</span>{lbl}</div>'
    for lbl in _COMPLY
)
st.markdown(f'<div class="comply-grid">{_items}</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────
# BENCHMARK
# ──────────────────────────────────────────────────────────────────
st.markdown('<div id="benchmark"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sec-head">Pipeline Demonstration<div class="sh-line"></div></div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
<div class="bench-card">
  <div class="bench-tag">Official Pipeline Configuration</div>
  <div class="bench-desc">
    Executes the candidate ranking pipeline against the target job description and profile dataset.
    Outputs a ranked <code>submission.csv</code> containing the top 100 candidates with explainability scores.
  </div>
</div>
""",
    unsafe_allow_html=True,
)

_BENCH_STEPS = [
    ("[1]", "Loading Candidates"),
    ("[2]", "Parsing Profiles"),
    ("[3]", "Extracting Career Features"),
    ("[4]", "Loading Embedding Model"),
    ("[5]", "FAISS Vector Retrieval"),
    ("[6]", "Evidence Validation"),
    ("[7]", "Recruiter Signal Analysis"),
    ("[8]", "Integrity Screening"),
    ("[9]", "Hybrid Ranking"),
    ("[10]", "Generating Explanations"),
    ("[11]", "Top 100 Output Ready"),
]


def _render_pipeline_state(states, error_msg=None) -> str:
    html = '<div class="prog-list">'
    for i, (icon, label) in enumerate(_BENCH_STEPS):
        state = states[i] if i < len(states) else "pending"
        
        extra = ""
        if state == "completed":
            cls, marker = "done", "✓"
        elif state == "running":
            cls, marker = "active", '<div class="spinner-inline"></div>'
        elif state == "failed":
            cls, marker = "failed", "✗"
            if error_msg and i == len(states) - 1:
                extra = f'<div style="color: #ef4444; font-size: 0.85rem; margin-top: 0.4rem; padding-left: 2rem;">{error_msg}</div>'
        else:
            cls, marker = "pending", "○"
            
        html += (
            f'<div class="prog-step {cls}">'
            f'<div><span class="prog-icon">{marker}</span>'
            f'{icon}&nbsp; {label}</div>'
            f'{extra}'
            f"</div>"
        )
    html += "</div>"
    return html


# Check if analysis is requested via URL query param
run_requested = False
if st.query_params.get("run") == "true":
    run_requested = True
    st.query_params.clear()

if st.session_state.get("run_analysis", False):
    run_requested = True

_, col_run, _ = st.columns([1, 2, 1])
with col_run:
    run_clicked = st.button("Run Candidate Evaluation", type="primary", use_container_width=True)

if run_clicked or run_requested:
    # Reset the flag immediately to prevent loops on output interactions
    st.session_state.run_analysis = False
    
    # Ensure the viewport scrolls to the benchmark section
    st.components.v1.html(
        """
        <script>
            setTimeout(function() {
                var el = window.parent.document.getElementById("benchmark");
                if (el) { el.scrollIntoView({behavior: "smooth"}); }
            }, 150);
        </script>
        """,
        height=0,
    )
    init_slot = st.empty()
    init_slot.markdown(
        f'<div style="font-weight: 600; color: #4f46e5; text-align: center; margin: 1rem 0; font-size: 1.1rem;">'
        f'<div class="spinner-inline" style="margin-right: 10px;"></div>Initializing TalentDNA AI Pipeline...</div>',
        unsafe_allow_html=True
    )

    prog_slot = st.empty()
    states = ["pending"] * len(_BENCH_STEPS)
    prog_slot.markdown(_render_pipeline_state(states), unsafe_allow_html=True)

    error_output = []
    process = subprocess.Popen(
        [
            sys.executable, "-u", "rank.py",
            "--candidates", "data/raw/candidates.jsonl",
            "--jd",         "data/raw/job_description.docx",
            "--out",        "submission.csv",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    current_stage = -1
    first_output = True
    captured_error = None
    captured_tb = None
    
    while True:
        line = process.stdout.readline()
        if first_output and line:
            init_slot.empty()
            first_output = False
            
        if not line and process.poll() is not None:
            break
        if line:
            line_str = line.strip()
            if line_str.startswith("LOG:"):
                print(line_str)
            elif line_str.startswith("TRACEBACK:"):
                captured_tb = line_str.split("TRACEBACK:", 1)[1]
            elif line_str.startswith("STAGE:"):
                parts = line_str.split(":")
                if len(parts) >= 3:
                    stage_num = int(parts[1]) - 1
                    action = parts[2]
                    
                    if action == "START":
                        states[stage_num] = "running"
                        current_stage = stage_num
                    elif action == "END":
                        states[stage_num] = "completed"
                    elif action == "ERROR":
                        states[stage_num] = "failed"
                        err_type = parts[3] if len(parts) > 3 else "Unknown"
                        err_msg = ":".join(parts[4:]) if len(parts) > 4 else ""
                        captured_error = {"stage": stage_num + 1, "type": err_type, "msg": err_msg}
                    
                    prog_slot.markdown(_render_pipeline_state(states), unsafe_allow_html=True)
            else:
                if line_str:
                    error_output.append(line_str)
    
    if process.returncode != 0:
        if current_stage >= 0 and current_stage < len(states):
            states[current_stage] = "failed"
        elif len(states) > 0:
            states[0] = "failed"
        
        if captured_error and captured_tb:
            tb_html = captured_tb.replace('<br>', '\n')
            err_html = f"""
            <div class="error-card">
              <div class="error-title">Stage {captured_error['stage']} Failed: {captured_error['type']}</div>
              <div class="error-details">{captured_error['msg']}</div>
              <details style="margin-top: 1rem; cursor: pointer;">
                <summary style="font-weight: 600; color: #ef4444;">View Full Traceback</summary>
                <pre style="background: rgba(0,0,0,0.05); padding: 1rem; border-radius: 8px; margin-top: 0.5rem; font-size: 0.85rem; overflow-x: auto;">{tb_html}</pre>
              </details>
            </div>
            """
            prog_slot.markdown(_render_pipeline_state(states, f"Stage {captured_error['stage']} failed."), unsafe_allow_html=True)
            st.markdown(err_html, unsafe_allow_html=True)
        else:
            err_msg = "<br>".join(error_output[-5:])
            prog_slot.markdown(_render_pipeline_state(states, err_msg), unsafe_allow_html=True)
            st.markdown(f'<div class="error-card"><div class="error-title">System Error Detected</div><div class="error-details">{err_msg}</div><div style="margin-top:1rem;color:#334155;">Please verify dataset paths or contact support.</div></div>', unsafe_allow_html=True)
    else:
        loading_slot = st.empty()
        messages = [
            "Generating Ranked Results...",
            "Preparing Candidate Insights...",
            "Loading Dashboard..."
        ]
        
        for msg in messages:
            loading_slot.markdown(
                f'<div style="font-weight: 600; color: #4f46e5; text-align: center; margin: 2rem 0; font-size: 1.1rem;">'
                f'<div class="spinner-inline" style="margin-right: 10px;"></div>{msg}</div>',
                unsafe_allow_html=True
            )
            time.sleep(1.2)
            
        loading_slot.empty()
        st.session_state.pipeline_complete = True
        prog_slot.empty()

if st.session_state.get("pipeline_complete", False):
    st.markdown(_render_pipeline_state(["completed"] * len(_BENCH_STEPS)), unsafe_allow_html=True)
    st.markdown(
        '<div class="success-banner">✓&nbsp; Pipeline complete — output submission.csv generated.</div>',
        unsafe_allow_html=True,
    )

    if os.path.exists("submission.csv"):
        df = pd.read_csv("submission.csv")

        st.markdown(
            '<div class="sec-head" style="margin-top:2.25rem">🏅 Top 10 Candidates<div class="sh-line"></div></div>',
            unsafe_allow_html=True,
        )
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)

        st.markdown(
            '<div class="sec-head" style="margin-top:2.25rem">🔍 Candidate Drill Down<div class="sh-line"></div></div>',
            unsafe_allow_html=True,
        )
        selected_cand = st.selectbox("Select Candidate to view reasoning:", df.head(10)["candidate_id"].tolist())
        if selected_cand:
            cand_row = df[df["candidate_id"] == selected_cand].iloc[0]
            
            score_cols = {
                'semantic_score': 'Semantic Score',
                'role_alignment_score': 'Role Alignment Score',
                'evidence_match_score': 'Evidence Match Score',
                'behavioral_score': 'Behavioral / Recruiter Signal Score',
                'integrity_score': 'Integrity Score',
                'score': 'Final Score'
            }
            
            summary_html = f"""
            <div style="background: rgba(99,102,241,.03); border: 1px solid rgba(99,102,241,.15); border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 0.85rem; font-weight: 700; color: #4f46e5; text-transform: uppercase; letter-spacing: 0.05em;">Candidate Summary</div>
                        <div style="font-size: 1.4rem; font-weight: 800; color: #0f172a;">{cand_row['candidate_id']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 0.85rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em;">Rank</div>
                        <div style="font-size: 2rem; font-weight: 900; background: linear-gradient(135deg, #4f46e5, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">#{cand_row['rank']}</div>
                    </div>
                </div>
            </div>
            """
            st.markdown(summary_html, unsafe_allow_html=True)
            
            st.markdown('<div style="font-size: 1rem; font-weight: 600; color: #334155; margin-bottom: 1rem;">Ranking signals contributing to the final recommendation</div>', unsafe_allow_html=True)
            
            for col, label in score_cols.items():
                if col in df.columns:
                    val = float(cand_row[col])
                    if val > 100:
                        pct = min(100, max(0, (val / 1000) * 100))
                    elif val > 1:
                        pct = min(100, max(0, val))
                    else:
                        pct = min(100, max(0, val * 100))
                    
                    bar_html = f"""
                    <div style="margin-bottom: 1rem;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                            <span style="font-size: 0.9rem; font-weight: 600; color: #475569;">{label}</span>
                            <span style="font-size: 0.9rem; font-weight: 700; color: #0f172a;">{val:.2f}</span>
                        </div>
                        <div style="height: 8px; background: rgba(99,102,241,.1); border-radius: 999px; overflow: hidden;">
                            <div style="height: 100%; width: {pct}%; background: linear-gradient(90deg, #6366f1, #8b5cf6); border-radius: 999px; transition: width 1s ease-out;"></div>
                        </div>
                    </div>
                    """
                    st.markdown(bar_html, unsafe_allow_html=True)
                    
            reasoning_html = f"""
            <div style="background: rgba(255,255,255,.6); border: 1px solid rgba(99,102,241,.15); border-radius: 12px; padding: 1.2rem; margin-top: 1.5rem;">
                <div style="font-size: 0.85rem; font-weight: 700; color: #4f46e5; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Reasoning</div>
                <div style="font-size: 0.9rem; color: #334155; line-height: 1.6;">
                    {cand_row['reasoning']}
                </div>
            </div>
            """
            st.markdown(reasoning_html, unsafe_allow_html=True)

        with open("submission.csv", "rb") as _f:
            st.download_button(
                "⬇  Download Full Submission (CSV)",
                _f,
                file_name="submission.csv",
                mime="text/csv",
                use_container_width=True,
            )

st.markdown('<hr class="div-line">', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────
# PROJECT LINKS
# ──────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-head">Project Resources<div class="sh-line"></div></div>', unsafe_allow_html=True)

pl1, pl2 = st.columns(2)
with pl1:
    st.markdown(
        '<a href="https://github.com/Vvl1232/EduBotX---TalentDNA-AI" target="_blank">'
        '<button style="width:100%;padding:14px;border-radius:12px;background:linear-gradient(135deg,#333,#000);color:white;border:none;font-weight:700;cursor:pointer;">'
        'Source Code (GitHub)'
        '</button></a>', 
        unsafe_allow_html=True
    )
with pl2:
    # Use jsDelivr CDN to serve the PDF directly from the repo.
    # This guarantees 'Content-Type: application/pdf' is sent, 
    # forcing the browser to open it natively in a new tab instead of downloading.
    pdf_url = "https://cdn.jsdelivr.net/gh/Vvl1232/EduBotX---TalentDNA-AI@main/TalentDNA%20AI%20-%20Methodology.pdf"
    
    st.markdown(
        f'<a href="{pdf_url}" target="_blank" rel="noopener noreferrer">'
        '<button style="width:100%;padding:14px;border-radius:12px;background:linear-gradient(135deg,#ef4444,#b91c1c);color:white;border:none;font-weight:700;cursor:pointer;">'
        'Methodology PDF'
        '</button></a>', 
        unsafe_allow_html=True
    )

# ──────────────────────────────────────────────────────────────────
# TEAM EDUBOTX
# ──────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-head" style="margin-top:3rem;">Team EduBotX<div class="sh-line"></div></div>', unsafe_allow_html=True)

t1, t2, t3 = st.columns(3)
with t1:
    st.info("**Vinit Limkar**\n\nTeam Lead / AIML Engineer\n\n*SKNCOE Pune*")
with t2:
    st.info("**Sarah Khambatta**\n\nDevOps & Full Stack\n\n*SKNCOE Pune*")
with t3:
    st.info("**Shreyash Date**\n\nFull Stack Developer\n\n*SKNCOE Pune*")

st.markdown(
    """
<div class="footer">
  <div class="footer-logo">TalentDNA AI</div>
  <div class="footer-sub">Intelligent Candidate Discovery Engine</div>
</div>
""",
    unsafe_allow_html=True,
)

st.components.v1.html(
    """
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        const sections = window.parent.document.querySelectorAll('div[id]');
        const navLinks = window.parent.document.querySelectorAll('.nav-link');
        
        const observerOptions = { root: null, rootMargin: '0px', threshold: 0.5 };
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.getAttribute('id');
                    navLinks.forEach(link => {
                        link.classList.remove('active-nav');
                        if (link.getAttribute('href') === '#' + id) {
                            link.classList.add('active-nav');
                        }
                    });
                }
            });
        }, observerOptions);
        
        sections.forEach(sec => observer.observe(sec));
        
        const animObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                }
            });
        }, { threshold: 0.1 });
        
        const applyAnimations = () => {
            window.parent.document.querySelectorAll('.bench-card, .sec-head, .problem-card, .innov-card, .stat-card, .success-banner, .error-card, div[data-testid="stDataFrame"]').forEach(el => {
                if (!el.classList.contains('animate-on-scroll')) {
                    el.classList.add('animate-on-scroll');
                    animObserver.observe(el);
                }
            });
        };
        applyAnimations();
        
        const buttons = window.parent.document.querySelectorAll('button[kind="primary"]');
        buttons.forEach(btn => {
            btn.addEventListener('click', function(e) {
                const bench = window.parent.document.getElementById('benchmark-results');
                if (bench) {
                    bench.scrollIntoView({behavior: "smooth"});
                }
                
                btn.style.opacity = '0.5';
                btn.style.pointerEvents = 'none';
                
                setTimeout(() => applyAnimations(), 2000);
            });
        });
        
        const mutationObserver = new MutationObserver((mutations) => {
            let shouldApply = false;
            mutations.forEach(m => { if (m.addedNodes.length > 0) shouldApply = true; });
            if (shouldApply) applyAnimations();
        });
        mutationObserver.observe(window.parent.document.body, { childList: true, subtree: true });
    });
    </script>
    """,
    height=0,
)