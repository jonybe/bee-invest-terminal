import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# 1. Config & Auto-refresh
st.set_page_config(page_title="BEE-INVEST | TERMINAL", layout="wide")
st_autorefresh(interval=30000, key="datarefresh")

# --- CSS PRO DARK ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    [data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; color: #00ff88 !important; font-size: 32px !important; }
    [data-testid="stMetricLabel"] { color: #555 !important; text-transform: uppercase; font-size: 10px !important; letter-spacing: 1px; }
    .news-card { border-left: 2px solid #ffb000; padding: 10px 15px; background: #0d0d0d; margin-bottom: 10px; border-radius: 0 4px 4px 0; }
    .footer-band { background: #00ff88; color: #000; text-align: center; padding: 15px; font-weight: 900; font-size: 20px; border-radius: 4px; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

# 2. Données
try:
    # Prix
    gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
    btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
    dxy = yf.Ticker("DX-Y.NYB").history(period="1d")['Close'].iloc[-1]
    yields = yf.Ticker("^TNX").history(period="1d")['Close'].iloc[-1] / 10
    
    # News RSS (Source alternative direct)
    feed = feedparser.parse("https://news.google.com/rss/search?q=gold+market+forex&hl=en-US&gl=US&ceid=US:en")
    entries = feed.entries[:8]
except:
    st.error("Connexion aux flux financiers interrompue...")
    st.stop()

# --- INTERFACE ---
# HEADER
col_h1, col_h2, col_h3 = st.columns([1.5, 1, 1])
with col_h1:
    st.markdown(f"<h2 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST</h2><small style='color:#333;'>GOLD INTELLIGENCE UNIT</small>", unsafe_allow_html=True)
with col_h2:
    st.metric(label="XAU / USD (LIVE)", value=f"{gold:,.2f} $")
with col_h3:
    st.markdown(f"<div style='text-align:right; color:#444; font-size:12px;'>MAJ: {datetime.now().strftime('%H:%M:%S')}<br>● CONNECTED</div>", unsafe_allow_html=True)

st.markdown("---")

# CORPS DU TERMINAL
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("<p style='color:#555; font-size:10px; font-weight:bold; letter-spacing:2px;'>● LIVE MARKET NARRATIVE</p>", unsafe_allow_html=True)
    if entries:
        for n in entries:
            st.markdown(f"""<div class="news-card">
                <small style="color:#444;">{n.published[:16]}</small><br>
                <b style="color:#ccc; font-size:14px;">{n.title}</b>
            </div>""", unsafe_allow_html=True)
    else:
        st.warning("Recherche de nouvelles dépêches en cours...")

with c2:
    st.markdown("<p style='color:#555; font-size:10px; font-weight:bold; letter-spacing:2px;'>● SYNCHRONISATION ZONE</p>", unsafe_allow_html=True)
    st.metric("INDICE DOLLAR (DXY)", f"{dxy:.2f}")
    st.metric("TAUX US 10Y", f"{yields:.2f} %")
    st.metric("BITCOIN (BTC)", f"{btc:,.0f} $")
    
    st.markdown("<br><hr style='border-color:#222;'>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    st.markdown("<p style='color:#ffb000; font-weight:bold;'>BIAIS : NEUTRE</p>", unsafe_allow_html=True)
    st.info("LOT CONSEILLÉ : 0.00 (WAIT)")
    st.markdown("</div>", unsafe_allow_html=True)

# FOOTER
st.markdown("<div class='footer-band'>CONFLUENCE ANALYSÉE - ATTENTE SIGNAL TECHNIQUE</div>", unsafe_allow_html=True)
