import streamlit as st
import yfinance as yf
import feedparser
import math
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re

# 1. Configuration & Design System (V79 TOTAL RESTORE)
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
    .status-tag { padding: 2px 6px; border-radius: 3px; font-size: 9px; font-weight: bold; margin-left: 10px; }
    .macro-note { font-size: 9px; color: #666; margin-top: -8px; margin-bottom: 12px; font-style: italic; border-left: 2px solid #333; padding-left: 8px; }
    .cal-header { display: flex; font-size: 8px; color: #444; border-bottom: 1px solid #222; padding-bottom: 4px; margin-bottom: 5px; font-weight: bold; }
    .cal-col-ev { width: 50%; } .cal-col-val { width: 25%; text-align: right; }
    .cal-row { display: flex; font-size: 10px; padding: 6px 0; border-bottom: 1px solid #111; align-items: center; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=2)
def sync_terminal():
    try:
        # 1. FETCH & DATA PREP
        t = yf.Ticker("GC=F")
        gold = t.fast_info['last_price']
        df_m15 = t.history(period="2d", interval="15m").dropna()
        m15_imp = ((gold - df_m15['Close'].iloc[-2]) / df_m15['Close'].iloc[-2]) * 100
        
        # 2. VOLUME PROFILE (V77 FAST METHOD)
        vp_data = df_m15.tail(96).copy()
        p_min, p_max = vp_data['Low'].min(), vp_data['High'].max()
        bins, bin_size = 20, (p_max - p_min) / 20
        vp_data['bin'] = ((vp_data['Close'] - p_min) / bin_size).astype(int).clip(0, 19)
        v_profile = vp_data.groupby('bin', observed=True)['Volume'].sum()
        poc_p = p_min + (v_profile.idxmax() * bin_size) + (bin_size/2)
        vah, val = poc_p + (vp_data['Close'].std() * 1.1), poc_p - (vp_data['Close'].std() * 1.1)

        # 3. MACRO & NEWS
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        vix = yf.Ticker("^VIX").fast_info['last_price']
        feed = feedparser.parse("https://news.google.com/rss/search?q=XAU+Gold+PPI+CPI+FED&hl=en")
        text_f = " ".join([n.title.lower() for n in feed.entries])
        
        # 4. SCORES & SENTIMENT
        geo, cb, etf = (32.5, 21.4, 11.2) if any(x in text_f for x in ["war", "conflict", "tension"]) else (28.0, 18.0, 9.5)
        fund_sent = ((geo + cb + etf) / 65.1) * 100
        drag = (dxy - 100) + (yields * 5) + (vix * 0.5)
        bull_score = min(max((geo + cb + etf) - drag + (m15_imp * 35), 10), 100)
        
        # 5. SIGNAL LOGIC
        sig_label = "ACHAT" if bull_score > 58 else "VENTE" if bull_score < 42 else "ATTENTE"
        sig_col = "#00ff88" if sig_label == "ACHAT" else "#ff4b4b" if sig_label == "VENTE" else "#ffb000"
        
        # 6. CALENDAR PARSING
        cal_data = []
        for n in feed.entries[:15]:
            title = n.title.upper()
            if any(x in title for x in ["PPI", "CPI", "PMI", "FED", "NFP"]):
                ev_name = next((x for x in ["PPI", "CPI", "PMI", "FED", "NFP"] if x in title), "NEWS")
                if not any(d['name'] == ev_name for d in cal_data):
                    nums = re.findall(r'\d+\.\d+', title)
                    cal_data.append({"name": ev_name, "act": nums[-1]+"%" if nums else "--", "exp": nums[0]+"%" if len(nums)>1 else "--", "col": "#ff4b4b" if "FED" in ev_name or "CPI" in ev_name else "#ffb000"})

        # --- RENDER ---
        st.markdown(f"""<div style='display:flex; justify-content:space-between;'><div><h3 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST UNIT</h3><small style='color:#444;'>V79 OMEGA RESTORE | M15 ENGINE</small></div><div class='val-quant'>{gold:,.2f} $ <span class='status-tag' style='background:{sig_col}22; color:{sig_col}; border:1px solid {sig_col};'>{sig_label}</span></div></div>""", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

        c1, c2 = st.columns([2, 1])
        with c1:
            cap = 960.23
            prog = (math.log(cap/100) / math.log(1000000/100)) * 100
            st.markdown(f"<div class='roadmap-box'><div style='display:flex; justify-content:space-between; font-size:10px;'><span>PROG: {prog:.2f}%</span><span style='color:#ffb000;'>SOLDE: {cap} £</span></div><div style='background:#222; height:6px; margin:5px 0;'><div style='background:#ffb000; height:100%; width:{prog}%;'></div></div></div>", unsafe_allow_html=True)
            st.markdown(f"""<div class="legende-centrale"><b style="color:#ffb000;">⚖️ PROTOCOLE :</b> 🟢 ACHAT > 58% | 🔴 VENTE < 42% | RISQUE 6%.</div>""", unsafe_allow_html=True)

            # CHART (STABLE V77)
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=df_m15.index, open=df_m15['Open'], high=df_m15['High'], low=df_m15['Low'], close=df_m15['Close'], name="M15"))
            max_v = v_profile.max()
            for b, v in v_profile.items():
                p_lvl = p_min + (b * bin_size)
                w = (v / max_v) * 0.15
                fig.add_shape(type="rect", xref="paper", yref="y", x0=0, x1=w, y0=p_lvl, y1=p_lvl+bin_size, fillcolor="rgba(150,150,150,0.1)", line_width=0)
            fig.add_hline(y=poc_p, line_color="#ffb000", line_width=1.5, opacity=0.8)
            fig.add_hrect(y0=val, y1=vah, fillcolor="rgba(255, 255, 255, 0.05)", line_width=0)
            fig.update_layout(template="plotly_dark", paper_bgcolor="#050505", plot_bgcolor="#050505", height=320, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            st.markdown("<p class='label'>● STRATEGIC OPPORTUNITY FINDER</p>", unsafe_allow_html=True)
            opp = "LONG" if sig_label == "ACHAT" and gold <= vah else "SHORT" if sig_label == "VENTE" and gold >= val else None
            if opp:
                e, d = gold, 12.0
                tp, sl = (e+d*2 if opp=="LONG" else e-d*2), (e-d if opp=="LONG" else e+d)
                sc1, sc2 = st.columns(2)
                sc1.markdown(f"<div class='kz-card' style='border-left:3px solid #00ff88;'>🔥 <b>{opp} SETUP</b><br>⚪ IN: {e:,.2f}<br>🟢 TP: {tp:,.2f}<br>🔴 SL: {sl:,.2f}</div>", unsafe_allow_html=True)
                sc2.markdown(f"<div class='kz-card' style='border-left:3px solid #00ff88;'>📊 LOTS: {(cap*0.06)/(d*10):.2f}<br>💰 GAIN: +{(cap*0.06)*2:.2f} £</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='kz-card' style='text-align:center; color:#444; padding:20px;'>⌛ WAITING FOR SETUP...</div>", unsafe_allow_html=True)

            st.markdown("<p class='label'>● MATRIX ROADMAP</p>", unsafe_allow_html=True)
            tr_m = cap
            for i in range(1, 6):
                ret = (tr_m * 0.1) if tr_m > 5000 else 0
                tr_m = (tr_m * 2) - ret
                badge = f"<div class='m-badge-blue'>SORTIE: {ret:,.0f}£</div>" if ret > 0 else f"<div class='m-badge-red'>ACCUMULATION</div>"
                st.markdown(f"""<div class="matrix-row"><div class="m-id">P{i:02}</div><div style="width:150px; color:white; font-weight:bold; font-size:13px;">{tr_m:,.0f} £</div><div style="color:#00ff88; font-weight:bold;">LOT: {(tr_m*0.06)/120:.2f}</div>{badge}</div>""", unsafe_allow_html=True)

        with c2:
            st.markdown(f"<div style='display:flex; justify-content:space-between; font-weight:bold;'><span style='color:#555;'>BULL SCORE</span><span style='color:{sig_col};'>{sig_label} {bull_score:.1f}%</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='bar-container'><div class='p-bull' style='width:{bull_score}%; background:{sig_col};'></div></div>", unsafe_allow_html=True)
            
            st.markdown("<p class='label'>● PRESSURE SENSORS (RAW)</p>", unsafe_allow_html=True)
            for ut, pr in [("H4 TREND", 55.0), ("H2 FLOW", 50.0), ("M15 MOMENTUM", bull_score)]:
                st.markdown(f"<div style='display:flex; justify-content:space-between;'><small>{ut}</small><small style='color:#00ff88; font-weight:bold;'>{pr:.1f}%</small></div><div class='bar-container'><div class='p-bull' style='width:{pr}%'></div></div>", unsafe_allow_html=True)
            
            st.markdown("<p class='label'>● FUNDAMENTAL SCORES</p>", unsafe_allow_html=True)
            st.markdown(f"""<div class='kz-card'><div style='display:grid; grid-template-columns:1fr 1fr 1fr; text-align:center;'><div><small>GEO</small><br><b>{geo}</b></div><div><small>FED</small><br><b>{cb}</b></div><div><small>ETF</small><br><b>{etf}</b></div></div><div style='display:flex; justify-content:space-between; margin-top:5px;'><small>SENTIMENT</small><small style='color:#00ff88;'>{fund_sent:.1f}%</small></div><div class='bar-container'><div class='p-bull' style='width:{fund_sent}%'></div></div></div>""", unsafe_allow_html=True)

            st.metric("DXY INDEX", f"{dxy:.2f}")
            st.markdown("<div class='macro-note'>Vendre Gold si DXY > 102.50. Chute = Bullish.</div>", unsafe_allow_html=True)
            st.metric("REAL YIELDS", f"{yields:.2f}%")
            st.markdown("<div class='macro-note'>Bullish si Yields < 4.0%. Coût d'opp. bas.</div>", unsafe_allow_html=True)
            st.metric("VIX INDEX", f"{vix:.2f}")
            st.markdown("<div class='macro-note'>Safe Haven si VIX > 20. Panique = Achat.</div>", unsafe_allow_html=True)
            
            st.markdown("<p class='label'>● ECONOMIC CALENDAR (LIVE)</p>", unsafe_allow_html=True)
            st.markdown("<div class='kz-card' style='padding:8px;'><div class='cal-header'><span class='cal-col-ev'>EVENT</span><span class='cal-col-val'>ACT</span><span class='cal-col-val'>EXP</span></div>", unsafe_allow_html=True)
            for ev in (cal_data if cal_data else [{"name": "SCANNING", "act": "--", "exp": "--", "col": "#444"}]):
                st.markdown(f"<div class='cal-row'><span class='cal-col-ev'><span style='color:{ev['col']};'>●</span> {ev['name']}</span><span class='cal-col-val' style='color:#00ff88;'>{ev['act']}</span><span class='cal-col-val' style='color:#555;'>{ev['exp']}</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<p class='label'>● NEWS STREAM (RSS)</p>", unsafe_allow_html=True)
            for n in feed.entries[:3]:
                st.markdown(f"<div style='font-size:10px; border-bottom:1px solid #111; padding:4px 0;'>🕒 {n.published[5:11]} | {n.title[:45]}...</div>", unsafe_allow_html=True)

        st.markdown(f"<div style='background:{sig_col}; color:black; text-align:center; padding:10px; font-weight:900; border-radius:4px; margin-top:10px;'>VERDICT FINAL : {sig_label} | {bull_score:.1f}%</div>", unsafe_allow_html=True)

    except Exception: st.warning("Re-sync...")

sync_terminal()
