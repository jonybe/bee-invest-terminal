import streamlit as st
import yfinance as yf
import feedparser
import math
import pandas as pd
from datetime import datetime

# 1. Config & Style
st.set_page_config(page_title="BEE-INVEST | ECHELON 1M", layout="wide")

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; font-size: 13px; }
    .block-container { padding-top: 1rem !important; }
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; padding: 15px; border-radius: 4px; margin-bottom: 10px; }
    .label { color: #555; font-size: 9px; text-transform: uppercase; font-weight: bold; letter-spacing: 1.2px; }
    .val-quant { font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: bold; color: #00ff88; }
    .roadmap-box { background: linear-gradient(90deg, #0d0d0d 0%, #1a1a1a 100%); border-left: 3px solid #ffb000; padding: 10px; border-radius: 0 4px 4px 0; }
</style>
""", unsafe_allow_html=True)

def get_market_data():
    try:
        gold = yf.Ticker("GC=F").fast_info['last_price']
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        feed = feedparser.parse("https://news.google.com/rss/search?q=or+bourse+forex&hl=fr&gl=FR&ceid=FR:fr")
        news = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)[:4]
        
        text_blob = " ".join([n.title.lower() for n in news])
        geo = 32.50 if any(w in text_blob for w in ['guerre', 'tension', 'iran']) else 28.00
        cb = 21.40 if any(w in text_blob for w in ['fed', 'inflation', 'taux']) else 18.00
        return gold, dxy, yields, news, geo, cb
    except: return None

data = get_market_data()

if data:
    gold, dxy, yields, news, geo, cb = data
    capital = 959.56
    lot_size = (capital * 0.06) / 150
    drag = (dxy - 100) + (yields * 5)
    dominance = min(max((geo + cb + 9.0) - drag, 10), 100)
    can_trade = dominance > 58 and yields < 2.00

    # --- HEADER ---
    h1, h2 = st.columns([2, 1])
    h1.markdown(f"<h3 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST : MISSION 1M</h3>", unsafe_allow_html=True)
    h2.markdown(f"<div style='text-align:right;'><span class='val-quant'>{gold:,.2f} $</span></div>", unsafe_allow_html=True)

    st.markdown("---")

    # --- VUE PRINCIPALE (EXISTANTE) ---
    col_main, col_side = st.columns([2, 1])
    with col_main:
        st.markdown("<p class='label'>● ROADMAP ACTUELLE</p>", unsafe_allow_html=True)
        paliers_restants = math.log(1000000 / capital) / math.log(2)
        prog = (math.log(capital/100) / math.log(1000000/100)) * 100
        st.markdown(f"<div class='roadmap-box'><small>Paliers restants : {paliers_restants:.1f} | Prog: {prog:.2f}%</small><div style='background:#222; height:6px; margin-top:5px;'><div style='background:#ffb000; height:100%; width:{prog}%;'></div></div></div>", unsafe_allow_html=True)

        c_ex1, c_ex2 = st.columns(2)
        with c_ex1:
            st.markdown(f"<div class='kz-card' style='text-align:center; border-left: 3px solid #00ff88;'><small class='label'>LOT 6%</small><br><span style='font-size:35px; font-weight:900; color:#00ff88;'>{lot_size:.2f}</span><br><b>{'BUY' if can_trade else 'WAIT'}</b></div>", unsafe_allow_html=True)
        with c_ex2:
            st.markdown(f"<div class='kz-card' style='font-size:12px;'><small class='label'>PALIERS PRIX</small><br>🟢 TP: {gold+20:,.1f}<br>⚪ IN: {gold:,.1f}<br>🔴 SL: {gold-15:,.1f}</div>", unsafe_allow_html=True)

    with col_side:
        st.metric("DOMINANCE", f"{dominance:.1f}%")
        st.metric("DXY", f"{dxy:.2f}")
        st.metric("YIELDS", f"{yields:.2f}%")

    st.markdown("---")

    # --- NOUVELLE SECTION : ANALYSE DES PALIERS & DIAGRAMME ---
    st.markdown("<p class='label'>● PROJECTION DES PALIERS ET PLAN DE RETRAIT</p>", unsafe_allow_html=True)
    
    # Génération des données de paliers
    paliers_data = []
    temp_cap = capital
    for i in range(1, 12):
        temp_cap *= 2
        retrait = temp_cap * 0.10 if temp_cap >= 5000 else 0 # Sortie de 10% à partir de 5k
        paliers_data.append({"Palier": f"P{i}", "Capital": round(temp_cap, 2), "Retrait": round(retrait, 2)})
    
    df_paliers = pd.DataFrame(paliers_data)

    col_chart, col_table = st.columns([2, 1])

    with col_chart:
        # Diagramme de gains (Capital vs Paliers)
        st.line_chart(df_paliers.set_index("Palier")["Capital"])
        st.caption("Diagramme de croissance composée (Doublement par palier)")

    with col_table:
        st.markdown("<p class='label'>PLAN DE SORTIE</p>", unsafe_allow_html=True)
        st.dataframe(df_paliers, height=300)
        st.markdown("""
        <div style='font-size:10px; color:#666;'>
        📌 <b>P1 à P3</b> : 0% retrait (Capitalisation brute).<br>
        📌 <b>P4 (8k+)</b> : Retrait 10% des profits pour sécurité.<br>
        📌 <b>P10 (1M)</b> : Sortie totale / Rente.
        </div>
        """, unsafe_allow_html=True)

    # News en bas
    st.markdown("<hr>", unsafe_allow_html=True)
    for n in news:
        with st.expander(f"{n.published[5:16]} | {n.title[:80]}"):
            st.write(n.summary if 'summary' in n else "Analyse...")
            st.markdown(f"[Source]({n.link})")

import time
time.sleep(2)
st.rerun()
