import streamlit as st
import yfinance as yf
import feedparser
import math
from datetime import datetime

# 1. Configuration Interface Compacte
st.set_page_config(page_title="BEE-INVEST | DASHBOARD", layout="wide", initial_sidebar_state="collapsed")

# CSS "Micro-Design" pour tout faire tenir
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    /* Réduction drastique des espaces Streamlit */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; padding: 10px; border-radius: 4px; margin-bottom: 8px; }
    .label { color: #555; font-size: 9px; text-transform: uppercase; font-weight: bold; letter-spacing: 1px; margin-bottom: 4px; }
    .val-quant { font-family: 'JetBrains Mono', monospace; font-size: 18px; font-weight: bold; color: #00ff88; }
    .roadmap-txt { font-size: 11px; line-height: 1.2; }
    .stMetric { padding: 0 !important; }
    [data-testid="stMetricValue"] { font-size: 20px !important; }
    .news-item { font-size: 11px; border-bottom: 1px solid #111; padding: 4px 0; }
</style>
""", unsafe_allow_html=True)

def get_market_data():
    try:
        gold = yf.Ticker("GC=F").fast_info['last_price']
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        feed = feedparser.parse("https://news.google.com/rss/search?q=or+bourse+forex&hl=fr&gl=FR&ceid=FR:fr")
        news = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)[:6] # 6 news max pour le scroll
        
        # Scores dynamiques
        text_blob = " ".join([n.title.lower() for n in news])
        geo = 32.50 if any(w in text_blob for w in ['guerre', 'tension', 'iran']) else 28.0
        cb = 21.40 if any(w in text_blob for w in ['fed', 'taux', 'bce']) else 18.0
        return gold, dxy, yields, news, geo, cb
    except: return None

data = get_market_data()
if data:
    gold, dxy, yields, news, geo, cb = data
    capital = 959.56
    lot = (capital * 0.06) / 150
    dominance = min(max((geo + cb + 9.0) - ((dxy - 100) + (yields * 5)), 10), 100)
    can_trade = dominance > 58 and yields < 2.00

    # HEADER COMPACT
    cols = st.columns([2, 1, 1])
    cols[0].markdown(f"<h3 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST UNIT</h3>", unsafe_allow_html=True)
    cols[1].markdown(f"<div class='val-quant' style='text-align:center;'>{gold:,.2f} $</div>", unsafe_allow_html=True)
    cols[2].markdown(f"<div style='text-align:right; font-size:10px; color:#444;'>{datetime.now().strftime('%H:%M:%S')} | LIVE</div>", unsafe_allow_html=True)

    st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

    # GRILLE PRINCIPALE (4 COLONNES)
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1])

    with c1: # FORCES
        st.markdown("<p class='label'>● FORCES RÉELLES</p>", unsafe_allow_html=True)
        for l, v, c in [("GÉO", geo, "#00ff88"), ("BCE", cb, "#58a6ff"), ("ETF", 9.0, "#ffb000")]:
            st.markdown(f"<div style='border-left:2px solid {c}; padding-left:8px; margin-bottom:10px;'><small class='label'>{l}</small><br><span style='font-size:14px; font-weight:bold;'>+{v:.1f}</span></div>", unsafe_allow_html=True)

    with c2: # EXECUTION
        st.markdown("<p class='label'>● EXÉCUTION (6%)</p>", unsafe_allow_html=True)
        st.markdown(f"""<div class='kz-card' style='text-align:center;'>
            <b style='color:{'#00ff88' if can_trade else '#ffb000'}; font-size:14px;'>{'BUY' if can_trade else 'WAIT'}</b><br>
            <span style='font-size:32px; font-weight:900; color:#00ff88;'>{lot:.2f}</span><br>
            <small class='label'>LOT TAILLE</small>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:10px; color:#666;'>SL: {gold-15:,.1f} | TP: {gold+30:,.1f}</div>", unsafe_allow_html=True)

    with c3: # ROADMAP
        st.markdown("<p class='label'>● ROADMAP 1M</p>", unsafe_allow_html=True)
        paliers = math.log(1000000 / capital) / math.log(2)
        st.markdown(f"""<div class='kz-card'>
            <span class='roadmap-txt'>Paliers : <b>{paliers:.1f}</b></span><br>
            <div style='background:#222; height:6px; border-radius:3px; margin:5px 0;'>
                <div style='background:#ffb000; height:100%; width:15%; border-radius:3px;'></div>
            </div>
            <span class='roadmap-txt' style='color:#666;'>Prochain: 1,919 GBP</span>
        </div>""", unsafe_allow_html=True)

    with c4: # MACRO
        st.markdown("<p class='label'>● SYNCHRO</p>", unsafe_allow_html=True)
        st.metric("DXY", f"{dxy:.2f}")
        st.metric("YIELDS", f"{yields:.2f}%")

    # NEWS & DOMINANCE (PIED DE PAGE)
    st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)
    
    cb1, cb2 = st.columns([1, 2])
    with cb1:
        st.markdown(f"<p class='label'>● DOMINANCE : {dominance:.1f}%</p>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:#111; height:15px; border-radius:3px;'><div style='background:#00ff88; height:100%; width:{dominance}%; border-radius:3px;'></div></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:{'#00ff88' if can_trade else '#ffb000'}; color:black; text-align:center; font-weight:bold; font-size:12px; margin-top:10px; border-radius:2px;'>VERDICT EN DIRECT</div>", unsafe_allow_html=True)

    with cb2:
        st.markdown("<p class='label'>● NEWS FIL (DERNIÈRES 5)</p>", unsafe_allow_html=True)
        for n in news[:5]:
            st.markdown(f"<div class='news-item'>• {n.title[:75]}...</div>", unsafe_allow_html=True)

# Rafraîchissement 2s
import time
time.sleep(2)
st.rerun()
