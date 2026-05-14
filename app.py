import streamlit as st
import yfinance as yf
import feedparser
import math
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import re

# 1. Configuration & Design System (V76 LOCKED)
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
    .p-bull { background: #00ff88; height: 100%; transition: 0.2s; } 
    .p-bear { background: #ff4b4b; height: 100%; transition: 0.2s; }
    .legende-centrale { font-size: 11px; color: #888; line-height: 1.6; padding: 15px; background: #0a0a0a; border-radius: 4px; border-left: 4px solid #ffb000; margin: 15px 0; }
    .status-tag { padding: 2px 6px; border-radius: 3px; font-size: 9px; font-weight: bold; margin-left: 10px; }
    .cal-row { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid #111; font-size: 10px; }
    .cal-val { font-family: 'JetBrains Mono', monospace; font-weight: bold; width: 45px; text-align: right; }
    .macro-note { font-size: 9px; color: #666; margin-top: -10px; margin-bottom: 10px; font-style: italic; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=2)
def sync_terminal():
    try:
        # 1. FETCH DATA
        t = yf.Ticker("GC=F")
        gold = t.fast_info['last_price']
        df_m15 = t.history(period="2d", interval="15m").dropna()
        m15_imp = ((gold - df_m15['Close'].iloc[-2]) / df_m15['Close'].iloc[-2]) * 100
        
        # 2. VOLUME PROFILE (Fast Render)
        vp_data = df_m15.tail(96).copy()
        price_min, price_max = vp_data['Low'].min(), vp_data['High'].max()
        bins = 30
        bin_size = (price_max - price_min) / bins
        vp_data['bin'] = ((vp_data['Close'] - price_min) / bin_size).astype(int).clip(0, bins-1)
        volume_profile = vp_data.groupby('bin', observed=True)['Volume'].sum()
        
        poc_price = price_min + (volume_profile.idxmax() * bin_size) + (bin_size/2)
        std_dev = vp_data['Close'].std()
        vah, val = poc_price + (std_dev * 1.28), poc_price - (std_dev * 1.28)

        # 3. MACRO & NEWS
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        vix = yf.Ticker("^VIX").fast_info['last_price']
        feed = feedparser.parse("https://news.google.com/rss/search?q=XAU+Gold+PPI+CPI+FED&hl=en")
        
        # 4. SCORES
        text_full = " ".join([n.title.lower() for n in feed.entries])
        geo, cb, etf = (32.5, 21.4, 11.2) if any(x in text_full for x in ["war", "conflict", "tension"]) else (28.0, 18.0, 9.5)
        fund_sent = ((geo + cb + etf) / 65.1) * 100
        
        # 5. ACCOUNT
        cap = 960.23
        perte_gbp = cap * 0.06
        drag = (dxy - 100) + (yields * 5) + (vix * 0.5)
        bull_score = min(max((geo + cb + etf) - drag + (m15_imp * 35), 10), 100)
        status_text = "NEUTRAL" if 42 <= bull_score <= 58 else "BULLISH" if bull_score > 58 else "BEARISH"
        status_color = "#ffb000" if status_text == "NEUTRAL" else "#00ff88" if status_text == "BULLISH" else "#ff4b4b"

        # --- RENDER UI ---
        st.markdown(f"""<div style='display:flex; justify-content:space-between;'><div><h3 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST UNIT</h3><small style='color:#444;'>V76 ENGINE STABILIZED | M15 PRO</small></div><div class='val-quant'>{gold:,.2f} $ <span class='status-tag' style='background:{status_color}22; color:{status_color}; border:1px solid {status_color};'>{status_text}</span></div></div>""", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

        c1, c2 = st.columns([2, 1])
        with c1:
            # Roadmap
            prog = (math.log(cap/100) / math.log(1000000/100)) * 100
            st.markdown(f"<div class='roadmap-box'><div style='display:flex; justify-content:space-between; font-size:10px;'><span>PROG: {prog:.2f}%</span><span style='color:#ffb000;'>SOLDE: {cap} £</span></div><div style='background:#222; height:6px; margin:5px 0;'><div style='background:#ffb000; height:100%; width:{prog}%;'></div></div></div>", unsafe_allow_html=True)
            st.markdown(f"""<div class="legende-centrale"><b style="color:#ffb000;">⚖️ PROTOCOLE :</b> 🟢 ACHAT > 58% | 🔴 VENTE < 42% | RISQUE 6%.</div>""", unsafe_allow_html=True)

            # CHART WITH FAST VOLUME PROFILE
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Candlestick(x=df_m15.index, open=df_m15['Open'], high=df_m15['High'], low=df_m15['Low'], close=df_m15['Close'], name="M15"), secondary_y=False)
            
            # Profil Horizontal (Bar Chart sur Axe X inversé)
            vp_prices = [price_min + (i * bin_size) for i in volume_profile.index]
            fig.add_trace(go.Bar(y=vp_prices, x=volume_profile.values, orientation='h', name="Profile", marker_color="rgba(100,100,100,0.2)", width=bin_size), secondary_y=False)
            
            fig.add_hline(y=poc_price, line_color="#ffb000", line_width=2)
            fig.add_hrect(y0=val, y1=vah, fillcolor="rgba(255, 255, 255, 0.05)", line_width=0)
            fig.update_layout(template="plotly_dark", paper_bgcolor="#050505", plot_bgcolor="#050505", height=320, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False, showlegend=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # STRATEGIC OPPORTUNITY
            st.markdown("<p class='label'>● STRATEGIC OPPORTUNITY FINDER</p>", unsafe_allow_html=True)
            opportunity = "LONG" if status_text == "BULLISH" and gold <= vah else "SHORT" if status_text == "BEARISH" and gold >= val else None
            if opportunity:
                sl_dist = 12.0
                entry_p, tp_p = gold, (gold + sl_dist*2 if opportunity=="LONG" else gold - sl_dist*2)
                sl_p = gold - sl_dist if opportunity=="LONG" else gold + sl_dist
                t_col1, t_col2 = st.columns(2)
                t_col1.markdown(f"<div class='kz-card' style='border-left:3px solid #00ff88;'>🔥 <b>{opportunity} SETUP</b><br>⚪ <b>IN:</b> {entry_p:,.2f}<br>🟢 <b>TP:</b> {tp_p:,.2f}<br>🔴 <b>SL:</b> {sl_p:,.2f}</div>", unsafe_allow_html=True)
                t_col2.markdown(f"<div class='kz-card' style='border-left:3px solid #00ff88;'>📊 <b>LOTS:</b> {perte_gbp/(sl_dist*10):.2f}<br>💰 <b>GAIN:</b> +{perte_gbp*2:.2f} £</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='kz-card' style='text-align:center; color:#444; border:1px dashed #222; padding:20px;'>⌛ <b>WAITING FOR SETUP...</b><br><small>Market: {status_text} | Score: {bull_score:.1f}%</small></div>", unsafe_allow_html=True)

            # Roadmap
            st.markdown("<p class='label'>● MATRIX ROADMAP</p>", unsafe_allow_html=True)
            tr_m = cap
            for i in range(1, 6):
                ret = (tr_m * 0.1) if tr_m > 5000 else 0
                tr_m = (tr_m * 2) - ret
                badge = f"<div class='m-badge-blue'>SORTIE: {ret:,.0f}£</div>" if ret > 0 else f"<div class='m-badge-red'>ACCUMULATION</div>"
                st.markdown(f"""<div class="matrix-row"><div class="m-id">P{i:02}</div><div style="width:150px; color:white; font-weight:bold;">{tr_m:,.0f} £</div><div style="color:#00ff88; font-weight:bold;">LOT: {(tr_m*0.06)/120:.2f}</div>{badge}</div>""", unsafe_allow_html=True)

        with c2:
            st.markdown("<p class='label'>● BULL VS BEAR DOMINANCE</p>", unsafe_allow_html=True)
            st.markdown(f"""<div class='kz-card'><div style='display:flex; justify-content:space-between;'><small>IMPULSE M15</small><small style='color:{status_color};'>{m15_imp:+.3f}%</small></div><div class='bar-container'><div class='p-bull' style='width:{bull_score}%'></div></div></div>""", unsafe_allow_html=True)
            
            st.markdown("<p class='label'>● PRESSURE SENSORS</p>", unsafe_allow_html=True)
            for ut, pr in [("H4 TREND", 55.0), ("H2 FLOW", 50.0), ("M15 MOMENTUM", 50.0+(m15_imp*35))]:
                st.markdown(f"<div style='display:flex; justify-content:space-between;'><small>{ut}</small><small style='color:#00ff88;'>{pr:.1f}%</small></div><div class='bar-container'><div class='p-bull' style='width:{pr}%'></div></div>", unsafe_allow_html=True)
            
            st.markdown("<p class='label'>● FUNDAMENTAL SCORES</p>", unsafe_allow_html=True)
            st.markdown(f"""<div class='kz-card'><div style='display:grid; grid-template-columns:1fr 1fr 1fr; text-align:center;'><div><small>GEO</small><br><b>{geo}</b></div><div><small>FED</small><br><b>{cb}</b></div><div><small>ETF</small><br><b>{etf}</b></div></div><div class='bar-container'><div class='p-bull' style='width:{fund_sent}%'></div></div></div>""", unsafe_allow_html=True)

            st.metric("DXY INDEX", f"{dxy:.2f}")
            st.metric("REAL YIELDS", f"{yields:.2f}%")
            st.metric("VIX INDEX", f"{vix:.2f}")
            
            st.markdown("<p class='label'>● ECONOMIC CALENDAR</p>", unsafe_allow_html=True)
            st.markdown("<div class='kz-card' style='padding:8px;'><div class='cal-header'><span>EVENT</span><span>ACT</span><span>EXP</span></div>" + 
                "".join([f"<div class='cal-row'><span>{n.title[:5]}</span><span style='color:#00ff88;'>--</span><span style='color:#555;'>--</span></div>" for n in feed.entries[:2]]) + "</div>", unsafe_allow_html=True)

        st.markdown(f"<div style='background:{status_color}; color:black; text-align:center; padding:10px; font-weight:900; border-radius:4px; margin-top:10px;'>VERDICT FINAL : {status_text}</div>", unsafe_allow_html=True)

    except Exception: st.warning("Synchronisation...")

sync_terminal()
