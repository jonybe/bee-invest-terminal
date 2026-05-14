import streamlit as st
import yfinance as yf
import feedparser
import math
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re

# 1. Configuration & Design System (V64 LOCKED)
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
    .status-tag { padding: 2px 6px; border-radius: 3px; font-size: 9px; font-weight: bold; margin-left: 10px; }
    .intel-desk-sidebar { background: #080808; border-top: 1px dashed #333; padding: 12px 0; margin-top: 15px; }
    
    /* CALENDAR STYLING */
    .cal-header { display: flex; justify-content: space-between; color: #444; font-size: 8px; font-weight: bold; margin-bottom: 5px; border-bottom: 1px solid #222; padding-bottom: 2px; }
    .cal-row { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid #111; font-size: 10px; }
    .cal-val { font-family: 'JetBrains Mono', monospace; font-weight: bold; width: 45px; text-align: right; }
    .impact-dot { height: 6px; width: 6px; border-radius: 50%; display: inline-block; margin-right: 6px; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=10)
def sync_terminal():
    try:
        t = yf.Ticker("GC=F")
        gold = t.fast_info['last_price']
        df_m15 = t.history(period="2d", interval="15m").dropna()
        m15_imp = ((df_m15['Close'].iloc[-1] - df_m15['Close'].iloc[-3]) / df_m15['Close'].iloc[-3]) * 100
        
        # Volume Profile
        vp_data = df_m15.tail(96)
        ph, pl = vp_data['High'].max(), vp_data['Low'].min()
        price_bins = pd.cut(vp_data['Close'], bins=25)
        bin_volumes = vp_data.groupby(price_bins, observed=True)['Volume'].sum()
        poc = bin_volumes.idxmax().mid
        std_dev = vp_data['Close'].std()
        vah, val = poc + (std_dev * 1.28), poc - (std_dev * 1.28)

        # Market Context
        hist = t.history(period="5d")
        vol_atr = (hist['High'] - hist['Low']).mean()
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        
        # Calendar & News Feed
        feed = feedparser.parse("https://news.google.com/rss/search?q=XAU+Gold+Forex+PPI+CPI+PMI+FED&hl=en")
        news_list = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)[:4]
        
        cal_events = []
        for n in feed.entries[:20]:
            title = n.title.upper()
            if any(x in title for x in ["PPI", "CPI", "PMI", "FED", "NFP", "JOBS", "RATE"]):
                impact_lvl = "HIGH" if any(x in title for x in ["FED", "NFP", "CPI", "RATE"]) else "MED"
                col = "#ff4b4b" if impact_lvl == "HIGH" else "#ffb000"
                nums = re.findall(r'[-+]?\d*\.\d+|\d+', title)
                actual = nums[-1] + "%" if nums else "--"
                expect = nums[0] + "%" if len(nums) > 1 else "--"
                event_name = next((x for x in ["PPI", "CPI", "PMI", "FED", "NFP", "RATE"] if x in title), "DATA")
                cal_events.append({"name": event_name, "impact": impact_lvl, "col": col, "act": actual, "exp": expect})
        
        seen = set()
        unique_cal = [x for x in cal_events if not (x['name'] in seen or seen.add(x['name']))]

        h4_p = min(max(50 + ((df_m15['Close'].iloc[-1] - df_m15['Close'].mean())/2), 10), 90)
        cap, risk_pct = 959.56, 0.06
        sl_dyn = max(vol_atr * 0.5, 15.0)
        perte_gbp = cap * risk_pct
        lot = perte_gbp / (sl_dyn * 10)
        drag = (dxy - 100) + (yields * 5)
        bull_score = min(max((28.0 + 18.0 + 9.0) - drag + (m15_imp * 25), 10), 100)
        status_text = "NEUTRAL" if 42 <= bull_score <= 58 else "BULLISH" if bull_score > 58 else "BEARISH"
        status_color = "#ffb000" if status_text == "NEUTRAL" else "#00ff88" if status_text == "BULLISH" else "#ff4b4b"

        # --- RENDER UI ---
        st.markdown(f"""<div style='display:flex; justify-content:space-between;'><div><h3 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST UNIT</h3><small style='color:#444;'>V64 TOTAL Cockpit | M15 Chart</small></div><div class='val-quant'>{gold:,.2f} $ <span class='status-tag' style='background:{status_color}22; color:{status_color}; border:1px solid {status_color};'>{status_text}</span></div></div>""", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

        col_main, col_side = st.columns([2, 1])

        with col_main:
            # Roadmap
            prog = (math.log(cap/100) / math.log(1000000/100)) * 100
            st.markdown(f"<div class='roadmap-box'><div style='display:flex; justify-content:space-between; font-size:10px;'><span>PROG: {prog:.2f}%</span><span style='color:#ffb000;'>SOLDE: {cap} £</span></div><div style='background:#222; height:6px; margin:5px 0;'><div style='background:#ffb000; height:100%; width:{prog}%;'></div></div></div>", unsafe_allow_html=True)
            st.markdown(f"""<div class="legende-centrale"><b style="color:#ffb000;">⚖️ PROTOCOLE :</b> 🟢 ACHAT > 58% | 🔴 VENTE < 42% | RISQUE 6%.</div>""", unsafe_allow_html=True)

            # Chart M15
            fig = go.Figure(data=[go.Candlestick(x=df_m15.index, open=df_m15['Open'], high=df_m15['High'], low=df_m15['Low'], close=df_m15['Close'], name="M15")])
            fig.add_hline(y=poc, line_color="#ffb000", line_width=2.5)
            fig.add_hrect(y0=val, y1=vah, fillcolor="rgba(255, 255, 255, 0.05)", line_width=0)
            fig.update_layout(template="plotly_dark", paper_bgcolor="#050505", plot_bgcolor="#050505", height=320, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # Targets & Projection
            st.markdown("<p class='label'>● PARAMÈTRES D'EXÉCUTION & PROJECTION FINANCIÈRE</p>", unsafe_allow_html=True)
            c_t1, c_t2 = st.columns(2)
            c_t1.markdown(f"<div class='kz-card' style='font-size:11px; border-left:3px solid #ffb000;'>🟢 <b>TP:</b> {gold + (sl_dyn * 2):,.2f} $<br>⚪ <b>IN:</b> {gold:,.2f} $<br>🔴 <b>SL:</b> {gold - sl_dyn:,.2f} $</div>", unsafe_allow_html=True)
            c_t2.markdown(f"<div class='kz-card' style='font-size:11px; border-left:3px solid #00ff88;'>💰 <b>GAIN:</b> +{perte_gbp * 2:.2f} £<br>⚠️ <b>RISQUE:</b> -{perte_gbp:.2f} £<br>📊 <b>LOT:</b> {lot:.2f}</div>", unsafe_allow_html=True)

            # Matrix Roadmap
            st.markdown("<p class='label'>● MATRIX ROADMAP : ÉVOLUTION DU CAPITAL RÉEL</p>", unsafe_allow_html=True)
            tr = cap
            for i in range(1, 6):
                ret = (tr * 0.1) if tr > 5000 else 0
                tr = (tr * 2) - ret
                badge = f"<div class='m-badge-blue'>SORTIE</div>" if ret > 0 else f"<div class='m-badge-red'>ACCUMULATION</div>"
                st.markdown(f"""<div class="matrix-row"><div class="m-id">P{i:02}</div><div style="color:white; font-weight:bold; font-size:13px;">{tr:,.0f} £</div><div style="color:#00ff88; font-weight:bold; width:80px;">LOT: {(tr*0.06)/(sl_dyn*10):.2f}</div>{badge}</div>""", unsafe_allow_html=True)

        with col_side:
            # Dominance & Macro
            st.markdown("<p class='label'>● BULL VS BEAR DOMINANCE</p>", unsafe_allow_html=True)
            st.markdown(f"""<div class='kz-card'><small>IMPULSE M15</small><div class='bar-container'><div class='p-bull' style='width:{bull_score}%'></div></div></div>""", unsafe_allow_html=True)
            st.metric("DXY INDEX", f"{dxy:.2f}")
            st.metric("REAL YIELDS", f"{yields:.2f}%")
            
            # Strategic Intel
            st.markdown(f"""<div class="intel-desk-sidebar"><p class='label' style='color:#ffb000; margin-bottom:10px;'>⚔️ STRATEGIC INTEL</p><div style="font-size:10px; color:#aaa;"><b>M15 ENGINE :</b> Réactivité x25.<br><b>STATUS :</b> {status_text}</div></div>""", unsafe_allow_html=True)

            # Calendrier Économique
            st.markdown("<p class='label'>● ECONOMIC CALENDAR (LIVE)</p>", unsafe_allow_html=True)
            st.markdown("<div class='kz-card' style='padding: 8px;'><div class='cal-header'><span style='width: 80px;'>EVENT</span><span style='width: 45px; text-align: right;'>ACT</span><span style='width: 45px; text-align: right;'>EXP</span></div>", unsafe_allow_html=True)
            if unique_cal:
                for ev in unique_cal[:4]:
                    st.markdown(f"<div class='cal-row'><span style='width: 80px;'><span class='impact-dot' style='background:{ev['col']};'></span>{ev['name']}</span><span class='cal-val' style='color:#00ff88;'>{ev['act']}</span><span class='cal-val' style='color:#555;'>{ev['exp']}</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # News Stream (Rétabli)
            st.markdown("<p class='label'>● NEWS STREAM (RSS)</p>", unsafe_allow_html=True)
            for n in news_list[:3]:
                st.markdown(f"<div style='font-size:10px; border-bottom:1px solid #111; padding:4px 0;'>🕒 {n.published[5:11]} | {n.title[:45]}...</div>", unsafe_allow_html=True)

        st.markdown(f"<div style='background:{status_color}; color:black; text-align:center; padding:10px; font-weight:900; border-radius:4px; margin-top:10px;'>VERDICT FINAL : {status_text}</div>", unsafe_allow_html=True)

    except Exception:
        st.warning("Récupération des flux...")

sync_terminal()
