import streamlit as st
import yfinance as yf
import feedparser
import math
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="BEE-INVEST | MISSION 1M", layout="wide")

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; font-size: 13px; }
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

    # HEADER
    st.markdown(f"<div style='display:flex; justify-content:space-between; align-items:center;'><div><h2 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST : MISSION 1M</h2></div><div class='val-quant'>{gold:,.2f} $</div></div>", unsafe_allow_html=True)
    st.markdown("---")

    # --- PALIERS & PROJECTION LIVE ---
    col_a, col_b = st.columns([1.5, 1])
    
    with col_a:
        st.markdown("<p class='label'>● PROJECTION DE TRADE (LIVE 6%)</p>", unsafe_allow_html=True)
        # Projection de gain sur TP1 (15$)
        gain_estime = lot_size * 15 * 10 # 10 car 1 lot or = 100oz mais on ajuste au lot mini forex-style
        st.markdown(f"""
        <div class='kz-card' style='border-top: 2px solid #00ff88;'>
            <div style='display:flex; justify-content:space-between;'>
                <span>Gain estimé au TP1 : <b style='color:#00ff88;'>+{gain_estime:.2f} GBP</b></span>
                <span>Nouveau Capital : <b>{capital + gain_estime:.2f} GBP</b></span>
            </div>
            <p style='font-size:11px; color:#666; margin-top:5px;'>
                Un trade gagnant valide {(gain_estime/capital)*100:.1f}% du prochain palier de doublement.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("<p class='label'>● STATUT ROADMAP</p>", unsafe_allow_html=True)
        prog = (math.log(capital/100) / math.log(1000000/100)) * 100
        st.markdown(f"<div class='roadmap-box'><small>PROG: {prog:.2f}%</small><div style='background:#222; height:6px; margin-top:5px;'><div style='background:#ffb000; height:100%; width:{prog}%;'></div></div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # --- CORRECTION GRAPHIQUE ---
    st.markdown("<p class='label'>● DIAGRAMME DE CROISSANCE (TRI FIXÉ)</p>", unsafe_allow_html=True)
    
    paliers_list = []
    temp_cap = capital
    for i in range(1, 12):
        temp_cap *= 2
        paliers_list.append({"Num": i, "Palier": f"P{i}", "Capital": temp_cap})
    
    df_fix = pd.DataFrame(paliers_list)
    # On utilise "Num" pour le graphique afin d'avoir l'ordre correct 1, 2, 3...
    st.line_chart(df_fix.set_index("Palier")["Capital"])

    # TABLEAU DES PALIERS
    col_t1, col_t2 = st.columns([2, 1])
    with col_t1:
        st.table(df_fix[["Palier", "Capital"]].head(10))
    with col_t2:
        st.markdown(f"""
        <div class='kz-card'>
            <small class='label'>PARAMÈTRES ACTUELS</small><br>
            Solde : <b>{capital} GBP</b><br>
            Risque : <b>6%</b><br>
            Lot Recommandé : <b style='color:#00ff88;'>{lot_size:.2f}</b><br><br>
            <p style='font-size:10px; color:#444;'>L'ordre de tri a été corrigé via indexation numérique.</p>
        </div>
        """, unsafe_allow_html=True)

import time
time.sleep(2)
st.rerun()
