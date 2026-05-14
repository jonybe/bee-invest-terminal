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
    .bar-container { background: #1a1a1a; height: 6px; border-radius: 3px; margin: 4px 0 10px 0; overflow: hidden; display: flex; }
    .p-bull { background: #00ff88; height: 100%; transition: 0.5s; }
    .p-bear { background: #ff4b4b; height: 100%; transition: 0.5s; }
    .matrix-row { display: flex; justify-content: space-between; align-items: center; background: rgba(15, 15, 15, 0.8); border: 1px solid #1a1a1a; margin-bottom: 5px; padding: 10px 15px; border-radius: 4px; }
    .m-id { color: #ffb000; font-family: 'JetBrains Mono'; font-weight: 900; width: 45px; font-size: 14px; }
    .m-cap-group { width: 200px; }
    .m-cap-real { color: #fff; font-weight: bold; font-size: 13.5px; }
    .m-lot { color: #00ff88; font-family: 'JetBrains Mono'; width: 90px; }
    .legende-centrale { font-size: 11px; color: #888; line-height: 1.6; padding: 15px; background: #0a0a0a; border-radius: 4px; border-left: 4px solid #ffb000; margin: 15px 0; }
</style>
""", unsafe_allow_html=True)

def get_market_data():
    try:
        t = yf.Ticker("GC=F")
        gold = t.fast_info['last_price']
        
        # Données pour le Graphique H2 (5 jours pour avoir assez de recul)
        df_h2 = t.history(period="10d", interval="1h") # On prend 1h pour simuler 2h précisément
        df_h2 = df_h2.resample('2h').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}).dropna()
        
        # Données de la veille pour VA/POC
        yesterday = t.history(period="2d", interval="15m")
        prev_day = yesterday.iloc[:int(len(yesterday)/2)]
        p_high, p_low = prev_day['High'].max(), prev_day['Low'].min()
        poc = prev_day['Close'].mode().iloc[0] # Simplification POC
        va_high = poc + (p_high - poc) * 0.70
        va_low = poc - (poc - p_low) * 0.70

        hist = t.history(period="5d")
        vol_atr = (hist['High'] - hist['Low']).mean()
        dxy = yf.Ticker("DX-Y.NYB").history(period="1d")['Close'].iloc[-1]
        yields = yf.Ticker("^TNX").history(period="1d")['Close'].iloc[-1] / 10
        
        # News & Force
        feed = feedparser.parse("https://news.google.com/rss/search?q=gold+market+forex&hl=en")
        news = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)[:4]
        text = " ".join([n.title.lower() for n in news])
        geo = 32.5 if any(w in text for w in ['war', 'tension']) else 28.0
        cb = 21.4 if any(w in text for w in ['fed', 'rate']) else 18.0
        etf = 11.2 if any(w in text for w in ['etf', 'demand']) else 9.0
        
        # Flux
        h4_p = min(max(50 + ((df_h2['Close'].iloc[-1] - df_h2['Close'].rolling(20).mean().iloc[-1]) / 2), 10), 90)
        
        return gold, dxy, yields, news, vol_atr, h4_p, geo, cb, etf, df_h2, p_high, p_low, poc, va_high, va_low
    except: return None

data = get_market_data()

if data:
    gold, dxy, yields, news, vol_atr, h4_p, geo, cb, etf, df_h2, ph, pl, poc, vah, val = data
    cap, risk = 959.56, 0.06
    sl_dyn = max(vol_atr * 0.5, 15.0)
    lot = (cap * risk) / (sl_dyn * 10)
    bull_score = min(max((geo + cb + etf) - ((dxy - 100) + (yields * 5)), 10), 100)
    can_buy, can_sell = bull_score > 58, bull_score < 42

    # Header
    st.markdown(f"<div style='display:flex; justify-content:space-between;'><div><h3 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST UNIT</h3><small style='color:#444;'>V46 TACTICAL CHART H2 | VA-POC ACTIVE</small></div><div class='val-quant'>{gold:,.2f} $</div></div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

    col_main, col_side = st.columns([2, 1])

    with col_main:
        # ROADMAP
        prog = (math.log(cap/100) / math.log(1000000/100)) * 100
        st.markdown(f"<div class='roadmap-box'><div style='display:flex; justify-content:space-between; font-size:10px;'><span>Doublements restants : <b>{math.log(1000000/cap)/math.log(2):.1f}</b></span><span style='color:#ffb000;'>PROG: {prog:.2f}%</span></div><div style='background:#222; height:6px; margin:5px 0;'><div style='background:#ffb000; height:100%; width:{prog}%;'></div></div></div>", unsafe_allow_html=True)

        st.markdown(f"""<div class="legende-centrale"><b>⚖️ PROTOCOLE TACTIQUE :</b> 🟢 ACHAT > 58% | 🔴 VENTE < 42% | ⏳ NEUTRE ENTRE LES DEUX.</div>""", unsafe_allow_html=True)

        # GRAPHIC H2 TACTICAL
        st.markdown("<p class='label'>● ANALYSE FLUX H2 & ZONES DE VALEUR (VA/POC)</p>", unsafe_allow_html=True)
        fig = go.Figure(data=[go.Candlestick(x=df_h2.index, open=df_h2['Open'], high=df_h2['High'], low=df_h2['Low'], close=df_h2['Close'], name="XAU/USD H2")])
        
        # Niveaux de la veille
        fig.add_hline(y=ph, line_dash="dash", line_color="#ff4b4b", annotation_text="P-HIGH")
        fig.add_hline(y=pl, line_dash="dash", line_color="#00ff88", annotation_text="P-LOW")
        fig.add_hline(y=poc, line_color="#ffb000", line_width=2, annotation_text="POC")
        fig.add_hrect(y0=val, y1=vah, fillcolor="white", opacity=0.05, line_width=0, annotation_text="VALUE AREA")
        
        fig.update_layout(template="plotly_dark", paper_bgcolor="#050505", plot_bgcolor="#050505", height=400, margin=dict(l=0,r=0,t=0,b=0), showlegend=False, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # EXECUTION
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"<div class='kz-card' style='text-align:center; border-left:3px solid #00ff88;'><small class='label'>LOT ACTUEL</small><br><span style='font-size:32px; font-weight:900; color:{'#00ff88' if can_buy else '#ff4b4b' if can_sell else '#ffb000'};'>{lot:.2f}</span><br><small>{'ACHAT' if can_buy else 'VENTE' if can_sell else 'ATTENTE'}</small></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='kz-card' style='font-size:11px;'><small class='label'>NIVEAUX</small><br>🟢 TP: {gold+sl_dyn*2:,.1} | 🔴 SL: {gold-sl_dyn:,.1}</div>", unsafe_allow_html=True)

        # MATRIX
        st.markdown("<p class='label'>● PLAN DE CAPITALISATION MATRIX</p>", unsafe_allow_html=True)
        tr = cap
        for i in range(1, 6):
            tr = (tr * 2) - (tr * 0.1 if tr > 5000 else 0)
            st.markdown(f"<div class='matrix-row'><div class='m-id'>P0{i}</div><div class='m-cap-real'>{tr:,.0f} £</div><div class='m-lot'>LOT: {(tr*risk)/(sl_dyn*10):.2f}</div><div class='m-badge'>SOLDE RÉEL</div></div>", unsafe_allow_html=True)

    with col_side:
        st.markdown("<p class='label'>● BULL SCORE & INSIGHTS</p>", unsafe_allow_html=True)
        st.markdown(f"<div class='kz-card'>BULL SCORE: <b style='color:#00ff88;'>{bull_score:.1f}%</b><div class='bar-container'><div class='p-bull' style='width:{bull_score}%'></div></div><small style='color:#444;'>VOL ATR: {vol_atr:.2f}$</small></div>", unsafe_allow_html=True)
        st.metric("DXY INDEX", f"{dxy:.2f}")
        st.metric("REAL YIELDS", f"{yields:.2f}%")
        st.markdown("<p class='label'>● PRESSURE SENSORS</p>", unsafe_allow_html=True)
        for ut, pr in [("H4 TREND", h4_p), ("H2 FLOW", h4_p-5), ("M15 MOMENTUM", h4_p+10)]:
            st.markdown(f"<small>{ut}</small><div class='bar-container'><div class='p-bull' style='width:{pr}%'></div></div>", unsafe_allow_html=True)
    
    st.markdown(f"<div style='background:{'#00ff88' if can_buy else '#ff4b4b' if can_sell else '#ffb000'}; color:black; text-align:center; padding:10px; font-weight:900; border-radius:4px;'>VERDICT : {'ACHAT VALIDÉ' if can_buy else 'VENTE VALIDÉE' if can_sell else 'NEUTRE'}</div>", unsafe_allow_html=True)

st.rerun()
