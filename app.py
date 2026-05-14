import streamlit as st
import yfinance as yf
import feedparser
import math
import pandas as pd
from datetime import datetime, timedelta

# 1. Configuration & Design System (V36 - Ultra Stylized)
st.set_page_config(page_title="BEE-INVEST | CYBER-QUANT", layout="wide")

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #050505; 
        color: #e0e0e0; 
        font-family: 'Inter', sans-serif; 
        font-size: 12px; 
    }
    .block-container { padding-top: 3.5rem !important; padding-bottom: 0rem !important; }
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; padding: 12px; border-radius: 4px; margin-bottom: 8px; }
    .label { color: #555; font-size: 9px; text-transform: uppercase; font-weight: bold; letter-spacing: 1.2px; }
    .val-quant { font-family: 'JetBrains Mono', monospace; font-size: 18px; font-weight: bold; color: #00ff88; }
    .roadmap-box { background: linear-gradient(90deg, #0d0d0d 0%, #1a1a1a 100%); border-left: 3px solid #ffb000; padding: 8px; margin-top: 5px; border-radius: 0 4px 4px 0; }
    .bar-bg { background: #1a1a1a; height: 8px; border-radius: 4px; margin: 8px 0; overflow: hidden; }
    .bar-bull { background: #00ff88; height: 100%; transition: width 1s; }
    .bar-bear { background: #ff4b4b; height: 100%; transition: width 1s; }
    
    /* TABLEAU CYBER-STYLE */
    .matrix-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(20, 20, 20, 0.5);
        border: 1px solid #1a1a1a;
        margin-bottom: 4px;
        padding: 10px 15px;
        border-radius: 4px;
        transition: 0.3s;
    }
    .matrix-row:hover {
        border-color: #ffb000;
        background: rgba(255, 176, 0, 0.05);
        box-shadow: 0 0 15px rgba(255, 176, 0, 0.1);
    }
    .m-id { color: #ffb000; font-family: 'JetBrains Mono'; font-weight: 900; font-size: 14px; width: 50px; }
    .m-cap { color: #fff; font-weight: bold; font-size: 13px; width: 120px; }
    .m-lot { color: #00ff88; font-family: 'JetBrains Mono'; font-size: 12px; width: 100px; }
    .m-date { color: #444; font-size: 11px; width: 80px; }
    .m-badge {
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 8px;
        font-weight: bold;
        text-transform: uppercase;
        background: rgba(255, 75, 75, 0.1);
        color: #ff4b4b;
        border: 1px solid rgba(255, 75, 75, 0.2);
    }
    .m-badge-safe { color: #58a6ff; border-color: #58a6ff; background: rgba(88, 166, 255, 0.1); }
</style>
""", unsafe_allow_html=True)

def get_market_data():
    try:
        ticker = yf.Ticker("GC=F")
        gold = ticker.fast_info['last_price']
        hist = ticker.history(period="5d")
        vol_atr = (hist['High'] - hist['Low']).mean()
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        feed = feedparser.parse("https://news.google.com/rss/search?q=or+bourse+forex&hl=fr&gl=FR&ceid=FR:fr")
        news = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)[:4]
        
        text_blob = " ".join([n.title.lower() for n in news])
        geo = 32.50 if any(w in text_blob for w in ['guerre', 'tension', 'iran', 'russie']) else 28.00
        cb = 21.40 if any(w in text_blob for w in ['fed', 'inflation', 'taux', 'powell']) else 18.00
        etf = 11.20 if any(w in text_blob for w in ['etf', 'achat', 'physique']) else 9.00
        
        return gold, dxy, yields, news, geo, cb, etf, vol_atr
    except: return None

data = get_market_data()

if data:
    gold, dxy, yields, news, geo, cb, etf, vol_atr = data
    cap = 959.56
    risk_pct = 0.06
    sl_dynamique = max(vol_atr * 0.5, 15.0) 
    perte_gbp = cap * risk_pct
    lot = perte_gbp / (sl_dynamique * 10)
    
    bull_score = min(max((geo + cb + etf) - ((dxy - 100) + (yields * 5)), 10), 100)
    bear_score = 100 - bull_score
    can_trade = bull_score > 58 and yields < 2.00
    p_restants = math.log(1000000 / cap) / math.log(2)
    prog = (math.log(cap/100) / math.log(1000000/100)) * 100

    # Header
    h1, h2 = st.columns([2, 1])
    h1.markdown(f"<h3 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST UNIT</h3><small style='color:#444; font-size:8px;'>MATRIX ROADMAP V36 | VOLATILITÉ : {vol_atr:.2f}$</small>", unsafe_allow_html=True)
    h2.markdown(f"<div style='text-align:right;'><span class='val-quant'>{gold:,.2f} $</span><br><small style='color:#444; font-size:9px;'>{datetime.now().strftime('%H:%M:%S')}</small></div>", unsafe_allow_html=True)

    st.markdown("<hr style='margin: 0.2rem 0;'>", unsafe_allow_html=True)

    col_main, col_side = st.columns([2, 1])

    with col_main:
        # ROADMAP
        st.markdown("<p class='label'>● ROADMAP STRATÉGIQUE</p>", unsafe_allow_html=True)
        st.markdown(f"""<div class='roadmap-box'><div style='display:flex; justify-content:space-between; font-size:10px;'><span>Paliers : <b>{p_restants:.1f}</b></span><span style='color:#ffb000;'>{prog:.2f}%</span></div><div style='background:#222; height:6px; margin:5px 0;'><div style='background:#ffb000; height:100%; width:{prog}%;'></div></div></div>""", unsafe_allow_html=True)

        # DISCIPLINE
        st.markdown(f"""<div class='kz-card' style='border-left: 2px solid #555; padding: 10px;'>
            <p class='label' style='margin-bottom:5px;'>● DISCIPLINE DE TRADING</p>
            <div style='display:flex; justify-content:space-between; font-size:10px; color:#aaa;'>
                <span>Risque: 6% ({perte_gbp:.2f}£)</span>
                <span>SL: {sl_dynamique:.1f}$</span>
                <span>TP1: BE ✅</span>
            </div>
        </div>""", unsafe_allow_html=True)

        # EXÉCUTION
        c_ex1, c_ex2 = st.columns(2)
        with c_ex1:
            st.markdown(f"""<div class='kz-card' style='text-align:center; border-left: 3px solid #00ff88;'>
                <small class='label'>LOT CALCULÉ</small><br>
                <span style='font-size:36px; font-weight:900; color:#00ff88;'>{lot:.2f}</span><br>
                <b style='font-size:11px; color:{'#00ff88' if can_trade else '#ffb000'};'>{'ACHAT VALIDÉ' if can_trade else 'WAITING'}</b>
            </div>""", unsafe_allow_html=True)
        with c_ex2:
            st.markdown(f"""<div class='kz-card' style='font-size:11px;'>
                <small class='label'>TARGETS</small><br>
                🟢 TP : <b>{gold+sl_dynamique*2:,.1f}</b><br>
                ⚪ IN : <b>{gold:,.1f}</b><br>
                🔴 SL : <b>{gold-sl_dynamique:,.1f}</b>
            </div>""", unsafe_allow_html=True)

        # DIAGRAMME
        st.markdown("<p class='label'>● COURBE DE CROISSANCE</p>", unsafe_allow_html=True)
        p_list = []
        temp_cap = cap
        now = datetime.now()
        for i in range(1, 12):
            temp_cap *= 2
            date_p = now + timedelta(days=i*1.2*30)
            p_list.append({"ID": f"P{i:02}", "Capital": temp_cap, "Lot": (temp_cap * risk_pct) / (sl_dynamique * 10), "Echéance": date_p.strftime('%m/%Y'), "Retrait": temp_cap * 0.1 if temp_cap > 5000 else 0})
        df_p = pd.DataFrame(p_list)
        st.line_chart(df_p.set_index("ID")["Capital"])
        
        # TABLEAU MATRIX STYLISÉ
        st.markdown("<p class='label'>● PLAN DE CAPITALISATION MATRIX</p>", unsafe_allow_html=True)
        for _, row in df_p.head(10).iterrows():
            badge_class = "m-badge-safe" if row['Retrait'] > 0 else ""
            badge_text = f"RETRAIT: {row['Retrait']:,.0f}£" if row['Retrait'] > 0 else "ACCUMULATION"
            
            st.markdown(f"""
            <div class="matrix-row">
                <div class="m-id">{row['ID']}</div>
                <div class="m-cap">{row['Capital']:,.0f} £</div>
                <div class="m-lot">Lot: {row['Lot']:.2f}</div>
                <div class="m-date">{row['Echéance']}</div>
                <div class="m-badge {badge_class}">{badge_text}</div>
            </div>
            """, unsafe_allow_html=True)

        # NEWS
        st.markdown("<br><p class='label'>● NEWS STREAM</p>", unsafe_allow_html=True)
        for n in news:
            with st.expander(f"🕒 {n.published[5:16]} | {n.title[:65]}..."):
                st.markdown(f"<small style='color:#aaa;'>{n.title}</small><br>[Article]({n.link})", unsafe_allow_html=True)

    with col_side:
        # DOMINANCE
        st.markdown("<p class='label'>● DOMINANCE</p>", unsafe_allow_html=True)
        st.markdown(f"<small style='color:#00ff88;'>BULL : {bull_score:.1f}%</small><div class='bar-bg'><div class='bar-bull' style='width:{bull_score}%'></div></div>", unsafe_allow_html=True)
        st.markdown(f"<small style='color:#ff4b4b;'>BEAR : {bear_score:.1f}%</small><div class='bar-bg'><div class='bar-bear' style='width:{bear_score}%'></div></div>", unsafe_allow_html=True)
        
        st.markdown("<hr style='border-color:#222;'>", unsafe_allow_html=True)
        st.metric("DXY BROAD", f"{dxy:.2f}")
        st.metric("REAL YIELDS", f"{yields:.2f}%")
        
        st.markdown(f"""<div class='kz-card' style='font-size:10px; padding:8px;'>
            <p class='label'>SENSORS</p>
            🌍 Géo : <b>+{geo:.1f}</b><br>
            🏛️ BCE : <b>+{cb:.1f}</b><br>
            💰 ETF : <b>+{etf:.1f}</b>
        </div>""", unsafe_allow_html=True)

    # Footer
    st.markdown(f"<div style='background:{'#00ff88' if can_trade else '#ffb000'}; color:black; text-align:center; padding:6px; font-weight:900; font-size:12px; border-radius:4px; margin-top:5px;'>VERDICT : {'ACCORD EXÉCUTION' if can_trade else 'ATTENTE CONFLUENCE'}</div>", unsafe_allow_html=True)

import time
time.sleep(2)
st.rerun()
