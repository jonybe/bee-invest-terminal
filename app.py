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
    .m-badge-red { padding: 4px 10px; border-radius: 12px; font-size: 8.5px; font-weight: bold; text-transform: uppercase; background: rgba(255, 75, 75, 0.1); color: #ff4b4b; border: 1px solid rgba(255, 75, 75, 0.2); width: 110px; text-align: center; }
    .m-badge-blue { padding: 4px 10px; border-radius: 12px; font-size: 8.5px; font-weight: bold; text-transform: uppercase; background: rgba(88, 166, 255, 0.1); color: #58a6ff; border: 1px solid #58a6ff33; width: 110px; text-align: center; }
    
    .bar-container { background: #1a1a1a; height: 6px; border-radius: 3px; margin: 4px 0 10px 0; overflow: hidden; display: flex; }
    .p-bull { background: #00ff88; height: 100%; transition: 0.5s; }
    .p-bear { background: #ff4b4b; height: 100%; transition: 0.5s; }
    .legende-centrale { font-size: 11px; color: #888; line-height: 1.6; padding: 15px; background: #0a0a0a; border-radius: 4px; border-left: 4px solid #ffb000; margin: 15px 0; }
    
    .intel-desk { background: #080808; border: 1px dashed #333; padding: 20px; border-radius: 4px; margin-top: 30px; }
</style>
""", unsafe_allow_html=True)

def get_market_data():
    try:
        t = yf.Ticker("GC=F")
        gold = t.fast_info['last_price']
        df_h2 = t.history(period="10d", interval="1h").resample('2h').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}).dropna()
        yesterday = t.history(period="2d", interval="15m")
        p_high, p_low = yesterday.iloc[:int(len(yesterday)/2)]['High'].max(), yesterday.iloc[:int(len(yesterday)/2)]['Low'].min()
        poc = yesterday.iloc[:int(len(yesterday)/2)]['Close'].mode().iloc[0]
        m15_imp = ((yesterday['Close'].iloc[-1] - yesterday['Close'].iloc[-2]) / yesterday['Close'].iloc[-2]) * 100
        
        hist = t.history(period="5d")
        vol_atr = (hist['High'] - hist['Low']).mean()
        change = ((gold - hist['Close'].iloc[-1]) / hist['Close'].iloc[-1]) * 100
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        
        feed = feedparser.parse("https://news.google.com/rss/search?q=gold+forex&hl=en")
        news = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)[:4]
        text = " ".join([n.title.lower() for n in news])
        geo, cb, etf = (32.5, 21.4, 11.2) if "war" in text or "tension" in text else (28.0, 18.0, 9.0)
        h4_p = min(max(50 + ((df_h2['Close'].iloc[-1] - df_h2['Close'].mean())/2), 10), 90)
        return gold, dxy, yields, news, vol_atr, h4_p, geo, cb, etf, df_h2, p_high, p_low, poc, change, m15_imp
    except: return None

data = get_market_data()

if data:
    gold, dxy, yields, news, vol_atr, h4_p, geo, cb, etf, df_h2, ph, pl, poc, g_change, m15_imp = data
    cap, risk_pct = 959.56, 0.06
    sl_dyn = max(vol_atr * 0.5, 15.0)
    perte_gbp = cap * risk_pct
    lot = perte_gbp / (sl_dyn * 10)
    drag = (dxy - 100) + (yields * 5)
    bull_score = min(max((geo + cb + etf) - drag + (m15_imp * 10), 10), 100)
    status_text = "NEUTRAL" if 42 <= bull_score <= 58 else "BULLISH" if bull_score > 58 else "BEARISH"
    status_color = "#ffb000" if "NEUTRAL" in status_text else "#00ff88" if "BULL" in status_text else "#ff4b4b"

    # --- Header ---
    st.markdown(f"""<div style='display:flex; justify-content:space-between;'><div><h3 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST UNIT</h3><small style='color:#444;'>V51 INTELLIGENCE STRATEGIST</small></div><div class='val-quant'>{gold:,.2f} $ <small style='color:{status_color};'>[{status_text}]</small></div></div>""", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

    col_main, col_side = st.columns([2, 1])

    with col_main:
        # ROADMAP
        prog = (math.log(cap/100) / math.log(1000000/100)) * 100
        st.markdown(f"<div class='roadmap-box'><div style='display:flex; justify-content:space-between; font-size:10px;'><span>PROG: {prog:.2f}%</span><span style='color:#ffb000;'>SOLDE: {cap} £</span></div><div style='background:#222; height:6px; margin:5px 0;'><div style='background:#ffb000; height:100%; width:{prog}%;'></div></div></div>", unsafe_allow_html=True)
        st.markdown(f"""<div class="legende-centrale"><b style="color:#ffb000;">⚖️ PROTOCOLE :</b> 🟢 ACHAT > 58% | 🔴 VENTE < 42% | RISQUE 6%.</div>""", unsafe_allow_html=True)

        # CHART
        fig = go.Figure(data=[go.Candlestick(x=df_h2.index, open=df_h2['Open'], high=df_h2['High'], low=df_h2['Low'], close=df_h2['Close'], name="H2")])
        fig.add_hline(y=ph, line_dash="dash", line_color="#ff4b4b")
        fig.add_hline(y=pl, line_dash="dash", line_color="#00ff88")
        fig.add_hline(y=poc, line_color="#ffb000", line_width=2)
        fig.update_layout(template="plotly_dark", paper_bgcolor="#050505", plot_bgcolor="#050505", height=320, margin=dict(l=0,r=0,t=0,b=0), showlegend=False, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # TARGETS & PROJECTION
        st.markdown("<p class='label'>● PARAMÈTRES D'EXÉCUTION & PROJECTION FINANCIÈRE</p>", unsafe_allow_html=True)
        c_t1, c_t2 = st.columns(2)
        with c_t1:
            st.markdown(f"""<div class='kz-card' style='font-size:12px; border-left:3px solid #ffb000;'>
                🟢 <b>TP (1:2) :</b> {gold + (sl_dyn * 2):,.2f} $<br>
                ⚪ <b>IN (ENTRY) :</b> {gold:,.2f} $<br>
                🔴 <b>SL (EXIT) :</b> {gold - sl_dyn:,.2f} $
            </div>""", unsafe_allow_html=True)
        with c_t2:
            st.markdown(f"""<div class='kz-card' style='font-size:12px; border-left:3px solid #00ff88;'>
                💰 <b>GAIN ESTIMÉ :</b> +{perte_gbp * 2:.2f} £<br>
                ⚠️ <b>RISQUE MAX :</b> -{perte_gbp:.2f} £<br>
                📊 <b>LOT CONSEILLÉ :</b> {lot:.2f}
            </div>""", unsafe_allow_html=True)

        # MATRIX ROADMAP
        st.markdown("<p class='label'>● MATRIX ROADMAP : ÉVOLUTION DU CAPITAL RÉEL</p>", unsafe_allow_html=True)
        tr = cap
        now = datetime.now()
        for i in range(1, 6):
            ret = (tr * 0.1) if tr > 5000 else 0
            tr = (tr * 2) - ret
            badge = f"<div class='m-badge-blue'>SORTIE: {ret:,.0f}£</div>" if ret > 0 else f"<div class='m-badge-red'>ACCUMULATION</div>"
            st.markdown(f"""<div class="matrix-row"><div class="m-id">P{i:02}</div><div style="width:180px;"><div style="color:white; font-weight:bold; font-size:13px;">{tr:,.0f} £</div></div><div style="color:#00ff88; font-weight:bold; width:80px;">LOT: {(tr*0.06)/(sl_dyn*10):.2f}</div><div style="color:#555; font-size:10px; width:100px;">🚀 {(now+timedelta(days=i*30)).strftime('%m/%y')}</div>{badge}</div>""", unsafe_allow_html=True)

    with col_side:
        st.markdown("<p class='label'>● BULL VS BEAR DOMINANCE</p>", unsafe_allow_html=True)
        st.markdown(f"""<div class='kz-card'><div style='display:flex; justify-content:space-between;'><small>IMPULSE SCORE</small><small style='color:{status_color};'>{m15_imp:+.3f}</small></div><div class='bar-container'><div class='p-bull' style='width:{bull_score}%'></div><div class='p-bear' style='width:{100-bull_score}%'></div></div></div>""", unsafe_allow_html=True)
        st.metric("DXY INDEX", f"{dxy:.2f}")
        st.metric("REAL YIELDS", f"{yields:.2f}%")
        st.markdown("<p class='label'>● PRESSURE SENSORS</p>", unsafe_allow_html=True)
        for ut, pr in [("H4 TREND", h4_p), ("H2 FLOW", h4_p-5), ("M15 MOMENTUM", h4_p+(m15_imp*10))]:
            st.markdown(f"<div style='display:flex; justify-content:space-between;'><small>{ut}</small><small>{pr:.1f}%</small></div><div class='bar-container'><div class='p-bull' style='width:{pr}%'></div></div>", unsafe_allow_html=True)
        st.markdown("<p class='label'>● NEWS STREAM</p>", unsafe_allow_html=True)
        for n in news[:3]:
            st.markdown(f"<div style='font-size:10px; border-bottom:1px solid #111; padding:3px 0;'>🕒 {n.published[5:11]} | {n.title[:50]}...</div>", unsafe_allow_html=True)

    # --- LE BUREAU D'INTELLIGENCE (NOUVEAU BLOC) ---
    st.markdown(f"""
    <div class="intel-desk">
        <h3 style="color:#ffb000; margin-top:0;">⚔️ STRATEGIC INTELLIGENCE : MICRO vs MACRO</h3>
        <p style="color:#888;">Pourquoi le terminal peut différer d'une capture "Killzone" institutionnelle :</p>
        <div style="display:flex; gap:20px;">
            <div style="flex:1; border-right:1px solid #222; padding-right:20px;">
                <b style="color:#ff4b4b;">🔴 MICRO (CAPTURE KILLZONE) :</b><br>
                Regarde le <b>Flux d'Ordres (Tape)</b> immédiat. Si le prix chute de -0.30% en 15min, il passe en "Bearish" instantanément pour protéger le capital. C'est la vue du <b>Sniper</b>.
            </div>
            <div style="flex:1;">
                <b style="color:#00ff88;">🟢 MACRO (TON TERMINAL) :</b><br>
                Regarde la <b>Structure de Fond</b>. Même si le prix baisse sur 15min, si les Banques Centrales achètent et que le DXY est bas, le terminal garde son biais "Bullish". C'est la vue du <b>Stratège</b>.
            </div>
        </div>
        <p style="margin-top:15px; color:#aaa; font-style:italic;">
            📌 <b>CONSEIL :</b> Si le Killzone est Rouge et ton terminal Vert, le marché est en "Divergence". 
            Attends que ton <b>Impulse Score (M15)</b> redevienne positif avant d'exécuter, pour acheter au meilleur prix.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    

    st.markdown(f"<div style='background:{status_color}; color:black; text-align:center; padding:10px; font-weight:900; border-radius:4px; margin-top:10px;'>VERDICT FINAL : {status_text} | {'VALIDÉ' if bull_score > 58 or bull_score < 42 else 'ATTENTE'}</div>", unsafe_allow_html=True)

import time
time.sleep(2)
st.rerun()
