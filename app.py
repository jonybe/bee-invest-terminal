import streamlit as st
import yfinance as yf
import feedparser
import math
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. Configuration & Design System
st.set_page_config(page_title="BEE-INVEST | TOTAL CONTROL", layout="wide")

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; font-size: 11.5px; }
    .block-container { padding-top: 3.5rem !important; padding-bottom: 0rem !important; }
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; padding: 12px; border-radius: 4px; margin-bottom: 8px; }
    .label { color: #555; font-size: 9px; text-transform: uppercase; font-weight: bold; letter-spacing: 1.2px; }
    .val-quant { font-family: 'JetBrains Mono', monospace; font-size: 18px; font-weight: bold; color: #00ff88; }
    .matrix-row { display: flex; justify-content: space-between; align-items: center; background: rgba(15, 15, 15, 0.8); border: 1px solid #1a1a1a; margin-bottom: 5px; padding: 12px 18px; border-radius: 4px; }
    .m-id { color: #ffb000; font-family: 'JetBrains Mono'; font-weight: 900; width: 45px; font-size: 14px; }
    .bar-container { background: #1a1a1a; height: 6px; border-radius: 3px; margin: 4px 0 10px 0; overflow: hidden; display: flex; }
    .p-bull { background: #00ff88; height: 100%; transition: 0.5s; }
    .p-bear { background: #ff4b4b; height: 100%; transition: 0.5s; }
    .legende-centrale { font-size: 11px; color: #888; line-height: 1.6; padding: 15px; background: #0a0a0a; border-radius: 4px; border: 1px solid #1a1a1a; border-left: 4px solid #ffb000; margin: 15px 0; }
    .status-tag { padding: 2px 6px; border-radius: 3px; font-size: 9px; font-weight: bold; margin-left: 10px; }
</style>
""", unsafe_allow_html=True)

def get_market_data():
    try:
        t = yf.Ticker("GC=F")
        gold = t.fast_info['last_price']
        df_h2 = t.history(period="10d", interval="1h").resample('2h').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}).dropna()
        yesterday = t.history(period="2d", interval="15m")
        prev_day = yesterday.iloc[:int(len(yesterday)/2)]
        p_high, p_low = prev_day['High'].max(), prev_day['Low'].min()
        poc = prev_day['Close'].mode().iloc[0]
        
        # Calcul de l'impulsion (Comme sur Killzone)
        m15_impulse = ((yesterday['Close'].iloc[-1] - yesterday['Close'].iloc[-2]) / yesterday['Close'].iloc[-2]) * 100
        
        hist = t.history(period="5d")
        vol_atr = (hist['High'] - hist['Low']).mean()
        change = ((gold - hist['Close'].iloc[-1]) / hist['Close'].iloc[-1]) * 100
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        
        feed = feedparser.parse("https://news.google.com/rss/search?q=gold+forex&hl=en")
        news = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)[:4]
        text = " ".join([n.title.lower() for n in news])
        geo, cb, etf = (32.5, 21.4, 11.2) if "war" in text else (28.0, 18.0, 9.0)
        
        h4_p = min(max(50 + ((df_h2['Close'].iloc[-1] - df_h2['Close'].mean())/2), 10), 90)
        return gold, dxy, yields, news, vol_atr, h4_p, geo, cb, etf, df_h2, p_high, p_low, poc, change, m15_impulse
    except: return None

data = get_market_data()

if data:
    gold, dxy, yields, news, vol_atr, h4_p, geo, cb, etf, df_h2, ph, pl, poc, g_change, m15_imp = data
    cap, risk_pct = 959.56, 0.06
    sl_dyn = max(vol_atr * 0.5, 15.0)
    perte_gbp = cap * risk_pct
    lot = perte_gbp / (sl_dyn * 10)
    
    # CALCUL DE FORCE NET (MAINTENANT RÉACTIF AU M15)
    drag = (dxy - 100) + (yields * 5)
    bull_score = min(max((geo + cb + etf) - drag + (m15_imp * 10), 10), 100)
    can_buy, can_sell = bull_score > 58, bull_score < 42
    
    # STATUS TAG (Killzone Style)
    status_text = "NEUTRAL - LOW" if 40 < bull_score < 55 else "BULLISH" if bull_score >= 55 else "BEARISH"
    status_color = "#ffb000" if "NEUTRAL" in status_text else "#00ff88" if "BULL" in status_text else "#ff4b4b"

    # Header
    st.markdown(f"""<div style='display:flex; justify-content:space-between;'><div><h3 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST UNIT</h3><small style='color:#444;'>V49 TOTAL COCKPIT | SCORE: {bull_score:.0f}</small></div><div class='val-quant'>{gold:,.2f} $ <span class='status-tag' style='background:{status_color}22; color:{status_color}; border:1px solid {status_color};'>{status_text}</span></div></div>""", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

    col_main, col_side = st.columns([2, 1])

    with col_main:
        # ROADMAP
        prog = (math.log(cap/100) / math.log(1000000/100)) * 100
        st.markdown(f"<div class='roadmap-box'><div style='display:flex; justify-content:space-between; font-size:10px;'><span>PROG: {prog:.2f}%</span><span style='color:#ffb000;'>SOLDE: {cap} £</span></div><div style='background:#222; height:6px; margin:5px 0;'><div style='background:#ffb000; height:100%; width:{prog}%;'></div></div></div>", unsafe_allow_html=True)
        
        # LEGENDE CENTRALE (V48 Restored)
        st.markdown(f"""<div class="legende-centrale"><b style="color:#ffb000;">⚖️ PROTOCOLE :</b> 🟢 ACHAT > 58% | 🔴 VENTE < 42% | RISQUE 6% FIXE.</div>""", unsafe_allow_html=True)

        # CHART
        fig = go.Figure(data=[go.Candlestick(x=df_h2.index, open=df_h2['Open'], high=df_h2['High'], low=df_h2['Low'], close=df_h2['Close'], name="H2")])
        fig.add_hline(y=ph, line_dash="dash", line_color="#ff4b4b", annotation_text="P-HIGH")
        fig.add_hline(y=pl, line_dash="dash", line_color="#00ff88", annotation_text="P-LOW")
        fig.add_hline(y=poc, line_color="#ffb000", line_width=2, annotation_text="POC")
        fig.update_layout(template="plotly_dark", paper_bgcolor="#050505", plot_bgcolor="#050505", height=350, margin=dict(l=0,r=0,t=0,b=0), showlegend=False, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # TARGETS & PROJECTION (V48 Restored)
        st.markdown("<p class='label'>● PARAMÈTRES D'EXÉCUTION & PROJECTION</p>", unsafe_allow_html=True)
        c_t1, c_t2 = st.columns(2)
        with c_t1:
            st.markdown(f"""<div class='kz-card' style='font-size:12px; border-left:3px solid #ffb000;'>
                <small class='label'>TARGETS XAU/USD</small><br>
                🟢 <b>TP (1:2) :</b> {gold + (sl_dyn * 2):,.2f} $<br>
                ⚪ <b>IN (ENTRY) :</b> {gold:,.2f} $<br>
                🔴 <b>SL (EXIT) :</b> {gold - sl_dyn:,.2f} $
            </div>""", unsafe_allow_html=True)
        with c_t2:
            st.markdown(f"""<div class='kz-card' style='font-size:12px; border-left:3px solid #00ff88;'>
                <small class='label'>PROJECTION GBP</small><br>
                💰 <b>GAIN ESTIMÉ :</b> +{perte_gbp * 2:.2f} £<br>
                ⚠️ <b>RISQUE MAX :</b> -{perte_gbp:.2f} £<br>
                📊 <b>LOT CONSEILLÉ :</b> {lot:.2f}
            </div>""", unsafe_allow_html=True)

        # VERDICT GEANT
        st.markdown(f"<div class='kz-card' style='text-align:center; border-top:2px solid {status_color};'><span style='font-size:42px; font-weight:900; color:{status_color};'>{lot:.2f}</span><br><b>{'CONFLUENCE VALIDÉE' if can_buy or can_sell else 'ATTENTE CONFLUENCE'}</b></div>", unsafe_allow_html=True)

    with col_side:
        # BULL VS BEAR (Inspiration Capture 152355)
        st.markdown("<p class='label'>● BULL VS BEAR DOMINANCE</p>", unsafe_allow_html=True)
        st.markdown(f"""<div class='kz-card'><div style='display:flex; justify-content:space-between;'><small>IMPULSE M15</small><small style='color:{"#00ff88" if m15_imp > 0 else "#ff4b4b"};'>{m15_imp:+.3f}</small></div><div class='bar-container'><div class='p-bull' style='width:{bull_score}%'></div><div class='p-bear' style='width:{100-bull_score}%'></div></div></div>""", unsafe_allow_html=True)

        st.markdown("<p class='label'>● PRESSURE SENSORS</p>", unsafe_allow_html=True)
        for ut, pr in [("H4 TREND", h4_p), ("H2 FLOW", h4_p-5), ("M15 MOMENTUM", h4_p+(m15_imp*10))]:
            st.markdown(f"<div style='display:flex; justify-content:space-between;'><small>{ut}</small><small>{pr:.1f}%</small></div><div class='bar-container'><div class='p-bull' style='width:{pr}%'></div></div>", unsafe_allow_html=True)

        st.metric("DXY INDEX", f"{dxy:.2f}")
        st.metric("REAL YIELDS", f"{yields:.2f}%")
        
        st.markdown("<p class='label'>● MATRIX ROADMAP</p>", unsafe_allow_html=True)
        tp, tr = cap, cap
        for i in range(1, 4):
            tp *= 2
            ret = (tr * 0.1) if tr > 5000 else 0
            tr = (tr * 2) - ret
            st.markdown(f"<div class='matrix-row' style='padding:5px 10px;'><div class='m-id'>P{i:02}</div><div style='color:white; font-weight:bold;'>{tr:,.0f}£</div><div style='color:#00ff88;'>L:{(tr*0.06)/(sl_dyn*10):.2f}</div></div>", unsafe_allow_html=True)

    st.markdown(f"<div style='background:{status_color}; color:black; text-align:center; padding:10px; font-weight:900; border-radius:4px;'>VERDICT FINAL : {status_text} | {'VALIDÉ' if can_buy or can_sell else 'NEUTRE'}</div>", unsafe_allow_html=True)

import time
time.sleep(2)
st.rerun()
