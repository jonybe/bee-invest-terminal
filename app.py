import streamlit as st
import yfinance as yf
import feedparser
import math
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re

# 1. Configuration & Design System (V68 LOCKED)
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
    .intel-desk-sidebar { background: #080808; border-top: 1px dashed #333; padding: 12px 0; margin-top: 15px; }
    .cal-header { display: flex; justify-content: space-between; color: #444; font-size: 8px; font-weight: bold; margin-bottom: 5px; border-bottom: 1px solid #222; padding-bottom: 2px; }
    .cal-row { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid #111; font-size: 10px; }
    .cal-val { font-family: 'JetBrains Mono', monospace; font-weight: bold; width: 45px; text-align: right; }
    .impact-dot { height: 6px; width: 6px; border-radius: 50%; display: inline-block; margin-right: 6px; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=2)
def sync_terminal():
    try:
        t = yf.Ticker("GC=F")
        gold = t.fast_info['last_price']
        df_m15 = t.history(period="2d", interval="15m").dropna()
        m15_imp = ((gold - df_m15['Close'].iloc[-2]) / df_m15['Close'].iloc[-2]) * 100
        
        # Volume Profile
        vp_data = df_m15.tail(96)
        ph, pl = vp_data['High'].max(), vp_data['Low'].min()
        price_bins = pd.cut(vp_data['Close'], bins=25)
        bin_volumes = vp_data.groupby(price_bins, observed=True)['Volume'].sum()
        poc = bin_volumes.idxmax().mid
        std_dev = vp_data['Close'].std()
        vah, val = poc + (std_dev * 1.28), poc - (std_dev * 1.28)

        # Context Data
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        vix = yf.Ticker("^VIX").fast_info['last_price'] # AJOUT DU VIX
        
        feed = feedparser.parse("https://news.google.com/rss/search?q=XAU+Gold+Forex+PPI+CPI+PMI+FED&hl=en")
        news_list = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)[:4]
        
        # Calendar (Anti-bug PPI)
        cal_events = []
        for n in feed.entries[:20]:
            title = n.title.upper()
            if any(x in title for x in ["PPI", "CPI", "PMI", "FED", "NFP", "JOBS", "RATE"]):
                impact = "HIGH" if any(x in title for x in ["FED", "NFP", "CPI", "RATE"]) else "MED"
                nums = re.findall(r'\d+\.\d+', title)
                actual = nums[-1] + "%" if nums and float(nums[-1]) < 20 else "--"
                expect = nums[0] + "%" if len(nums) > 1 and float(nums[0]) < 20 else "--"
                event_name = next((x for x in ["PPI", "CPI", "PMI", "FED", "NFP", "RATE"] if x in title), "DATA")
                cal_events.append({"name": event_name, "impact": impact, "col": "#ff4b4b" if impact == "HIGH" else "#ffb000", "act": actual, "exp": expect})
        seen = set()
        unique_cal = [x for x in cal_events if not (x['name'] in seen or seen.add(x['name']))]

        # Sensors & Score
        h4_p = min(max(50 + ((gold - df_m15['Close'].mean())/2), 10), 90)
        drag = (dxy - 100) + (yields * 5) + (vix * 0.5)
        bull_score = min(max(55.0 - drag + (m15_imp * 35), 10), 100)
        status_text = "NEUTRAL" if 42 <= bull_score <= 58 else "BULLISH" if bull_score > 58 else "BEARISH"
        status_color = "#ffb000" if status_text == "NEUTRAL" else "#00ff88" if status_text == "BULLISH" else "#ff4b4b"

        # --- RENDER UI ---
        st.markdown(f"""<div style='display:flex; justify-content:space-between;'><div><h3 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST UNIT</h3><small style='color:#444;'>V68 VIX ENGINE | M15</small></div><div class='val-quant'>{gold:,.2f} $ <span class='status-tag' style='background:{status_color}22; color:{status_color}; border:1px solid {status_color};'>{status_text}</span></div></div>""", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

        c1, c2 = st.columns([2, 1])

        with c1:
            # Roadmap
            prog = (math.log(max(959, gold)/100) / math.log(1000000/100)) * 100
            st.markdown(f"<div class='roadmap-box'><div style='display:flex; justify-content:space-between; font-size:10px;'><span>PROG: {prog:.2f}%</span><span style='color:#ffb000;'>SOLDE: 959.56 £</span></div><div style='background:#222; height:6px; margin:5px 0;'><div style='background:#ffb000; height:100%; width:{prog}%;'></div></div></div>", unsafe_allow_html=True)
            st.markdown(f"""<div class="legende-centrale"><b style="color:#ffb000;">⚖️ PROTOCOLE :</b> 🟢 ACHAT > 58% | 🔴 VENTE < 42% | RISQUE 6%.</div>""", unsafe_allow_html=True)

            # Chart M15
            fig = go.Figure(data=[go.Candlestick(x=df_m15.index, open=df_m15['Open'], high=df_m15['High'], low=df_m15['Low'], close=df_m15['Close'])])
            fig.add_hline(y=poc, line_color="#ffb000", line_width=2.5)
            fig.add_hrect(y0=val, y1=vah, fillcolor="rgba(255, 255, 255, 0.05)", line_width=0)
            fig.update_layout(template="plotly_dark", paper_bgcolor="#050505", plot_bgcolor="#050505", height=320, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # Targets
            st.markdown("<p class='label'>● PARAMÈTRES & PROJECTION</p>", unsafe_allow_html=True)
            t_col1, t_col2 = st.columns(2)
            t_col1.markdown(f"<div class='kz-card' style='font-size:11px; border-left:3px solid #ffb000;'>🟢 <b>TP:</b> {gold+25:,.2f}<br>⚪ <b>IN:</b> {gold:,.2f}<br>🔴 <b>SL:</b> {gold-12:,.2f}</div>", unsafe_allow_html=True)
            t_col2.markdown(f"<div class='kz-card' style='font-size:11px; border-left:3px solid #00ff88;'>💰 <b>GAIN:</b> +115.15 £<br>⚠️ <b>RISQUE:</b> -57.57 £<br>📊 <b>LOT:</b> 0.24</div>", unsafe_allow_html=True)

            # Matrix Roadmap
            st.markdown("<p class='label'>● MATRIX ROADMAP : ÉVOLUTION DU CAPITAL RÉEL</p>", unsafe_allow_html=True)
            tr = 959.56
            for i in range(1, 6):
                ret = (tr * 0.1) if tr > 5000 else 0
                tr = (tr * 2) - ret
                badge = f"<div class='m-badge-blue'>SORTIE: {ret:,.0f}£</div>" if ret > 0 else f"<div class='m-badge-red'>ACCUMULATION</div>"
                st.markdown(f"""<div class="matrix-row"><div class="m-id">P{i:02}</div><div style="width:180px;"><div style="color:white; font-weight:bold; font-size:13px;">{tr:,.0f} £</div></div><div style="color:#00ff88; font-weight:bold; width:80px;">LOT: {(tr*0.06)/150:.2f}</div>{badge}</div>""", unsafe_allow_html=True)

        with c2:
            # Dominance
            st.markdown("<p class='label'>● BULL VS BEAR DOMINANCE</p>", unsafe_allow_html=True)
            st.markdown(f"""<div class='kz-card'><div style='display:flex; justify-content:space-between;'><small>IMPULSE M15</small><small style='color:{status_color}; font-weight:bold;'>{m15_imp:+.3f}%</small></div><div class='bar-container'><div class='p-bull' style='width:{bull_score}%'></div></div></div>""", unsafe_allow_html=True)
            
            # Sensors
            st.markdown("<p class='label'>● PRESSURE SENSORS</p>", unsafe_allow_html=True)
            for ut, pr in [("H4 TREND", h4_p), ("H2 FLOW", h4_p-5), ("M15 MOMENTUM", h4_p+(m15_imp*35))]:
                st.markdown(f"<div style='display:flex; justify-content:space-between;'><small>{ut}</small><small>{pr:.1f}%</small></div><div class='bar-container'><div class='p-bull' style='width:{pr}%'></div></div>", unsafe_allow_html=True)
            
            # Macro Metrics (VIX INCLUS)
            st.metric("DXY INDEX", f"{dxy:.2f}")
            st.metric("REAL YIELDS", f"{yields:.2f}%")
            st.metric("VIX INDEX", f"{vix:.2f}") # AFFICHAGE VIX
            
            # Calendrier
            st.markdown("<p class='label'>● ECONOMIC CALENDAR (LIVE)</p>", unsafe_allow_html=True)
            st.markdown("<div class='kz-card' style='padding:8px;'><div class='cal-header'><span>EVENT</span><span>ACT</span><span>EXP</span></div>", unsafe_allow_html=True)
            for ev in unique_cal[:4]:
                st.markdown(f"<div class='cal-row'><span><span class='impact-dot' style='background:{ev['col']};'></span>{ev['name']}</span><span class='cal-val' style='color:#00ff88;'>{ev['act']}</span><span class='cal-val' style='color:#555;'>{ev['exp']}</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # News Stream
            st.markdown("<p class='label'>● NEWS STREAM</p>", unsafe_allow_html=True)
            for n in news_list[:3]:
                st.markdown(f"<div style='font-size:10px; border-bottom:1px solid #111; padding:4px 0;'>🕒 {n.published[5:11]} | {n.title[:45]}...</div>", unsafe_allow_html=True)

        st.markdown(f"<div style='background:{status_color}; color:black; text-align:center; padding:10px; font-weight:900; border-radius:4px; margin-top:10px;'>VERDICT FINAL : {status_text}</div>", unsafe_allow_html=True)

    except:
        st.warning("Re-sync...")

sync_terminal()
