import streamlit as st
import yfinance as yf
import feedparser
import math
from datetime import datetime

st.set_page_config(page_title="BEE-INVEST | ROAD TO 1M", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; padding: 20px; border-radius: 4px; margin-bottom: 15px; }
    .label { color: #555; font-size: 10px; text-transform: uppercase; font-weight: bold; letter-spacing: 1.5px; }
    .val-quant { font-family: 'JetBrains Mono', monospace; font-size: 22px; font-weight: bold; color: #00ff88; }
    .roadmap-box { background: linear-gradient(90deg, #0d0d0d 0%, #1a1a1a 100%); border-left: 4px solid #ffb000; padding: 15px; margin-top: 10px; border-radius: 0 4px 4px 0; }
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
        
        text_blob = " ".join([n.title.lower() for n in news])
        geo = 32.50 if any(w in text_blob for w in ['guerre', 'tension', 'iran', 'russie']) else 28.00
        cb = 21.40 if any(w in text_blob for w in ['fed', 'inflation', 'taux', 'powell']) else 18.00
        etf = 11.20 if any(w in text_blob for w in ['etf', 'achat', 'physique']) else 9.00
        
        return gold, dxy, yields, btc, news, geo, cb, etf
    except: return None

data = get_market_data()

if data:
    gold, dxy, yields, btc, news, geo, cb, etf = data
    
    # --- LOGIQUE FINANCIÈRE ---
    capital_actuel = 959.56
    objectif = 1000000.00
    risk_percent = 0.06
    
    # Calcul des paliers pour le million (Doublement du capital)
    paliers_restants = math.log(objectif / capital_actuel) / math.log(2)
    
    # Calcul du lot dynamique (Risque 6% sur 150 pips)
    lot_size = (capital_actuel * risk_percent) / 150
    
    # Dominance
    drag = (dxy - 100) + (yields * 5)
    dominance = min(max((geo + cb + etf) - drag, 10), 100)
    can_trade = dominance > 58 and yields < 2.00

    # Header
    st.markdown(f"<div style='display:flex; justify-content:space-between; align-items:center;'><div><h2 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST : MISSION 1M</h2><small style='color:#444;'>SYSTÈME DE CROISSANCE COMPOSÉE EXTRÊME</small></div><div class='val-quant'>{gold:,.2f} $</div></div>", unsafe_allow_html=True)
    st.markdown("---")

    col_main, col_side = st.columns([2, 1])

    with col_main:
        # ROADMAP DU MILLION
        st.markdown("<p class='label'>● ROADMAP VERS LE MILLION</p>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='roadmap-box'>
            <div style='display:flex; justify-content:space-between;'>
                <span>Paliers de doublement nécessaires : <b>{paliers_restants:.1f}</b></span>
                <span style='color:#ffb000;'>Progression : {( (math.log(capital_actuel/100) / math.log(objectif/100)) * 100 ):.2f}%</span>
            </div>
            <div style='background:#222; height:10px; border-radius:5px; margin-top:10px;'>
                <div style='background:#ffb000; height:100%; width:{ (math.log(capital_actuel/100) / math.log(objectif/100)) * 100 }%; border-radius:5px;'></div>
            </div>
            <p style='font-size:12px; color:#666; margin-top:10px;'>
                Prochain palier majeur : <b>1,919.12 GBP</b>. Maintenir un risque de 6% par setup validé. 
                Ne jamais overtrade si la dominance est < 58%.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # EXÉCUTION
        c_exec1, c_exec2 = st.columns(2)
        with c_exec1:
            st.markdown(f"""<div class='kz-card' style='text-align:center; border-left: 4px solid #00ff88;'>
                <small class='label'>SIGNAL ACTUEL</small><br>
                <b style='font-size:20px; color:{'#00ff88' if can_trade else '#ffb000'};'>{'ACHAT VALIDÉ' if can_trade else 'PATIENCE (WAIT)'}</b><br><br>
                <small class='label'>LOT À EXÉCUTER (6%)</small><br>
                <span style='font-size:45px; font-weight:900; color:#00ff88;'>{lot_size:.2f}</span>
            </div>""", unsafe_allow_html=True)
        with c_exec2:
            st.markdown(f"""<div class='kz-card' style='text-align:center; border-left: 4px solid #ff4b4b;'>
                <small class='label'>PALIERS DE PRIX</small><br>
                <div style='text-align:left; font-size:13px; margin-top:10px;'>
                    🟢 TP2 : <b>{gold+30:,.2f}</b><br>
                    🟢 TP1 : <b>{gold+15:,.2f}</b><br>
                    ⚪ ENTRÉE : <b>{gold:,.2f}</b><br>
                    🔴 SL : <b>{gold-15:,.2f}</b>
                </div>
            </div>""", unsafe_allow_html=True)

    with col_side:
        st.markdown("<p class='label'>● MÉTRIQUES DE SURVEILLANCE</p>", unsafe_allow_html=True)
        st.metric("DOMINANCE OR", f"{dominance:.1f}%")
        st.metric("DXY BROAD", f"{dxy:.2f}")
        st.metric("REAL YIELDS", f"{yields:.2f}%")
        
        st.markdown("<br><p class='label'>● FORCES DE SOUTIEN RÉELLES</p>", unsafe_allow_html=True)
        st.markdown(f"🌍 Géo : **+{geo:.2f}**")
        st.markdown(f"🏛️ BCE : **+{cb:.2f}**")
        st.markdown(f"💰 ETF : **+{etf:.2f}**")

    st.markdown("---")
    st.markdown("<p class='label'>● DERNIÈRES DÉPÊCHES ANALYSÉES</p>", unsafe_allow_html=True)
    for n in news[:4]:
        with st.expander(f"🕒 {n.published[5:16]} | {n.title}"):
            st.write(n.summary if 'summary' in n else "Analyse en cours...")
            st.markdown(f"[Lien Source]({n.link})")

import time
time.sleep(2)
st.rerun()
