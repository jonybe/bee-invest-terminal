import streamlit as st
import yfinance as yf
import feedparser
import math
import pandas as pd
from datetime import datetime, timedelta

# 1. Configuration & Design System (V23/V26/V28)
st.set_page_config(page_title="BEE-INVEST | MASTER ROADMAP", layout="wide")

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #050505; 
        color: #e0e0e0; 
        font-family: 'Inter', sans-serif; 
        font-size: 12px; 
    }
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; padding: 12px; border-radius: 4px; margin-bottom: 8px; }
    .label { color: #555; font-size: 9px; text-transform: uppercase; font-weight: bold; letter-spacing: 1.2px; }
    .val-quant { font-family: 'JetBrains Mono', monospace; font-size: 18px; font-weight: bold; color: #00ff88; }
    .roadmap-box { background: linear-gradient(90deg, #0d0d0d 0%, #1a1a1a 100%); border-left: 3px solid #ffb000; padding: 8px; margin-top: 5px; border-radius: 0 4px 4px 0; }
    .stExpander { border: none !important; background: #0d0d0d !important; margin-bottom: 2px !important; }
    [data-testid="stMetricValue"] { font-size: 18px !important; color: #00ff88 !important; }
</style>
""", unsafe_allow_html=True)

def get_market_data():
    try:
        gold = yf.Ticker("GC=F").fast_info['last_price']
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        btc = yf.Ticker("BTC-USD").fast_info['last_price']
        feed = feedparser.parse("https://news.google.com/rss/search?q=or+bourse+forex&hl=fr&gl=FR&ceid=FR:fr")
        news = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)[:4]
        
        text_blob = " ".join([n.title.lower() for n in news])
        geo = 32.50 if any(w in text_blob for w in ['guerre', 'tension', 'iran', 'russie']) else 28.00
        cb = 21.40 if any(w in text_blob for w in ['fed', 'inflation', 'taux', 'powell']) else 18.00
        etf = 11.20 if any(w in text_blob for w in ['etf', 'achat', 'physique']) else 9.00
        
        return gold, dxy, yields, btc, news, geo, cb, etf
    except: return None

data = get_market_data()

if data:
    gold, dxy, yields, btc, news, geo, cb, etf = data
    cap = 959.56
    risk = 0.06
    
    # --- CALCULS AVANCÉS ROADMAP ---
    p_restants = math.log(1000000 / cap) / math.log(2)
    prog = (math.log(cap/100) / math.log(1000000/100)) * 100
    lot = (cap * risk) / 150
    drawdown_max = cap * 0.20 # Sécurité : Arrêt si -20% sur un palier
    
    drag = (dxy - 100) + (yields * 5)
    dominance = min(max((geo + cb + etf) - drag, 10), 100)
    can_trade = dominance > 58 and yields < 2.00

    # Header
    h1, h2 = st.columns([2, 1])
    h1.markdown(f"<h3 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST UNIT</h3><small style='color:#444; font-size:8px;'>STRATEGIC MASTER ROADMAP | RISK 6%</small>", unsafe_allow_html=True)
    h2.markdown(f"<div style='text-align:right;'><span class='val-quant'>{gold:,.2f} $</span><br><small style='color:#444; font-size:9px;'>{datetime.now().strftime('%H:%M:%S')}</small></div>", unsafe_allow_html=True)

    st.markdown("<hr style='margin: 0.2rem 0;'>", unsafe_allow_html=True)

    col_main, col_side = st.columns([2, 1])

    with col_main:
        # 1. ROADMAP & PSYCHOLOGIE (ENRICHI)
        st.markdown("<p class='label'>● ROADMAP STRATÉGIQUE VERS LE MILLION</p>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='roadmap-box'>
            <div style='display:flex; justify-content:space-between; font-size:10px;'>
                <span>Paliers de doublement : <b>{p_restants:.1f}</b></span>
                <span style='color:#ffb000;'>Progression Réelle : {prog:.2f}%</span>
            </div>
            <div style='background:#222; height:6px; margin:5px 0;'><div style='background:#ffb000; height:100%; width:{prog}%;'></div></div>
            <div style='display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px; font-size:10px; color:#888; margin-top:5px;'>
                <div>🎯 PROCHAIN : <b>{(cap*2):,.0f} £</b></div>
                <div>🛡️ DD MAX ADMIS : <b style='color:#ff4b4b;'>{cap-drawdown_max:,.0f} £</b></div>
                <div>⏱️ EST. TEMPS : <b>~12 mois</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        
        # 2. EXÉCUTION
        c_ex1, c_ex2 = st.columns(2)
        with c_ex1:
            st.markdown(f"""<div class='kz-card' style='text-align:center; border-left: 3px solid #00ff88;'><small class='label'>LOT ACTUEL (6%)</small><br><span style='font-size:36px; font-weight:900; color:#00ff88;'>{lot:.2f}</span><br><b style='font-size:11px; color:{'#00ff88' if can_trade else '#ffb000'};'>{'SIGNAL ACHAT VALIDÉ' if can_trade else 'WAITING FOR CONFLUENCE'}</b></div>""", unsafe_allow_html=True)
        with c_ex2:
            st.markdown(f"""<div class='kz-card' style='font-size:11px;'><small class='label'>OBJECTIFS DE PRIX</small><br>🟢 TP FINAL : <b>{gold+30:,.1f}</b><br>🟢 TP PARTIEL : <b>{gold+15:,.1f}</b><br>⚪ ENTRY : <b>{gold:,.1f}</b><br>🔴 SL : <b>{gold-15:,.1f}</b></div>""", unsafe_allow_html=True)

        # 3. DIAGRAMME DE CROISSANCE (FIXÉ)
        st.markdown("<p class='label'>● COURBE DE CROISSANCE COMPOSÉE</p>", unsafe_allow_html=True)
        p_list = []
        temp_cap = cap
        now = datetime.now()
        for i in range(1, 12):
            temp_cap *= 2
            date_p = now + timedelta(days=i*1.2*30)
            p_list.append({
                "ID": f"P{i:02}", 
                "Capital": temp_cap,
                "Echéance": date_p.strftime('%m/%Y'),
                "Retrait": temp_cap * 0.1 if temp_cap > 5000 else 0,
                "Lot": (temp_cap * 0.06) / 150,
                "Phase": "ACCUMULATION" if temp_cap < 50000 else "SÉCURITÉ" if temp_cap < 500000 else "LIBERTÉ"
            })
        df_p = pd.DataFrame(p_list)
        st.line_chart(df_p.set_index("ID")["Capital"])

        # 4. TABLEAU DÉTAILLÉ (ENRICHI)
        st.markdown("<p class='label'>● PLAN DE GUERRE : PALIERS & GESTION DE LOTS</p>", unsafe_allow_html=True)
        st.table(df_p[["ID", "Capital", "Lot", "Echéance", "Phase", "Retrait"]].head(10))

        # 5. NEWS
        st.markdown("<p class='label'>● DERNIÈRES DÉPÊCHES ANALYSÉES</p>", unsafe_allow_html=True)
        for n in news:
            with st.expander(f"🕒 {n.published[5:16]} | {n.title[:65]}..."):
                st.markdown(f"<small style='color:#aaa;'>{n.title}</small><br>[Lire]({n.link})", unsafe_allow_html=True)

    with col_side:
        # SURVEILLANCE
        st.markdown("<p class='label'>● SURVEILLANCE MARCHÉ</p>", unsafe_allow_html=True)
        st.metric("DOMINANCE", f"{dominance:.1f}%")
        st.metric("DXY BROAD", f"{dxy:.2f}")
        st.metric("REAL YIELDS", f"{yields:.2f}%")
        
        st.markdown(f"""<div class='kz-card' style='font-size:10px; padding:8px;'><p class='label'>FORCES RÉELLES</p>🌍 Géo : <b>+{geo:.1f}</b><br>🏛️ BCE : <b>+{cb:.1f}</b><br>💰 ETF : <b>+{etf:.1f}</b></div>""", unsafe_allow_html=True)
        
        st.markdown("<p class='label'>● DISCIPLINE DE TRADING</p>", unsafe_allow_html=True)
        st.warning("1. Ne pas déplacer le SL\n2. Sortir 50% au TP1\n3. Break-even après TP1")

    # Footer Verdict
    st.markdown(f"<div style='background:{'#00ff88' if can_trade else '#ffb000'}; color:black; text-align:center; padding:6px; font-weight:900; font-size:12px; border-radius:4px; margin-top:5px;'>VERDICT : {'ACCORD EXÉCUTION' if can_trade else 'ATTENTE CONFLUENCE'}</div>", unsafe_allow_html=True)

import time
time.sleep(2)
st.rerun()
