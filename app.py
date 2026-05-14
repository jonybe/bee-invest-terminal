import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. Configuration Haute Fréquence
st.set_page_config(page_title="BEE-INVEST | RISK 6%", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; padding: 20px; border-radius: 4px; margin-bottom: 15px; }
    .label { color: #555; font-size: 10px; text-transform: uppercase; font-weight: bold; letter-spacing: 1.5px; margin-bottom: 10px; }
    .val-quant { font-family: 'JetBrains Mono', monospace; font-size: 22px; font-weight: bold; }
    .bar-bg { background: #1a1a1a; height: 8px; border-radius: 4px; margin: 8px 0; overflow: hidden; }
    .bar-bull { background: #00ff88; height: 100%; transition: width 1s; }
</style>
""", unsafe_allow_html=True)

def get_market_data():
    try:
        gold = yf.Ticker("GC=F").fast_info['last_price']
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        btc = yf.Ticker("BTC-USD").fast_info['last_price']
        feed = feedparser.parse("https://news.google.com/rss/search?q=or+bourse+forex&hl=fr&gl=FR&ceid=FR:fr")
        news = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)[:10]
        
        # Analyse de Sentiment Réelle
        text_blob = " ".join([n.title.lower() for n in news])
        geo = 32.50 if any(w in text_blob for w in ['guerre', 'tension', 'conflit', 'iran', 'russie']) else 28.00
        cb = 21.40 if any(w in text_blob for w in ['fed', 'inflation', 'taux', 'bce', 'powell']) else 18.00
        etf = 11.20 if any(w in text_blob for w in ['etf', 'achat', 'physique', 'demande']) else 9.00
        
        return gold, dxy, yields, btc, news, geo, cb, etf
    except: return None

data = get_market_data()

if data:
    gold, dxy, yields, btc, news, geo, cb, etf = data
    
    # --- LOGIQUE DE RISQUE 6% ---
    capital = 959.56
    risk_percent = 0.06 # Passé à 6%
    risk_amount = capital * risk_percent
    stop_loss_distance = 15.0 # $15 de SL sur l'Or
    lot_size = risk_amount / (stop_loss_distance * 10) # Formule Gold
    
    # Calcul Dominance
    drag = (dxy - 100) + (yields * 5)
    dominance = min(max((geo + cb + etf) - drag, 10), 100)
    can_trade = dominance > 58 and yields < 2.00

    # Header
    st.markdown(f"<div style='display:flex; justify-content:space-between; align-items:center;'><div><h2 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST QUANT UNIT</h2><small style='color:#444;'>RISK PROFILE : 6% AGGRESSIVE</small></div><div style='font-family:JetBrains Mono; color:#00ff88; font-size:22px; font-weight:bold;'>XAU: {gold:,.2f} $</div></div>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns([1.2, 1.5, 0.8])

    with col1:
        st.markdown("<p class='label'>● ANALYSE DES FORCES (RÉEL)</p>", unsafe_allow_html=True)
        for label, val, color in [("GÉOPOLITIQUE", geo, "#00ff88"), ("BANQUES CENTRALES", cb, "#58a6ff"), ("FLUX ETF / INST.", etf, "#ffb000")]:
            st.markdown(f"""<div style="border-left:2px solid {color}; padding-left:15px; margin-bottom:20px;">
                <small class="label" style="color:{color};">{label}</small><br>
                <span class="val-quant">+{val:.2f}</span>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("<p class='label'>● EXÉCUTION & PALIERS</p>", unsafe_allow_html=True)
        st.markdown(f"<small style='color:#00ff88;'>BULL DOMINANCE : {dominance:.1f}%</small><div class='bar-bg'><div class='bar-bull' style='width:{dominance}%'></div></div>", unsafe_allow_html=True)
        
        st.markdown(f"""<div class='kz-card' style='border-top: 3px solid #ffb000; text-align:center;'>
            <small class="label">SIGNAL D'ENTRÉE</small><br>
            <b style="font-size:24px; color:{'#00ff88' if can_trade else '#ffb000'};">{'ACHAT (BUY)' if can_trade else 'ATTENTE CONFLUENCE'}</b>
            <hr style='border-color:#222;'>
            <small class="label">TAILLE DE LOT (RISQUE 6%)</small><br>
            <span style="font-size:50px; font-weight:900; color:#00ff88;">{lot_size:.2f}</span>
            <div style="margin-top:10px; color:#666; font-size:11px;">Risque par trade : {risk_amount:.2f} GBP</div>
        </div>""", unsafe_allow_html=True)
        
        # TABLEAU DES PALIERS
        st.markdown("<p class='label'>● PALIERS DE POSITION ACTUELS</p>", unsafe_allow_html=True)
        st.table({
            "Niveaux": ["STOP LOSS", "ENTRÉE LIVE", "TAKE PROFIT (R1)", "TAKE PROFIT (R2)"],
            "Prix ($)": [f"{gold-15:,.2f}", f"{gold:,.2f}", f"{gold+15:,.2f}", f"{gold+30:,.2f}"]
        })

    with col3:
        st.markdown("<p class='label'>● SYNCHRO MACRO</p>", unsafe_allow_html=True)
        st.metric("DXY BROAD", f"{dxy:.2f}")
        st.metric("REAL YIELDS", f"{yields:.2f}%")
        st.metric("BTC / USD", f"{btc:,.0f}")
        
        st.markdown("<br><p class='label'>● ÉTAT DU CAPITAL</p>", unsafe_allow_html=True)
        st.markdown(f"<div class='kz-card' style='text-align:center;'><small class='label'>SOLDE</small><br><b style='font-size:20px;'>{capital} GBP</b></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p class='label'>● NEWS ANALYSÉES EN TEMPS RÉEL</p>", unsafe_allow_html=True)
    for n in news[:5]:
        with st.expander(f"🕒 {n.published[5:16]} | {n.title}"):
            st.write(n.summary if 'summary' in n else "Analyse du contenu en cours...")
            st.markdown(f"[Source Article]({n.link})")

# Auto-refresh 2s pour le prix / 60s pour les news
import time
time.sleep(2)
st.rerun()
