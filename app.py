import streamlit as st
import yfinance as yf
import feedparser
import math
import pandas as pd
from datetime import datetime, timedelta

# 1. Configuration & Design System (V39 - Time Impact Matrix)
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
    .roadmap-box { background: linear-gradient(90deg, #0d0d0d 0%, #1a1a1a 100%); border-left: 3px solid #ffb000; padding: 8px; margin-top: 5px; border-radius: 0 4px 4px 0; }
    
    .bar-container { background: #1a1a1a; height: 6px; border-radius: 3px; margin: 4px 0 10px 0; overflow: hidden; display: flex; }
    .p-bull { background: #00ff88; height: 100%; transition: 0.5s; }
    .p-bear { background: #ff4b4b; height: 100%; transition: 0.5s; }

    /* MATRIX ROADMAP STYLE */
    .matrix-row {
        display: flex; justify-content: space-between; align-items: center;
        background: rgba(20, 20, 20, 0.5); border: 1px solid #1a1a1a;
        margin-bottom: 4px; padding: 8px 12px; border-radius: 4px; transition: 0.3s;
    }
    .m-id { color: #ffb000; font-family: 'JetBrains Mono'; font-weight: 900; font-size: 12px; width: 40px; }
    .m-cap { color: #fff; font-weight: bold; font-size: 12px; width: 100px; }
    .m-lot { color: #00ff88; font-family: 'JetBrains Mono'; font-size: 11px; width: 80px; }
    .m-time { color: #666; font-size: 10px; width: 140px; line-height: 1.1; }
    .m-badge {
        padding: 2px 8px; border-radius: 10px; font-size: 8px; font-weight: bold;
        text-transform: uppercase; background: rgba(255, 75, 75, 0.1);
        color: #ff4b4b; border: 1px solid rgba(255, 75, 75, 0.2); width: 90px; text-align: center;
    }
    .m-badge-safe { color: #58a6ff; border-color: #58a6ff; background: rgba(88, 166, 255, 0.1); }
</style>
""", unsafe_allow_html=True)

def get_flow_data(ticker_symbol):
    try:
        t = yf.Ticker(ticker_symbol)
        h4 = t.history(period="5d", interval="4h")
        h2 = t.history(period="2d", interval="1h")
        m15 = t.history(period="1d", interval="15m")
        def calc(df):
            if df.empty: return 50
            return min(max(50 + ((df['Close'].iloc[-1] - df['Close'].mean()) / df['Close'].mean() * 1000), 10), 90)
        return calc(h4), calc(h2), calc(m15)
    except: return 50, 50, 50

def get_market_data():
    try:
        ticker = yf.Ticker("GC=F")
        gold = ticker.fast_info['last_price']
        hist = ticker.history(period="5d")
        vol_atr = (hist['High'] - hist['Low']).mean()
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        feed = feedparser.parse("https://news.google.com/rss/search?q=or+bourse+fortex&hl=fr&gl=FR&ceid=FR:fr")
        news = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)[:4]
        text_blob = " ".join([n.title.lower() for n in news])
        geo = 32.50 if any(w in text_blob for w in ['guerre', 'tension', 'iran']) else 28.0
        cb = 21.40 if any(w in text_blob for w in ['fed', 'taux']) else 18.0
        etf = 11.20 if any(w in text_blob for w in ['etf']) else 9.0
        h4, h2, m15 = get_flow_data("GC=F")
        return gold, dxy, yields, news, geo, cb, etf, vol_atr, h4, h2, m15
    except: return None

data = get_market_data()

if data:
    gold, dxy, yields, news, geo, cb, etf, vol_atr, h4_p, h2_p, m15_p = data
    cap, risk_pct = 959.56, 0.06
    sl_dyn = max(vol_atr * 0.5, 15.0) 
    perte_gbp = cap * risk_pct
    lot = perte_gbp / (sl_dyn * 10)
    
    bull_score = min(max((geo + cb + etf) - ((dxy - 100) + (yields * 5)), 10), 100)
    can_trade = bull_score > 58 and yields < 2.00
    p_rest = math.log(1000000 / cap) / math.log(2)
    prog = (math.log(cap/100) / math.log(1000000/100)) * 100

    st.markdown(f"<div style='display:flex; justify-content:space-between;'><div><h3 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST UNIT</h3><small style='color:#444;'>V39 TIME-IMPACT ROADMAP</small></div><div class='val-quant'>{gold:,.2f} $</div></div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.markdown("<p class='label'>● ROADMAP STRATÉGIQUE</p>", unsafe_allow_html=True)
        st.markdown(f"""<div class='roadmap-box'><div style='display:flex; justify-content:space-between; font-size:10px;'><span>Doublements restants : <b>{p_rest:.1f}</b></span><span style='color:#ffb000;'>{prog:.2f}%</span></div><div style='background:#222; height:6px; margin:5px 0;'><div style='background:#ffb000; height:100%; width:{prog}%;'></div></div></div>""", unsafe_allow_html=True)

        st.markdown(f"<div class='kz-card' style='font-size:10px; color:#aaa;'>DISCIPLINE : Risque {perte_gbp:.2f}£ | SL {sl_dyn:.1f}$ | BE après TP1</div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"<div class='kz-card' style='text-align:center; border-left:3px solid #00ff88;'><small class='label'>LOT CALCULÉ</small><br><span style='font-size:36px; font-weight:900; color:#00ff88;'>{lot:.2f}</span><br><b style='color:{'#00ff88' if can_trade else '#ffb000'};'>{'SIGNAL VALIDÉ' if can_trade else 'WAITING'}</b></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='kz-card' style='font-size:11px;'><small class='label'>TARGETS</small><br>🟢 TP : {gold+sl_dyn*2:,.1f}<br>⚪ IN : {gold:,.1f}<br>🔴 SL : {gold-sl_dyn:,.1f}</div>", unsafe_allow_html=True)

        st.markdown("<p class='label'>● COURBE DE CROISSANCE</p>", unsafe_allow_html=True)
        p_list = []
        t_cap_pure = cap
        t_cap_retrait = cap
        now = datetime.now()
        for i in range(1, 12):
            t_cap_pure *= 2
            t_cap_retrait = (t_cap_retrait * 2) - (t_cap_retrait * 0.1 if t_cap_retrait > 5000 else 0)
            
            # Temps estimé (1 mois par palier sans retrait, 1.3 avec retrait)
            d_pure = now + timedelta(days=i * 30)
            d_retrait = now + timedelta(days=i * 39)
            
            p_list.append({
                "ID": f"P{i:02}", 
                "Cap": t_cap_pure, 
                "Lot": (t_cap_pure * risk_pct) / (sl_dyn * 10),
                "T_Pure": d_pure.strftime('%m/%y'),
                "T_Ret": d_retrait.strftime('%m/%y'),
                "Ret": t_cap_pure * 0.1 if t_cap_pure > 5000 else 0
            })
        st.line_chart(pd.DataFrame(p_list).set_index("ID")["Cap"])

        st.markdown("<p class='label'>● MATRIX ROADMAP & IMPACT TEMPOREL</p>", unsafe_allow_html=True)
        for p in p_list[:10]:
            b_class = "m-badge-safe" if p['Ret'] > 0 else ""
            b_text = f"RETRAIT: {p['Ret']:,.0f}£" if p['Ret'] > 0 else "ACCUMULATION"
            st.markdown(f"""
            <div class="matrix-row">
                <div class="m-id">{p['ID']}</div>
                <div class="m-cap">{p['Cap']:,.0f} £</div>
                <div class="m-lot">Lot: {p['Lot']:.2f}</div>
                <div class="m-time">🚀 Brut: {p['T_Pure']}<br>🐢 Sortie: {p['T_Ret']}</div>
                <div class="m-badge {b_class}">{b_text}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_side:
        st.markdown("<p class='label'>● PRESSURE SENSORS</p>", unsafe_allow_html=True)
        for ut, pr in [("H4 TREND", h4_p), ("H2 FLOW", h2_p), ("M15 MOMENTUM", m15_p)]:
            st.markdown(f"<div style='display:flex; justify-content:space-between;'><small style='font-size:9px;'>{ut}</small><small style='color:{'#00ff88' if pr > 50 else '#ff4b4b'}; font-weight:bold;'>{pr:.1f}%</small></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='bar-container'><div class='p-bull' style='width:{pr}%'></div><div class='p-bear' style='width:{100-pr}%'></div></div>", unsafe_allow_html=True)

        st.metric("DXY INDEX", f"{dxy:.2f}")
        st.metric("REAL YIELDS", f"{yields:.2f}%")
        st.markdown(f"<div class='kz-card' style='font-size:10px;'>🌍 Géo: +{geo:.1f} | 🏛️ BCE: +{cb:.1f} | 💰 ETF: +{etf:.1f}</div>", unsafe_allow_html=True)

        st.markdown("<p class='label'>● NEWS STREAM</p>", unsafe_allow_html=True)
        for n in news[:3]:
            st.markdown(f"<div style='font-size:10px; margin-bottom:5px; border-bottom:1px solid #111; padding-bottom:3px;'>🕒 {n.published[5:11]} | {n.title[:50]}...</div>", unsafe_allow_html=True)

    v_color = '#00ff88' if can_trade and m15_p > 50 else '#ffb000'
    st.markdown(f"<div style='background:{v_color}; color:black; text-align:center; padding:6px; font-weight:900; font-size:12px; border-radius:4px;'>VERDICT : {'CONFLUENCE TOTALE' if can_trade and m15_p > 50 else 'ATTENTE SIGNAL M15'}</div>", unsafe_allow_html=True)

import time
time.sleep(2)
st.rerun()
