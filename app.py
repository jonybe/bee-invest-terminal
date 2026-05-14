import streamlit as st
import yfinance as yf
import feedparser
import math
import pandas as pd
from datetime import datetime, timedelta

# 1. Configuration & Design System
st.set_page_config(page_title="BEE-INVEST | TOTAL CONTROL", layout="wide")

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #050505; 
        color: #e0e0e0; 
        font-family: 'Inter', sans-serif; 
        font-size: 11.5px; 
    }
    .block-container { padding-top: 3.5rem !important; padding-bottom: 0rem !important; }
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; padding: 12px; border-radius: 4px; margin-bottom: 8px; }
    .label { color: #555; font-size: 9px; text-transform: uppercase; font-weight: bold; letter-spacing: 1.2px; }
    .val-quant { font-family: 'JetBrains Mono', monospace; font-size: 18px; font-weight: bold; color: #00ff88; }
    
    .bar-container { background: #1a1a1a; height: 6px; border-radius: 3px; margin: 4px 0 10px 0; overflow: hidden; display: flex; }
    .p-bull { background: #00ff88; height: 100%; transition: 0.5s; }
    .p-bear { background: #ff4b4b; height: 100%; transition: 0.5s; }

    .matrix-row {
        display: flex; justify-content: space-between; align-items: center;
        background: rgba(15, 15, 15, 0.8); border: 1px solid #1a1a1a;
        margin-bottom: 5px; padding: 12px 18px; border-radius: 4px;
    }
    .m-id { color: #ffb000; font-family: 'JetBrains Mono'; font-weight: 900; width: 45px; font-size: 14px; }
    .m-cap-group { width: 200px; }
    .m-cap-pure { color: #444; font-size: 9px; text-decoration: line-through; margin-bottom: 2px; }
    .m-cap-real { color: #fff; font-weight: bold; font-size: 13.5px; letter-spacing: 0.5px; }
    .m-lot { color: #00ff88; font-family: 'JetBrains Mono'; width: 90px; font-weight: bold; }
    .m-time { color: #555; font-size: 10px; width: 140px; font-family: 'JetBrains Mono'; }
    .m-badge {
        padding: 4px 10px; border-radius: 12px; font-size: 8.5px; font-weight: bold;
        text-transform: uppercase; background: rgba(255, 75, 75, 0.1);
        color: #ff4b4b; border: 1px solid rgba(255, 75, 75, 0.2); width: 110px; text-align: center;
    }
    .m-badge-safe { color: #58a6ff; border-color: #58a6ff; background: rgba(88, 166, 255, 0.1); }
    .legende { font-size: 9px; color: #666; line-height: 1.4; padding: 10px; background: #080808; border-radius: 4px; border: 1px dashed #222; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

def get_flow_data(ticker_symbol):
    try:
        t = yf.Ticker(ticker_symbol)
        h4, h2, m15 = t.history(period="5d", interval="4h"), t.history(period="2d", interval="1h"), t.history(period="1d", interval="15m")
        def calc(df): return min(max(50 + ((df['Close'].iloc[-1] - df['Close'].mean()) / df['Close'].mean() * 1000), 10), 90) if not df.empty else 50
        return calc(h4), calc(h2), calc(m15)
    except: return 50, 50, 50

def get_market_data():
    try:
        ticker = yf.Ticker("GC=F")
        gold = ticker.fast_info['last_price']
        hist = ticker.history(period="5d")
        vol_atr = (hist['High'] - hist['Low']).mean()
        change = ((gold - hist['Close'].iloc[-1]) / hist['Close'].iloc[-1]) * 100
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        
        feed = feedparser.parse("https://news.google.com/rss/search?q=gold+market+forex&hl=en&gl=US&ceid=US:en")
        news = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)[:4]
        text_blob = " ".join([n.title.lower() for n in news])
        
        geo = 32.50 if any(w in text_blob for w in ['war', 'conflict', 'tension', 'iran', 'russia']) else 28.0
        cb = 21.40 if any(w in text_blob for w in ['fed', 'inflation', 'rates', 'hike', 'powell']) else 18.0
        etf = 11.20 if any(w in text_blob for w in ['etf', 'inflow', 'holdings', 'demand']) else 9.0
        
        h4, h2, m15 = get_flow_data("GC=F")
        return gold, dxy, yields, news, vol_atr, h4, h2, m15, change, geo, cb, etf
    except: return None

data = get_market_data()

if data:
    gold, dxy, yields, news, vol_atr, h4_p, h2_p, m15_p, gold_change, geo, cb, etf = data
    cap, risk_pct = 959.56, 0.06
    sl_dyn = max(vol_atr * 0.5, 15.0) 
    perte_gbp = cap * risk_pct
    lot = perte_gbp / (sl_dyn * 10)
    
    # CALCUL DE FORCE NET (BULL SCORE)
    drag = (dxy - 100) + (yields * 5)
    bull_score = min(max((geo + cb + etf) - drag, 10), 100)
    
    # LOGIQUE D'AUTORISATION
    # ACHAT : Bull Score > 58% ET Momentum M15 > 50%
    # VENTE : Bull Score < 42% ET Momentum M15 < 50%
    can_buy = bull_score > 58 and m15_p > 50
    can_sell = bull_score < 42 and m15_p < 50
    
    p_rest, prog = math.log(1000000 / cap) / math.log(2), (math.log(cap/100) / math.log(1000000/100)) * 100

    # Header
    st.markdown(f"<div style='display:flex; justify-content:space-between;'><div><h3 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST UNIT</h3><small style='color:#444;'>V43 TACTICAL INTELLIGENCE | RISK: {perte_gbp:.2f} £</small></div><div class='val-quant'>{gold:,.2f} $</div></div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.markdown(f"<div class='roadmap-box'><div style='display:flex; justify-content:space-between; font-size:10px;'><span>Doublements : <b>{p_rest:.1f}</b></span><span style='color:#ffb000;'>PROG: {prog:.2f}%</span></div><div style='background:#222; height:6px; margin:5px 0;'><div style='background:#ffb000; height:100%; width:{prog}%;'></div></div></div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"<div class='kz-card' style='text-align:center; border-left:3px solid #00ff88;'><small class='label'>LOT ACTUEL ATR</small><br><span style='font-size:36px; font-weight:900; color:#00ff88;'>{lot:.2f}</span><br><b style='color:{'#00ff88' if can_buy else '#ff4b4b' if can_sell else '#ffb000'};'>{'ACHAT VALIDÉ' if can_buy else 'VENTE VALIDÉE' if can_sell else 'ATTENTE CONFLUENCE'}</b></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='kz-card' style='font-size:11px;'><small class='label'>NIVEAUX TECHNIQUES</small><br>🟢 TP : {gold+sl_dyn*2:,.1f}<br>⚪ IN : {gold:,.1f}<br>🔴 SL : {gold-sl_dyn:,.1f}</div>", unsafe_allow_html=True)

        st.markdown("<p class='label'>● PLAN DE CAPITALISATION DÉTAILLÉ (SOLDE RÉEL)</p>", unsafe_allow_html=True)
        t_cap_pure, t_cap_real = cap, cap
        now = datetime.now()
        for i in range(1, 11):
            t_cap_pure *= 2
            retrait = (t_cap_real * 0.1) if t_cap_real > 5000 else 0
            t_cap_real = (t_cap_real * 2) - retrait
            st.markdown(f"""
            <div class="matrix-row">
                <div class="m-id">P{i:02}</div>
                <div class="m-cap-group"><div class="m-cap-pure">BRUT: {t_cap_pure:,.0f} £</div><div class="m-cap-real">{t_cap_real:,.0f} £</div></div>
                <div class="m-lot">LOT: {(t_cap_real * risk_pct) / (sl_dyn * 10):.2f}</div>
                <div class="m-time">🚀 {(now+timedelta(days=i*30)).strftime('%m/%Y')}<br>🐢 {(now+timedelta(days=i*39)).strftime('%m/%Y')}</div>
                <div class="m-badge {'m-badge-safe' if retrait > 0 else ''}">{f"SORTIE: {retrait:,.0f}£" if retrait > 0 else "FULL REINVEST"}</div>
            </div>""", unsafe_allow_html=True)

    with col_side:
        st.markdown("<p class='label'>● GOLD INSIGHTS & BULL SCORE</p>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='kz-card' style='border-right: 3px solid #ffb000;'>
            <div style='display:flex; justify-content:space-between; margin-bottom:5px;'><span style='color:#666;'>Volatilité (ATR) :</span><span style='color:#fff;'>{vol_atr:.2f} $</span></div>
            <div style='display:flex; justify-content:space-between; margin-bottom:10px;'><span style='color:#666;'>Variation J :</span><span style='color:{'#00ff88' if gold_change > 0 else '#ff4b4b'};'>{gold_change:+.2f}%</span></div>
            <hr style='border-color:#222;'>
            <div style='display:flex; justify-content:space-between; margin-top:10px;'>
                <span class='label' style='color:#00ff88;'>BULL SCORE NET :</span><span style='color:#00ff88; font-weight:bold; font-size:14px;'>{bull_score:.1f}%</span>
            </div>
            <div class='bar-container' style='height:10px;'><div class='p-bull' style='width:{bull_score}%'></div><div class='p-bear' style='width:{100-bull_score}%'></div></div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<p class='label'>● PRESSURE SENSORS</p>", unsafe_allow_html=True)
        for ut, pr in [("H4 TREND", h4_p), ("H2 FLOW", h2_p), ("M15 MOMENTUM", m15_p)]:
            st.markdown(f"<div style='display:flex; justify-content:space-between;'><small style='font-size:9px;'>{ut}</small><small style='color:{'#00ff88' if pr > 50 else '#ff4b4b'};'>{pr:.1f}%</small></div><div class='bar-container'><div class='p-bull' style='width:{pr}%'></div><div class='p-bear' style='width:{100-pr}%'></div></div>", unsafe_allow_html=True)

        st.metric("DXY INDEX", f"{dxy:.2f}")
        st.metric("REAL YIELDS", f"{yields:.2f}%")

    # FOOTER VERDICT + LÉGENDE TACTIQUE
    v_color = '#00ff88' if can_buy else '#ff4b4b' if can_sell else '#ffb000'
    v_text = 'CONFLUENCE ACHAT ✅' if can_buy else 'CONFLUENCE VENTE 🔴' if can_sell else 'ATTENTE CONFLUENCE ⏳'
    st.markdown(f"<div style='background:{v_color}; color:black; text-align:center; padding:8px; font-weight:900; font-size:13px; border-radius:4px;'>VERDICT FINAL : {v_text}</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="legende">
        <b>⚖️ LÉGENDE DES SIGNAUX :</b><br>
        • 🟢 <b>ACHAT (>58%) :</b> La macro (Géo+ETF) et la baisse du DXY/Yields créent une pression haussière dominante. Autorisé si M15 est Vert.<br>
        • 🔴 <b>VENTE (<42%) :</b> Le Dollar et les Yields écrasent l'Or. La macro est défavorable. Autorisé si M15 est Rouge.<br>
        • ⏳ <b>NEUTRE (42-58%) :</b> Zone de combat ou manque de news majeures. Risque de "choppiness". Attendre une sortie de zone.
    </div>
    """, unsafe_allow_html=True)

import time
time.sleep(2)
st.rerun()
