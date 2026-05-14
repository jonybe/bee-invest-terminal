import streamlit as st
import yfinance as yf
import feedparser
import math
from datetime import datetime

# 1. Configuration Pro & Compacte
st.set_page_config(page_title="BEE-INVEST | ELITE UNIT", layout="wide")

st.markdown("""
<style>
    /* Réduction globale de la taille de police et des marges */
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #050505; 
        color: #e0e0e0; 
        font-family: 'Inter', sans-serif; 
        font-size: 13px; 
    }
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; padding: 15px; border-radius: 4px; margin-bottom: 10px; }
    .label { color: #555; font-size: 9px; text-transform: uppercase; font-weight: bold; letter-spacing: 1.2px; }
    .val-quant { font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: bold; color: #00ff88; }
    .roadmap-box { background: linear-gradient(90deg, #0d0d0d 0%, #1a1a1a 100%); border-left: 3px solid #ffb000; padding: 10px; margin-top: 5px; border-radius: 0 4px 4px 0; }
    /* Ajustement des Expanders de news */
    .stExpander { border: none !important; background: #0d0d0d !important; margin-bottom: 2px !important; }
    .stExpander div[role="button"] p { font-size: 11px !important; }
</style>
""", unsafe_allow_html=True)

def get_market_data():
    try:
        gold = yf.Ticker("GC=F").fast_info['last_price']
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        btc = yf.Ticker("BTC-USD").fast_info['last_price']
        feed = feedparser.parse("https://news.google.com/rss/search?q=or+bourse+forex&hl=fr&gl=FR&ceid=FR:fr")
        news = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)[:8]
        
        text_blob = " ".join([n.title.lower() for n in news])
        geo = 32.50 if any(w in text_blob for w in ['guerre', 'tension', 'iran', 'russie']) else 28.00
        cb = 21.40 if any(w in text_blob for w in ['fed', 'inflation', 'taux', 'powell']) else 18.00
        etf = 11.20 if any(w in text_blob for w in ['etf', 'achat', 'physique']) else 9.00
        
        return gold, dxy, yields, btc, news, geo, cb, etf
    except: return None

data = get_market_data()

if data:
    gold, dxy, yields, btc, news, geo, cb, etf = data
    capital = 959.56
    risk_percent = 0.06 # Ton risque à 6%
    lot_size = (capital * risk_percent) / 150 # Calcul du lot dynamique
    
    # Roadmap Million
    paliers_restants = math.log(1000000 / capital) / math.log(2)
    progression = (math.log(capital/100) / math.log(1000000/100)) * 100

    # Dominance
    drag = (dxy - 100) + (yields * 5)
    dominance = min(max((geo + cb + etf) - drag, 10), 100)
    can_trade = dominance > 58 and yields < 2.00

    # Header Ultra-Compact
    h1, h2, h3 = st.columns([1.5, 1, 1])
    h1.markdown(f"<h3 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST UNIT</h3><small style='color:#444; font-size:9px;'>MISSION 1M | RISK 6%</small>", unsafe_allow_html=True)
    h2.markdown(f"<div class='val-quant' style='text-align:center;'>{gold:,.2f} $</div>", unsafe_allow_html=True)
    h3.markdown(f"<div style='text-align:right; font-size:10px; color:#444;'>{datetime.now().strftime('%H:%M:%S')} | LIVE</div>", unsafe_allow_html=True)

    st.markdown("<hr style='margin: 0.3rem 0;'>", unsafe_allow_html=True)

    col_main, col_side = st.columns([2, 1])

    with col_main:
        # ROADMAP
        st.markdown("<p class='label'>● ROADMAP VERS LE MILLION</p>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='roadmap-box'>
            <div style='display:flex; justify-content:space-between; font-size:11px;'>
                <span>Paliers restants : <b>{paliers_restants:.1f}</b></span>
                <span style='color:#ffb000;'>Progression : {progression:.2f}%</span>
            </div>
            <div style='background:#222; height:6px; border-radius:3px; margin-top:5px;'>
                <div style='background:#ffb000; height:100%; width:{progression}%; border-radius:3px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # EXÉCUTION & PALIERS
        c_ex1, c_ex2 = st.columns(2)
        with c_ex1:
            st.markdown(f"""<div class='kz-card' style='text-align:center; border-left: 3px solid #00ff88; padding: 10px;'>
                <small class='label'>LOT À EXÉCUTER</small><br>
                <span style='font-size:38px; font-weight:900; color:#00ff88;'>{lot_size:.2f}</span><br>
                <b style='font-size:12px; color:{'#00ff88' if can_trade else '#ffb000'};'>{'SIGNAL ACHAT' if can_trade else 'ATTENTE CONFLUENCE'}</b>
            </div>""", unsafe_allow_html=True)
        with c_ex2:
            st.markdown(f"""<div class='kz-card' style='padding: 10px; font-size:11px;'>
                <small class='label'>NIVEAUX ACTUELS</small><br>
                🟢 TP2 : <b>{gold+30:,.1f}</b> | 🟢 TP1 : <b>{gold+15:,.1f}</b><br>
                ⚪ ENTRY : <b>{gold:,.1f}</b> | 🔴 SL : <b>{gold-15:,.1f}</b>
            </div>""", unsafe_allow_html=True)

        # NEWS (Limitées à 5 pour gagner de la place)
        st.markdown("<p class='label'>● FLUX DÉPÊCHES ANALYSÉES</p>", unsafe_allow_html=True)
        for n in news[:5]:
            with st.expander(f"🕒 {n.published[5:16]} | {n.title[:70]}..."):
                st.write(n.summary[:200] if 'summary' in n else "Analyse en cours...")
                st.markdown(f"[Lien]({n.link})")

    with col_side:
        st.markdown("<p class='label'>● SURVEILLANCE MACRO</p>", unsafe_allow_html=True)
        st.metric("DOMINANCE OR", f"{dominance:.1f}%")
        st.metric("DXY BROAD", f"{dxy:.2f}")
        st.metric("REAL YIELDS", f"{yields:.2f}%")
        
        st.markdown("<div class='kz-card' style='margin-top:10px; padding:10px;'>", unsafe_allow_html=True)
        st.markdown(f"<p class='label'>FORCES RÉELLES</p>", unsafe_allow_html=True)
        st.markdown(f"🌍 Géo : **+{geo:.2f}**<br>🏛️ BCE : **+{cb:.2f}**<br>💰 ETF : **+{etf:.2f}**", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Footer Verdict
    st.markdown(f"<div style='background:{'#00ff88' if can_trade else '#ffb000'}; color:black; text-align:center; padding:8px; font-weight:900; font-size:14px; border-radius:4px;'>VERDICT : {'ACCORD EXÉCUTION' if can_trade else 'PATIENCE EXIGÉE'}</div>", unsafe_allow_html=True)

# Auto-refresh 2s
import time
time.sleep(2)
st.rerun()
