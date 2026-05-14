import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. Configuration Haute Performance
st.set_page_config(page_title="BEE-INVEST | LIVE", layout="wide")

# Système de rafraîchissement ultra-rapide (2 secondes pour le prix)
if "count" not in st.session_state:
    st.session_state.count = 0

def refresh():
    st.session_state.count += 1
    st.rerun()

# 2. CSS Style Professionnel "Killzone"
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    .price-box { background: #0d0d0d; border: 1px solid #1a1a1a; padding: 20px; border-radius: 4px; text-align: center; }
    .price-val { font-family: 'Courier New', monospace; font-size: 35px; font-weight: bold; color: #00ff88; }
    .news-card { border-left: 3px solid #ffb000; padding: 12px; background: #0d0d0d; margin-bottom: 8px; font-size: 14px; }
    .footer-live { background: #00ff88; color: black; text-align: center; padding: 10px; font-weight: 900; margin-top: 20px; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

# 3. Récupération des données
def get_data():
    # Prix en live
    g = yf.Ticker("GC=F").fast_info['last_price']
    b = yf.Ticker("BTC-USD").fast_info['last_price']
    d = yf.Ticker("DX-Y.NYB").fast_info['last_price']
    y = yf.Ticker("^TNX").fast_info['last_price'] / 10
    
    # News en Français (Source : Google News Finance FR)
    feed = feedparser.parse("https://news.google.com/rss/search?q=or+bourse+forex&hl=fr&gl=FR&ceid=FR:fr")
    return g, b, d, y, feed.entries[:10]

gold, btc, dxy, yields, news = get_data()

# --- AFFICHAGE ---

# HEADER
h1, h2 = st.columns([2, 1])
with h1:
    st.markdown(f"<h1 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST TERMINAL</h1>", unsafe_allow_html=True)
with h2:
    st.markdown(f"<div style='text-align:right; color:#444;'>ACTUALISATION RÉELLE : {datetime.now().strftime('%H:%M:%S')}<br><span style='color:#00ff88;'>● FLUX LIVE ACTIF</span></div>", unsafe_allow_html=True)

st.markdown("---")

# CORPS DU TERMINAL
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("<p style='color:#666; font-size:12px; font-weight:bold;'>● DERNIÈRES DÉPÊCHES (FRANCE)</p>", unsafe_allow_html=True)
    for n in news:
        st.markdown(f"""<div class="news-card">
            <small style="color:#555;">{n.published[:16]}</small><br>
            <b>{n.title}</b>
        </div>""", unsafe_allow_html=True)

with c2:
    st.markdown("<p style='color:#666; font-size:12px; font-weight:bold;'>● INDICATEURS TEMPS RÉEL</p>", unsafe_allow_html=True)
    
    # Cartes de prix
    st.markdown(f"<div class='price-box'><small>XAU/USD (OR)</small><br><div class='price-val'>{gold:,.2f} $</div></div><br>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-box'><small>DXY (DOLLAR)</small><br><div class='price-val' style='color:white;'>{dxy:.2f}</div></div><br>", unsafe_allow_html=True)
    st.markdown(f"<div class='price-box'><small>BTC/USD</small><br><div class='price-val' style='color:#58a6ff;'>{btc:,.0f} $</div></div>", unsafe_allow_html=True)

    st.markdown("<br><div style='text-align:center; border:1px solid #222; padding:15px;'>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#ffb000;'>BIAIS : NEUTRE</p><small>RENDEMENTS : {yields:.2f}%</small>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#00ff88;'>LOT 0.00</h2></div>", unsafe_allow_html=True)

# BANDEAU FINAL
st.markdown("<div class='footer-live'>Confluence Analysée - Attente Signal Technique</div>", unsafe_allow_html=True)

# Auto-refresh invisible toutes les 2 secondes
st.empty()
import time
time.sleep(2)
st.rerun()
