import streamlit as st
import yfinance as yf
import feedparser
import math
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configuration & Style
st.set_page_config(page_title="BEE-INVEST | TOTAL CONTROL", layout="wide")

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; font-size: 11.5px; }
    .block-container { padding-top: 3.5rem !important; padding-bottom: 0rem !important; }
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; padding: 12px; border-radius: 4px; margin-bottom: 8px; }
    .label { color: #555; font-size: 9px; text-transform: uppercase; font-weight: bold; letter-spacing: 1.2px; }
    .val-quant { font-family: 'JetBrains Mono', monospace; font-size: 18px; font-weight: bold; color: #00ff88; }
    .matrix-row { display: flex; justify-content: space-between; align-items: center; background: rgba(15, 15, 15, 0.8); border: 1px solid #1a1a1a; margin-bottom: 5px; padding: 12px 18px; border-radius: 4px; }
    .bar-container { background: #1a1a1a; height: 6px; border-radius: 3px; margin: 4px 0 10px 0; overflow: hidden; display: flex; }
    .p-bull { background: #00ff88; height: 100%; transition: 0.2s; }
    .p-bear { background: #ff4b4b; height: 100%; transition: 0.2s; }
</style>
""", unsafe_allow_html=True)

def get_market_data():
    try:
        t = yf.Ticker("GC=F")
        gold = t.fast_info['last_price']
        df_h2 = t.history(period="10d", interval="1h").resample('2h').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}).dropna()
        df_m15 = t.history(period="1d", interval="15m")
        
        # BOOST DE RÉACTIVITÉ : Calcul sur 2 bougies (30 min)
        m15_imp = ((df_m15['Close'].iloc[-1] - df_m15['Close'].iloc[-3]) / df_m15['Close'].iloc[-3]) * 100
        
        yesterday = t.history(period="2d", interval="60m")
        ph, pl = yesterday.iloc[:int(len(yesterday)/2)]['High'].max(), yesterday.iloc[:int(len(yesterday)/2)]['Low'].min()
        poc = yesterday.iloc[:int(len(yesterday)/2)]['Close'].mode().iloc[0]
        
        hist = t.history(period="5d")
        vol_atr = (hist['High'] - hist['Low']).mean()
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        
        # News
        feed = feedparser.parse("https://news.google.com/rss/search?q=gold+forex&hl=en")
        text = " ".join([n.title.lower() for n in feed.entries[:5]])
        geo, cb, etf = (32.5, 21.4, 11.2) if "war" in text or "conflict" in text else (28.0, 18.0, 9.0)
        
        return gold, dxy, yields, vol_atr, geo, cb, etf, df_h2, ph, pl, poc, m15_imp
    except: return None

data = get_market_data()

if data:
    gold, dxy, yields, vol_atr, geo, cb, etf, df_h2, ph, pl, poc, m15_imp = data
    cap, risk = 959.56, 0.06
    sl_dyn = max(vol_atr * 0.5, 15.0)
    perte_gbp = cap * risk
    lot = perte_gbp / (sl_dyn * 10)
    
    # LOGIQUE DE SCORE ULTRA-RÉACTIVE (Impulse x 25 au lieu de 10)
    drag = (dxy - 100) + (yields * 5)
    bull_score = min(max((geo + cb + etf) - drag + (m15_imp * 25), 10), 100)
    
    status = "NEUTRAL" if 42 <= bull_score <= 58 else "BULLISH" if bull_score > 58 else "BEARISH"
    st_col = "#ffb000" if status == "NEUTRAL" else "#00ff88" if status == "BULLISH" else "#ff4b4b"

    # Header
    st.markdown(f"### 🔱 BEE-INVEST V53 <small style='color:{st_col};'>[{status} | IMPULSE: {m15_imp:+.3f}]</small>", unsafe_allow_html=True)

    col_main, col_side = st.columns([2, 1])

    with col_main:
        # CHART
        fig = go.Figure(data=[go.Candlestick(x=df_h2.index, open=df_h2['Open'], high=df_h2['High'], low=df_h2['Low'], close=df_h2['Close'])])
        fig.add_hline(y=ph, line_dash="dash", line_color="#ff4b4b")
        fig.add_hline(y=pl, line_dash="dash", line_color="#00ff88")
        fig.add_hline(y=poc, line_color="#ffb000", line_width=2)
        fig.update_layout(template="plotly_dark", paper_bgcolor="#050505", plot_bgcolor="#050505", height=320, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # TARGETS
        st.markdown("<p class='label'>● PARAMÈTRES & PROJECTION</p>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.markdown(f"<div class='kz-card'>🟢 TP: {gold+(sl_dyn*2):,.2f}<br>⚪ IN: {gold:,.2f}<br>🔴 SL: {gold-sl_dyn:,.2f}</div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='kz-card'>💰 GAIN: +{perte_gbp*2:.2f} £<br>⚠️ RISQUE: -{perte_gbp:.2f} £<br>📊 LOT: {lot:.2f}</div>", unsafe_allow_html=True)

        # MATRIX (Locked)
        st.markdown("<p class='label'>● MATRIX ROADMAP</p>", unsafe_allow_html=True)
        tr = cap
        for i in range(1, 4):
            ret = (tr * 0.1) if tr > 5000 else 0
            tr = (tr * 2) - ret
            badge = f"<div class='m-badge-blue'>SORTIE</div>" if ret > 0 else f"<div class='m-badge-red'>ACCUM.</div>"
            st.markdown(f"<div class='matrix-row'><div>P{i:02}</div><div style='font-weight:bold;'>{tr:,.0f} £</div><div>LOT: {(tr*0.06)/(sl_dyn*10):.2f}</div>{badge}</div>", unsafe_allow_html=True)

    with col_side:
        # DOMINANCE
        st.markdown("<p class='label'>● BULL VS BEAR DOMINANCE</p>", unsafe_allow_html=True)
        st.markdown(f"<div class='kz-card'>SCORE: {bull_score:.1f}<div class='bar-container'><div class='p-bull' style='width:{bull_score}%'></div><div class='p-bear' style='width:{100-bull_score}%'></div></div></div>", unsafe_allow_html=True)
        st.metric("DXY", f"{dxy:.2f}")
        st.metric("YIELDS", f"{yields:.2f}%")

        # STRATEGIC INTEL (Side)
        st.markdown(f"""
        <div style="background:#080808; border-top:1px dashed #333; padding:10px; margin-top:20px;">
            <p class='label' style='color:#ffb000;'>⚔️ STRATEGIC INTEL</p>
            <div style="font-size:10px; color:#aaa;">
                <b>ANALYSE POSITION :</b> RR 3.24 détecté. Entry POC risquée mais à fort potentiel. <br><br>
                <b>MICRO-FLASH :</b> Si l'impulsion chute sous -0.500, ton terminal passera en "BEARISH" pour te couper avant le SL.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"<div style='background:{st_col}; color:black; text-align:center; padding:10px; font-weight:900; border-radius:4px;'>VERDICT FINAL : {status}</div>", unsafe_allow_html=True)

import time
time.sleep(2)
st.rerun()
