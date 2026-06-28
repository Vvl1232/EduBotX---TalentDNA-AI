import streamlit as st
import pandas as pd
import subprocess
import time
import os
import sys
import re

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
    margin-bottom: 0.75rem;
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
    run_clicked = st.button("Run Candidate Evaluation", key="lower_run_btn", type="primary", use_container_width=True)

if run_clicked or run_requested:
    # Reset the flag immediately to prevent loops on output interactions
    st.session_state.run_analysis = False
    
    # We must explicitly scroll for BOTH buttons to override Streamlit's native layout jumps.
    scroll_behavior = "smooth" if run_requested else "auto"
    st.components.v1.html(
        f"""
        <script>
            setTimeout(function() {{
                var el = window.parent.document.getElementById("benchmark");
                if (el) {{ el.scrollIntoView({{behavior: "{scroll_behavior}", block: "start"}}); }}
            }}, 50);
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
        selected_cand = st.selectbox("Select Candidate to view reasoning:", df["candidate_id"].tolist())

        # ──────────────────────────────────────────────────────────
        # COMPARISON HELPER FUNCTIONS (UI-only, zero backend coupling)
        # ──────────────────────────────────────────────────────────

        def _normalize_pct(val):
            """Convert a raw score value to a 0-100 percentage for bar display."""
            if val > 100:
                return min(100, max(0, (val / 1000) * 100))
            elif val > 1:
                return min(100, max(0, val))
            else:
                return min(100, max(0, val * 100))

        def _build_comparison_bullets(row_higher, row_lower, columns):
            """Generate recruiter-friendly bullet points from score deltas.

            Only mentions dimensions where the higher-ranked candidate scores
            better. Equal or unavailable dimensions are silently skipped.
            """
            bullet_map = {
                'semantic_score': '✓ Stronger semantic alignment with the Job Description',
                'role_alignment_score': '✓ Higher role relevance and alignment',
                'evidence_match_score': '✓ Stronger evidence supporting required skills',
                'behavioral_score': '✓ Better recruiter engagement signals',
                'integrity_score': '✓ Higher profile integrity score',
            }
            bullets = []
            for col, msg in bullet_map.items():
                if col in columns:
                    val_higher = float(row_higher[col])
                    val_lower = float(row_lower[col])
                    if val_higher > val_lower:
                        bullets.append(msg)
            return bullets

        def _parse_reasoning(reasoning_text):
            """Parse reasoning text into a list of individual reason sentences."""
            text = str(reasoning_text).strip()
            if text.endswith('.'):
                text = text[:-1]
            sentences = [s.strip().capitalize() for s in text.split('. ') if s.strip()]
            return sentences

        def _classify_reason(sentence):
            """Classify a reason sentence into a category for comparison."""
            s = sentence.lower()
            if 'years experience' in s or 'years' in s and 'experience' in s:
                return 'experience'
            elif 'retrieval' in s and 'expertise' in s:
                return 'retrieval_skills'
            elif 'applied ml' in s or 'ml experience' in s:
                return 'ml_skills'
            elif 'very strong alignment' in s:
                return 'alignment_very_strong'
            elif 'strong alignment' in s:
                return 'alignment_strong'
            elif 'partially aligned' in s:
                return 'alignment_partial'
            elif 'multiple signals of production' in s:
                return 'evidence_high'
            elif 'relevant ai' in s and 'evidence' in s:
                return 'evidence_medium'
            elif 'relevant engineering evidence' in s:
                return 'evidence_low'
            elif 'excellent recruiter' in s:
                return 'recruiter_excellent'
            elif 'strong recruiter' in s:
                return 'recruiter_strong'
            elif 'reasonable recruiter' in s:
                return 'recruiter_reasonable'
            elif 'skill portfolio' in s:
                return 'skill_portfolio'
            elif 'production engineering' in s:
                return 'production_bg'
            elif 'below ideal experience' in s:
                return 'exp_warning_low'
            elif 'more senior than' in s:
                return 'exp_warning_high'
            return 'other'

        # Category groupings for comparison
        _ALIGNMENT_LEVELS = {
            'alignment_very_strong': 3,
            'alignment_strong': 2,
            'alignment_partial': 1,
        }
        _EVIDENCE_LEVELS = {
            'evidence_high': 3,
            'evidence_medium': 2,
            'evidence_low': 1,
        }
        _RECRUITER_LEVELS = {
            'recruiter_excellent': 3,
            'recruiter_strong': 2,
            'recruiter_reasonable': 1,
        }

        def _build_detailed_comparison(row_a, row_b):
            """Build a detailed, self-explanatory comparison between two candidates.

            Returns (reasons_a, reasons_b, gaps, shared, missing) where:
              reasons_a: list of reason sentences for candidate A
              reasons_b: list of reason sentences for candidate B
              gaps: list of specific gap explanations (why A is ahead)
              shared: list of strengths both candidates share
              missing: list of what candidate B is missing compared to A
            """
            reasons_a = _parse_reasoning(row_a.get('reasoning', ''))
            reasons_b = _parse_reasoning(row_b.get('reasoning', ''))

            classified_a = {_classify_reason(r): r for r in reasons_a}
            classified_b = {_classify_reason(r): r for r in reasons_b}

            cats_a = set(classified_a.keys())
            cats_b = set(classified_b.keys())

            gaps = []
            shared = []
            missing = []

            # 1. Experience comparison
            exp_a = classified_a.get('experience', '')
            exp_b = classified_b.get('experience', '')
            if exp_a and exp_b:
                match_a = re.search(r'([\d.]+)\s*years?\s*experience\s+as\s+(.*)', exp_a, re.IGNORECASE)
                match_b = re.search(r'([\d.]+)\s*years?\s*experience\s+as\s+(.*)', exp_b, re.IGNORECASE)
                if match_a and match_b:
                    yrs_a = float(match_a.group(1))
                    yrs_b = float(match_b.group(1))
                    title_a = match_a.group(2).strip()
                    title_b = match_b.group(2).strip()
                    if yrs_a > yrs_b:
                        gaps.append(f"✓ More experience: {yrs_a} years (as {title_a}) vs {yrs_b} years (as {title_b})")
                        missing.append(f"Fewer years of experience ({yrs_b} vs {yrs_a})")
                    elif yrs_b > yrs_a:
                        pass  # Will be noted in the "other candidate" section
                    if title_a.lower() == title_b.lower():
                        shared.append(f"Both work as {title_a}")

            # 2. Retrieval / ML Skills comparison
            has_retrieval_a = 'retrieval_skills' in cats_a
            has_retrieval_b = 'retrieval_skills' in cats_b
            has_ml_a = 'ml_skills' in cats_a
            has_ml_b = 'ml_skills' in cats_b

            if has_retrieval_a and not has_retrieval_b:
                skill_text = classified_a['retrieval_skills']
                gaps.append(f"✓ Has retrieval/ranking expertise — \"{skill_text}\"")
                missing.append("Lacks explicit retrieval and ranking expertise")
                if has_ml_b:
                    gaps.append(f"✗ Other candidate has general ML experience instead — \"{classified_b['ml_skills']}\"")
                else:
                    gaps.append("✗ Other candidate shows no specialized retrieval or ML skills in reasoning")
            elif has_retrieval_a and has_retrieval_b:
                shared.append("Both demonstrate retrieval and ranking expertise")
            elif has_ml_a and not has_ml_b and not has_retrieval_b:
                gaps.append(f"✓ Has applied ML experience — \"{classified_a['ml_skills']}\"")
                missing.append("Lacks applied ML experience")
            elif not has_retrieval_a and not has_ml_a and (has_retrieval_b or has_ml_b):
                pass  # Other candidate has the skill advantage

            # 3. Alignment level comparison
            align_a = next((cat for cat in _ALIGNMENT_LEVELS if cat in cats_a), None)
            align_b = next((cat for cat in _ALIGNMENT_LEVELS if cat in cats_b), None)
            if align_a and align_b:
                level_a = _ALIGNMENT_LEVELS[align_a]
                level_b = _ALIGNMENT_LEVELS[align_b]
                if level_a > level_b:
                    gaps.append(f"✓ Stronger role alignment — \"{classified_a[align_a]}\" vs \"{classified_b[align_b]}\"")
                    missing.append(f"Lower role alignment (has \"{classified_b[align_b]}\")")
                elif level_a == level_b:
                    shared.append(f"Same role alignment level — \"{classified_a[align_a]}\"")

            # 4. Evidence level comparison
            ev_a = next((cat for cat in _EVIDENCE_LEVELS if cat in cats_a), None)
            ev_b = next((cat for cat in _EVIDENCE_LEVELS if cat in cats_b), None)
            if ev_a and ev_b:
                level_a = _EVIDENCE_LEVELS[ev_a]
                level_b = _EVIDENCE_LEVELS[ev_b]
                if level_a > level_b:
                    gaps.append(f"✓ Stronger evidence — \"{classified_a[ev_a]}\" vs \"{classified_b[ev_b]}\"")
                    missing.append(f"Weaker production evidence (has \"{classified_b[ev_b]}\")")
                elif level_a == level_b:
                    shared.append(f"Same production evidence level")
            elif ev_a and not ev_b:
                gaps.append(f"✓ Has production evidence — \"{classified_a[ev_a]}\"")
                missing.append("Lacks explicit production AI/ML evidence")

            # 5. Recruiter signals comparison
            rec_a = next((cat for cat in _RECRUITER_LEVELS if cat in cats_a), None)
            rec_b = next((cat for cat in _RECRUITER_LEVELS if cat in cats_b), None)
            if rec_a and rec_b:
                level_a = _RECRUITER_LEVELS[rec_a]
                level_b = _RECRUITER_LEVELS[rec_b]
                if level_a > level_b:
                    gaps.append(f"✓ Better recruiter signals — \"{classified_a[rec_a]}\" vs \"{classified_b[rec_b]}\"")
                    missing.append(f"Weaker recruiter engagement (has \"{classified_b[rec_b]}\")")
                elif level_a == level_b:
                    shared.append(f"Same recruiter engagement level")

            # 6. Skill portfolio
            if 'skill_portfolio' in cats_a and 'skill_portfolio' not in cats_b:
                gaps.append("✓ Has a strong skill portfolio (other candidate does not)")
                missing.append("Missing a strong skill portfolio signal")
            elif 'skill_portfolio' in cats_a and 'skill_portfolio' in cats_b:
                shared.append("Both have a strong skill portfolio")

            # 7. Experience range warnings
            if 'exp_warning_low' in cats_b and 'exp_warning_low' not in cats_a:
                gaps.append("✓ Within ideal experience range (other candidate is slightly below)")
                missing.append("Flagged as slightly below ideal experience range")
            if 'exp_warning_high' in cats_b and 'exp_warning_high' not in cats_a:
                gaps.append("✓ Within ideal experience range (other candidate is above target range)")
                missing.append("Flagged as being above the ideal target experience range")

            # 8. Score delta
            score_a = float(row_a['score'])
            score_b = float(row_b['score'])
            delta = score_a - score_b
            if delta > 0:
                gaps.append(f"✓ Higher composite score: {score_a:.2f} vs {score_b:.2f} (Δ {delta:.2f} points)")

            return reasons_a, reasons_b, gaps, shared, missing

        def _render_comparison_bar(label, val_a, val_b, rank_a, rank_b):
            """Render a side-by-side signal comparison bar in HTML."""
            pct_a = _normalize_pct(val_a)
            pct_b = _normalize_pct(val_b)

            return f"""<div style="margin-bottom: 1.25rem;">
                <div style="font-size: 0.85rem; font-weight: 700; color: #334155; margin-bottom: 0.5rem;">{label}</div>
                <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.3rem;">
                    <span style="font-size: 0.78rem; font-weight: 600; color: #4f46e5; min-width: 55px;">Rank {rank_a}</span>
                    <div style="flex: 1; height: 8px; background: rgba(99,102,241,.1); border-radius: 999px; overflow: hidden;">
                        <div style="height: 100%; width: {pct_a}%; background: linear-gradient(90deg, #6366f1, #8b5cf6); border-radius: 999px; transition: width 1s ease-out;"></div>
                    </div>
                    <span style="font-size: 0.78rem; font-weight: 700; color: #0f172a; min-width: 48px; text-align: right;">{val_a:.2f}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.6rem;">
                    <span style="font-size: 0.78rem; font-weight: 600; color: #8b5cf6; min-width: 55px;">Rank {rank_b}</span>
                    <div style="flex: 1; height: 8px; background: rgba(139,92,246,.1); border-radius: 999px; overflow: hidden;">
                        <div style="height: 100%; width: {pct_b}%; background: linear-gradient(90deg, #a78bfa, #c4b5fd); border-radius: 999px; transition: width 1s ease-out;"></div>
                    </div>
                    <span style="font-size: 0.78rem; font-weight: 700; color: #0f172a; min-width: 48px; text-align: right;">{val_b:.2f}</span>
                </div>
            </div>"""

        def _render_full_comparison(row_a, row_b, label_a, label_b, expander_key_suffix=""):
            """Render the full comparison panel between two candidate rows.

            row_a is the higher-ranked candidate, row_b is the lower-ranked one.
            """
            rank_a = int(row_a['rank'])
            rank_b = int(row_b['rank'])
            cand_id_a = row_a['candidate_id']
            cand_id_b = row_b['candidate_id']
            score_a = float(row_a['score'])
            score_b = float(row_b['score'])
            delta = score_a - score_b

            comparison_cols = {
                'semantic_score': 'Semantic Match',
                'role_alignment_score': 'Role Intelligence',
                'evidence_match_score': 'Evidence Match',
                'behavioral_score': 'Recruiter Signals',
                'integrity_score': 'Integrity',
            }

            reasons_a, reasons_b, gaps, shared, missing = _build_detailed_comparison(row_a, row_b)

            # ── Side-by-Side Candidate Cards ──
            col_left, col_right = st.columns(2)
            with col_left:
                st.markdown(
                    f"""
                    <div style="background: rgba(99,102,241,.04); border: 1px solid rgba(99,102,241,.18);
                                border-radius: 14px; padding: 1.1rem 1.25rem;">
                        <div style="font-size: 0.72rem; font-weight: 700; color: #4f46e5; text-transform: uppercase;
                                    letter-spacing: 0.06em; margin-bottom: 0.6rem;">{label_a}</div>
                        <div style="font-size: 1.6rem; font-weight: 900; background: linear-gradient(135deg, #4f46e5, #7c3aed);
                                    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.3rem;">#{rank_a}</div>
                        <div style="font-size: 0.88rem; font-weight: 600; color: #0f172a;">{cand_id_a}</div>
                        <div style="font-size: 0.8rem; color: #475569; margin-top: 0.2rem;">Score: <strong>{score_a:.2f}</strong></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_right:
                st.markdown(
                    f"""
                    <div style="background: rgba(139,92,246,.04); border: 1px solid rgba(139,92,246,.18);
                                border-radius: 14px; padding: 1.1rem 1.25rem;">
                        <div style="font-size: 0.72rem; font-weight: 700; color: #8b5cf6; text-transform: uppercase;
                                    letter-spacing: 0.06em; margin-bottom: 0.6rem;">{label_b}</div>
                        <div style="font-size: 1.6rem; font-weight: 900; background: linear-gradient(135deg, #8b5cf6, #a78bfa);
                                    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.3rem;">#{rank_b}</div>
                        <div style="font-size: 0.88rem; font-weight: 600; color: #0f172a;">{cand_id_b}</div>
                        <div style="font-size: 0.8rem; color: #475569; margin-top: 0.2rem;">Score: <strong>{score_b:.2f}</strong></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # ── What Each Candidate Demonstrates (side-by-side) ──
            reasons_col_l, reasons_col_r = st.columns(2)
            with reasons_col_l:
                reasons_a_html = "".join(
                    f'<div style="padding: 0.35rem 0; color: #1e293b; font-size: 0.88rem; display: flex; align-items: flex-start; gap: 0.5rem; '
                    f'border-bottom: 1px solid rgba(99,102,241,.08);">'
                    f'<span style="color: #4f46e5; font-weight: 700; flex-shrink: 0; margin-top: 1px;">•</span>'
                    f'<span>{r}</span></div>'
                    for r in reasons_a
                )
                st.markdown(
                    f"""
                    <div style="background: rgba(99,102,241,.02); border: 1px solid rgba(99,102,241,.12);
                                border-radius: 12px; padding: 1rem 1.1rem; margin-top: 1rem; height: 100%;">
                        <div style="font-size: 0.72rem; font-weight: 700; color: #4f46e5; text-transform: uppercase;
                                    letter-spacing: 0.06em; margin-bottom: 0.55rem;">What Rank #{rank_a} demonstrates</div>
                        {reasons_a_html}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with reasons_col_r:
                reasons_b_html = "".join(
                    f'<div style="padding: 0.35rem 0; color: #1e293b; font-size: 0.88rem; display: flex; align-items: flex-start; gap: 0.5rem; '
                    f'border-bottom: 1px solid rgba(139,92,246,.08);">'
                    f'<span style="color: #8b5cf6; font-weight: 700; flex-shrink: 0; margin-top: 1px;">•</span>'
                    f'<span>{r}</span></div>'
                    for r in reasons_b
                )
                st.markdown(
                    f"""
                    <div style="background: rgba(139,92,246,.02); border: 1px solid rgba(139,92,246,.12);
                                border-radius: 12px; padding: 1rem 1.1rem; margin-top: 1rem; height: 100%;">
                        <div style="font-size: 0.72rem; font-weight: 700; color: #8b5cf6; text-transform: uppercase;
                                    letter-spacing: 0.06em; margin-bottom: 0.55rem;">What Rank #{rank_b} demonstrates</div>
                        {reasons_b_html}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # ── Key Gaps — Why Rank #A is ahead ──
            if gaps:
                gaps_html = "".join(
                    f'<div style="padding: 0.4rem 0; color: #1e293b; font-size: 0.88rem; '
                    f'display: flex; align-items: flex-start; gap: 0.5rem; '
                    f'border-bottom: 1px solid rgba(0,0,0,.035);">'
                    f'<span style="color: {"#10b981" if g.startswith("✓") else "#ef4444"}; font-weight: 700; flex-shrink: 0; margin-top: 1px;">{g[:1]}</span>'
                    f'<span>{g[2:]}</span></div>'
                    for g in gaps
                )
                st.markdown(
                    f"""
                    <div style="background: rgba(255,255,255,.6); border: 1px solid rgba(16,185,129,.15);
                                border-left: 3px solid rgba(16,185,129,.5); border-radius: 12px;
                                padding: 1.1rem 1.3rem; margin-top: 1rem;">
                        <div style="font-size: 0.78rem; font-weight: 700; color: #047857; text-transform: uppercase;
                                    letter-spacing: 0.06em; margin-bottom: 0.65rem;">Key Gaps — Why Rank #{rank_a} is ahead</div>
                        {gaps_html}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # ── Shared Strengths and What's Missing (Side-by-Side) ──
            if shared or missing:
                share_col, miss_col = st.columns(2)
                
                with share_col:
                    if shared:
                        shared_html = "".join(
                            f'<div style="padding: 0.35rem 0; color: #475569; font-size: 0.88rem; display: flex; align-items: center; gap: 0.5rem; '
                            f'border-bottom: 1px solid rgba(0,0,0,.025);">'
                            f'<span style="color: #6366f1; flex-shrink: 0;">≡</span>'
                            f'<span>{s}</span></div>'
                            for s in shared
                        )
                        st.markdown(
                            f"""
                            <div style="background: rgba(99,102,241,.02); border: 1px solid rgba(99,102,241,.1);
                                        border-radius: 12px; padding: 1rem 1.2rem; margin-top: 0.75rem; height: 100%;">
                                <div style="font-size: 0.72rem; font-weight: 700; color: #6366f1; text-transform: uppercase;
                                            letter-spacing: 0.06em; margin-bottom: 0.5rem;">Shared Strengths</div>
                                {shared_html}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""
                            <div style="background: rgba(99,102,241,.02); border: 1px solid rgba(99,102,241,.1);
                                        border-radius: 12px; padding: 1rem 1.2rem; margin-top: 0.75rem; height: 100%;">
                                <div style="font-size: 0.72rem; font-weight: 700; color: #6366f1; text-transform: uppercase;
                                            letter-spacing: 0.06em; margin-bottom: 0.5rem;">Shared Strengths</div>
                                <div style="color: #64748b; font-size: 0.85rem; font-style: italic;">No specific shared strengths identified.</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                
                with miss_col:
                    if missing:
                        missing_html = "".join(
                            f'<div style="padding: 0.35rem 0; color: #475569; font-size: 0.88rem; display: flex; align-items: flex-start; gap: 0.5rem; '
                            f'border-bottom: 1px solid rgba(0,0,0,.025);">'
                            f'<span style="color: #ef4444; font-weight: 700; flex-shrink: 0; margin-top: 1px;">✗</span>'
                            f'<span>{m}</span></div>'
                            for m in missing
                        )
                        st.markdown(
                            f"""
                            <div style="background: rgba(239,68,68,.02); border: 1px solid rgba(239,68,68,.1);
                                        border-radius: 12px; padding: 1rem 1.2rem; margin-top: 0.75rem; height: 100%;">
                                <div style="font-size: 0.72rem; font-weight: 700; color: #ef4444; text-transform: uppercase;
                                            letter-spacing: 0.06em; margin-bottom: 0.5rem;">What Rank #{rank_b} is Missing</div>
                                {missing_html}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""
                            <div style="background: rgba(239,68,68,.02); border: 1px solid rgba(239,68,68,.1);
                                        border-radius: 12px; padding: 1rem 1.2rem; margin-top: 0.75rem; height: 100%;">
                                <div style="font-size: 0.72rem; font-weight: 700; color: #ef4444; text-transform: uppercase;
                                            letter-spacing: 0.06em; margin-bottom: 0.5rem;">What Rank #{rank_b} is Missing</div>
                                <div style="color: #64748b; font-size: 0.85rem; font-style: italic;">No specific missing signals identified.</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

            # ── Signal Comparison Bars ──
            signal_bars_html = ""
            for col, label in comparison_cols.items():
                if col in df.columns:
                    signal_bars_html += _render_comparison_bar(
                        label, float(row_a[col]), float(row_b[col]), rank_a, rank_b
                    )

            signal_bars_html += _render_comparison_bar(
                "Final Score", score_a, score_b, rank_a, rank_b
            )

            st.markdown(
                f"""<div style="background: rgba(255,255,255,.5); border: 1px solid rgba(99,102,241,.12);
                            border-radius: 12px; padding: 1.1rem 1.3rem; margin-top: 1rem;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #4f46e5; text-transform: uppercase;
                                letter-spacing: 0.06em; margin-bottom: 0.85rem;">Signal Comparison</div>
                    {signal_bars_html}
                </div>""",
                unsafe_allow_html=True,
            )

            # ── Recruiter Insight ──
            if delta < 1:
                gap_word = "marginal"
            elif delta < 5:
                gap_word = "small but measurable"
            elif delta < 15:
                gap_word = "moderate"
            else:
                gap_word = "significant"

            insight = (
                f"Rank #{rank_b} is a strong match for this role. "
                f"Rank #{rank_a} leads by {delta:.2f} points ({gap_word} gap). "
            )
            if gaps:
                insight += f"The gap is driven by {len(gaps)} identifiable difference{'s' if len(gaps) != 1 else ''} shown above."
            if shared:
                insight += f" Both candidates share {len(shared)} common strength{'s' if len(shared) != 1 else ''}."

            st.markdown(
                f"""
                <div style="background: rgba(99,102,241,.03); border: 1px solid rgba(99,102,241,.12);
                            border-radius: 12px; padding: 1.1rem 1.3rem; margin-top: 0.75rem;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #4f46e5; text-transform: uppercase;
                                letter-spacing: 0.06em; margin-bottom: 0.5rem;">Recruiter Insight</div>
                    <div style="font-size: 0.9rem; color: #334155; line-height: 1.65; font-style: italic;">
                        "{insight}"
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ──────────────────────────────────────────────────────────
        # CANDIDATE DRILL DOWN CONTENT
        # ──────────────────────────────────────────────────────────

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
                    pct = _normalize_pct(val)

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

            # ──────────────────────────────────────────────────────
            # SECTION 1: AUTO COMPARISON WITH RANK #1
            # ──────────────────────────────────────────────────────
            current_rank = int(cand_row['rank'])

            if current_rank == 1:
                st.markdown(
                    """
                    <div style="background: rgba(16,185,129,.04); border: 1px solid rgba(16,185,129,.18);
                                border-radius: 12px; padding: 1.2rem 1.5rem; margin-top: 1.5rem;
                                display: flex; align-items: center; gap: 0.75rem;">
                        <span style="font-size: 1.3rem;">🏆</span>
                        <div>
                            <div style="font-size: 0.85rem; font-weight: 700; color: #047857; text-transform: uppercase; letter-spacing: 0.05em;">
                                Comparison with Top Candidate
                            </div>
                            <div style="font-size: 0.95rem; color: #065f46; font-weight: 500; margin-top: 0.2rem;">
                                This is the highest ranked candidate. No comparison needed.
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                rank1_row = df[df['rank'] == 1]
                if not rank1_row.empty:
                    rank1_row = rank1_row.iloc[0]
                    rank1_id = rank1_row['candidate_id']

                    with st.expander(
                        f"🔻 Why This Candidate Ranked Lower — Compared with Rank #1 ({rank1_id})",
                        expanded=True
                    ):
                        _render_full_comparison(
                            rank1_row, cand_row,
                            label_a="Top Ranked Candidate (#1)",
                            label_b=f"Selected Candidate (#{current_rank})",
                        )

            # ──────────────────────────────────────────────────────
            # SECTION 2: COMPARE ANY TWO CANDIDATES
            # ──────────────────────────────────────────────────────
            st.markdown(
                '<div class="sec-head" style="margin-top:2.25rem">⚖️ Compare Any Two Candidates<div class="sh-line"></div></div>',
                unsafe_allow_html=True,
            )

            all_candidates = df["candidate_id"].tolist()
            cmp_col1, cmp_col2 = st.columns(2)
            with cmp_col1:
                cand_a_id = st.selectbox(
                    "Candidate A",
                    all_candidates,
                    index=0,
                    key="compare_cand_a",
                )
            with cmp_col2:
                default_b_idx = min(1, len(all_candidates) - 1)
                cand_b_id = st.selectbox(
                    "Candidate B",
                    all_candidates,
                    index=default_b_idx,
                    key="compare_cand_b",
                )

            if cand_a_id and cand_b_id:
                if cand_a_id == cand_b_id:
                    st.markdown(
                        """
                        <div style="background: rgba(245,158,11,.04); border: 1px solid rgba(245,158,11,.2);
                                    border-radius: 12px; padding: 1rem 1.3rem; margin-top: 0.5rem;
                                    display: flex; align-items: center; gap: 0.6rem;">
                            <span style="font-size: 1.1rem;">⚠️</span>
                            <span style="font-size: 0.92rem; color: #92400e; font-weight: 500;">
                                Please select two different candidates to compare.
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    row_a = df[df["candidate_id"] == cand_a_id].iloc[0]
                    row_b = df[df["candidate_id"] == cand_b_id].iloc[0]

                    # Always put the higher-ranked candidate first
                    if int(row_a['rank']) <= int(row_b['rank']):
                        higher_row, lower_row = row_a, row_b
                    else:
                        higher_row, lower_row = row_b, row_a

                    rank_h = int(higher_row['rank'])
                    rank_l = int(lower_row['rank'])

                    with st.expander(
                        f"📊 Rank #{rank_h} ({higher_row['candidate_id']}) vs Rank #{rank_l} ({lower_row['candidate_id']})",
                        expanded=True
                    ):
                        _render_full_comparison(
                            higher_row, lower_row,
                            label_a=f"Rank #{rank_h}",
                            label_b=f"Rank #{rank_l}",
                        )

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
    import urllib.parse
    
    repo_owner = "Vvl1232"
    repo_name = "EduBotX---TalentDNA-AI"
    pdf_filename = "TalentDNA AI - Methodology.pdf"
    
    # Generate the proper public RAW GitHub URL dynamically
    raw_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{urllib.parse.quote(pdf_filename)}"
    
    # Wrap in Google Docs Viewer to ensure native browser rendering with zoom/scroll and NO downloads
    viewer_url = f"https://docs.google.com/viewer?url={urllib.parse.quote(raw_url, safe='')}&embedded=true"
    

    modal_html = f"""
<!-- Methodology PDF Button -->
<a href="{viewer_url}" target="_blank" rel="noopener noreferrer" onclick="return handlePdfClick(event, this.href);" style="text-decoration:none;">
    <button style="width:100%;padding:14px;border-radius:12px;background:linear-gradient(135deg,#ef4444,#b91c1c);color:white;border:none;font-weight:700;cursor:pointer; transition: transform 0.2s, box-shadow 0.2s;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(239, 68, 68, 0.3)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
        Methodology PDF
    </button>
</a>

<!-- Fallback Modal Viewer -->
<div id="pdf-modal" style="display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(0,0,0,0.85); z-index:999999; opacity:0; transition:opacity 0.3s ease; align-items:center; justify-content:center; flex-direction:column;">
    <div style="width:100%; max-width:1200px; height:90vh; background:white; border-radius:12px; overflow:hidden; position:relative; display:flex; flex-direction:column; box-shadow:0 25px 50px -12px rgba(0,0,0,0.5);">
        <div style="padding:16px 24px; background:#f8fafc; border-bottom:1px solid #e2e8f0; display:flex; justify-content:space-between; align-items:center;">
            <h3 style="margin:0; font-family:Inter,sans-serif; color:#0f172a; font-size:1.1rem; font-weight:600;">Methodology PDF Viewer</h3>
            <button onclick="closePdfModal()" style="background:#ef4444; color:white; border:none; padding:8px 16px; border-radius:6px; cursor:pointer; font-weight:600; transition:background 0.2s;" onmouseover="this.style.background='#dc2626'" onmouseout="this.style.background='#ef4444'">Close</button>
        </div>
        <div style="flex-grow:1; position:relative; overflow:hidden;">
            <iframe id="pdf-iframe" style="width:100%; height:100%; border:none; overflow:auto;" src="about:blank"></iframe>
        </div>
    </div>
</div>

<!-- JavaScript Logic -->
<script>
function handlePdfClick(e, url) {{
    // Attempt to open the new tab
    var newTab = window.open(url, "_blank", "noopener,noreferrer");
    
    // Fallback: If popup is blocked or fails to open
    if (!newTab || newTab.closed || typeof newTab.closed === 'undefined') {{
        e.preventDefault();
        openPdfModal(url);
        return false;
    }}
    return true;
}}

function openPdfModal(url) {{
    var modal = document.getElementById("pdf-modal");
    var iframe = document.getElementById("pdf-iframe");
    iframe.src = url;
    modal.style.display = "flex";
    // Trigger reflow for smooth fade-in animation
    void modal.offsetWidth;
    modal.style.opacity = "1";
}}

function closePdfModal() {{
    var modal = document.getElementById("pdf-modal");
    modal.style.opacity = "0";
    setTimeout(function() {{
        modal.style.display = "none";
        document.getElementById("pdf-iframe").src = "about:blank"; // Stop background rendering
    }}, 300);
}}
</script>
"""
    st.markdown(modal_html, unsafe_allow_html=True)

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