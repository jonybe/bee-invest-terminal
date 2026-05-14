import streamlit as st
import yfinance as yf
import feedparser
import math
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re

# 1. Configuration & Design System (V87 OMEGA STABLE)
st.set_page_config(page_title="BEE-INVEST | TOTAL CONTROL", layout="wide")

if 'trades' not in st.session_state:
    st.session_state.trades = []
if 'last_m5_ts' not in st.session_state:
    st.session_state.last_m5_ts = None

st.markdown("""
<style>
    /* ANTI-FLICKER OMEGA */
    div[data-testid="stAppViewBlockContainer"], div[data-testid="stVerticalBlock"], div[data-fragment-component-id] {
        opacity: 1 !important; transition: none !important; filter: none !important;
    }
    
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #e0e0e0; font-family: 'Inter', sans-serif; font-size: 11.5px; }
    .block-container { padding-top: 3.5rem !important; padding-bottom: 0rem !important; }
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; padding: 12px; border-radius: 4px; margin-bottom: 8px; }
    .label { color: #555; font-size: 9px; text-transform: uppercase; font-weight: bold; letter-spacing: 1.2px; }
    .val-quant { font-family: 'JetBrains Mono', monospace; font-size: 18px; font-weight: bold; color: #00ff88; }
    
    /* MARKET REGIME DESIGN SYSTEM (IMAGE CLONE) */
    .regime-box { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 8px; padding: 15px; margin-bottom: 10px; }
    .regime-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid #1a1a1a; padding-bottom: 8px; }
    .regime-title { color: #e0e0e0; font-size: 10px; font-weight: bold; letter-spacing: 1.5px; display: flex; align-items: center; }
    .dot { height: 4px; width: 4px; background: #ffb000; border-radius: 50%; margin-right: 8px; }
    
    .regime-cards-container { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-bottom: 15px; }
    .regime-card { background: #111; border: 1px solid #1a1a1a; border-radius: 6px; padding: 12px 5px; text-align: center; color: #444; transition: 0.3s; }
    .regime-card.active { border: 1px solid #ffb000; color: #e0e0e0; background: rgba(255, 176, 0, 0.05); box-shadow: inset 0 0 10px rgba(255,176,0,0.05); }
    .regime-card i { display: block; font-size: 14px; margin-bottom: 8px; }
    .regime-card span { font-size: 8.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; }
    
    .strategy-alert { border: 1px solid #ffb000; border-left: 3px solid #ffb000; padding: 12px; border-radius: 4px; background: rgba(255, 176, 0, 0.02); color: #e0e0e0; font-size: 11px; margin-bottom: 15px; }
    
    .regime-metrics { display: grid; grid-template-columns: 1fr 1fr 1fr; border-top: 1px dashed #1a1a1a; padding-top: 12px; }
    .rm-item { text-align: left; }
    .rm-label { color: #444; font-size: 8px; font-weight: bold; text-transform: uppercase; }
    .rm-val { color: #e0e0e0; font-family: 'JetBrains Mono'; font-size: 14px; font-weight: bold; margin: 2px 0; }
    .rm-sub { color: #333; font-size: 8.5px; font-style: italic; }

    .matrix-row { display: flex; justify-content: space-between; align-items: center; background: rgba(15, 15, 15, 0.8); border: 1px solid #1a1a1a; margin-bottom: 5px; padding: 12px 18px; border-radius: 4px; }
    .m-id { color: #ffb000; font-family: 'JetBrains Mono'; font-weight: 900; width: 45px; font-size: 14px; }
    .m-badge-blue { padding: 4px 10px; border-radius: 12px; font-size: 8.5px; font-weight: bold; text-transform: uppercase; background: rgba(88, 166, 255, 0.1); color: #58a6ff; border: 1px solid #58a6ff33; width: 110px; text-align: center; }
    .m-badge-red { padding: 4px 10px; border-radius: 12px; font-size: 8.5px; font-weight: bold; text-transform: uppercase; background: rgba(255, 75, 75, 0.1); color: #ff4b4b; border: 1px solid rgba(255, 75, 75, 0.2); width: 110px; text-align: center; }
    .bar-container { background: #1a1a1a; height: 6px; border-radius: 3px; margin: 4px 0 10px 0; overflow: hidden; display: flex; }
    .p-bull { background: #00ff88; height: 100%; transition: 0.2s; } 
    .cal-header { display: flex; font-size: 8px; color: #444; border-bottom: 1px solid #222; padding-bottom: 4px; margin-bottom: 5px; font-weight: bold; }
    .cal-row { display: flex; font-size: 10px; padding: 6px 0; border-bottom: 1px solid #111; align-items: center; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=3)
def sync_terminal():
    try:
        # 1. FETCH
        t = yf.Ticker("GC=F")
        gold = t.fast_info['last_price']
        df_m15 = t.history(period="2d", interval="15m").dropna()
        df_m5 = t.history(period="1d", interval="5m").dropna()
        m15_imp = ((gold - df_m15['Close'].iloc[-2]) / df_m15['Close'].iloc[-2]) * 100
        
        # 2. VOLUME PROFILE
        vp_data = df_m15.tail(96).copy()
        p_min, p_max = vp_data['Low'].min(), vp_data['High'].max()
        bin_size = (p_max - p_min) / 20
        vp_data['bin'] = ((vp_data['Close'] - p_min) / bin_size).astype(int).clip(0, 19)
        v_profile = vp_data.groupby('bin', observed=True)['Volume'].sum()
        poc_p = p_min + (v_profile.idxmax() * bin_size) + (bin_size/2)
        vah, val = poc_p + (vp_data['Close'].std() * 1.1), poc_p - (vp_data['Close'].std() * 1.1)

        # 3. MACRO & SCORES
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        vix = yf.Ticker("^VIX").fast_info['last_price']
        feed = feedparser.parse("https://news.google.com/rss/search?q=Gold+Economic+Calendar+Weekly+PPI+CPI+FED&hl=en")
        text_f = " ".join([n.title.lower() for n in feed.entries])
        
        geo, cb, etf = (32.5, 21.4, 11.2) if any(x in text_f for x in ["war", "conflict", "tension"]) else (28.0, 18.0, 9.5)
        fund_sent = ((geo + cb + etf) / 65.1) * 100
        drag = (dxy - 100) + (yields * 5) + (vix * 0.5)
        bull_score = min(max((geo + cb + etf) - drag + (m15_imp * 35), 10), 100)
        sig_label = "ACHAT" if bull_score > 58 else "VENTE" if bull_score < 42 else "ATTENTE"
        sig_col = "#00ff88" if sig_label == "ACHAT" else "#ff4b4b" if sig_label == "VENTE" else "#ffb000"

        # REGIME LOGIC
        regime = "RANGE" if 45 < bull_score < 55 and vix < 20 else "TRENDING" if bull_score >= 58 or bull_score <= 42 else "VOL EXPANSION"
        strat_txt = "Neutral — Sideways / Wait for Liquidity"
        if sig_label == "ACHAT": strat_txt = "Strong — Lean Long / Increase Gold Exposure"
        elif sig_label == "VENTE": strat_txt = "Weak — Lean Short / Reduce Gold Exposure"

        # 4. CALENDAR
        cal_data = []
        kw = ["PPI", "CPI", "PMI", "FED", "NFP", "JOBS"]
        for n in feed.entries[:15]:
            title = n.title.upper()
            if any(k in title for k in kw):
                ev_name = next((k for k in kw if k in title), "DATA")
                if not any(d['name'] == ev_name for d in cal_data):
                    nums = re.findall(r'\d+\.\d+', title)
                    cal_data.append({"name": ev_name, "act": nums[-1]+"%" if nums else "TBD", "exp": nums[0]+"%" if len(nums)>1 else "--", "col": "#ff4b4b" if any(x in ev_name for x in ["FED","CPI"]) else "#ffb000"})

        # 5. TRADES
        active_trades = []
        for trade in st.session_state.trades:
            if trade['type'] == "LONG":
                if gold < trade['tp'] and gold > trade['sl']: active_trades.append(trade)
            else:
                if gold > trade['tp'] and gold < trade['sl']: active_trades.append(trade)
        st.session_state.trades = active_trades

        curr_m5 = df_m5.index[-1]
        if st.session_state.last_m5_ts != curr_m5:
            if len(st.session_state.trades) < 2:
                if sig_label == "ACHAT" and gold <= vah:
                    st.session_state.trades.append({'type': "LONG", 'in': gold, 'tp': gold+24, 'sl': gold-12, 'ts': curr_m5})
                elif sig_label == "VENTE" and gold >= val:
                    st.session_state.trades.append({'type': "SHORT", 'in': gold, 'tp': gold-24, 'sl': gold+12, 'ts': curr_m5})
            st.session_state.last_m5_ts = curr_m5

        # --- RENDER UI ---
        st.markdown(f"""<div style='display:flex; justify-content:space-between;'><div><h3 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST UNIT</h3><small style='color:#444;'>V87 REGIME MODULE | M5 ENGINE</small></div><div class='val-quant'>{gold:,.2f} $ <span style='padding: 2px 6px; border-radius: 3px; font-size: 9px; font-weight: bold; margin-left: 10px; background:{sig_col}22; color:{sig_col}; border:1px solid {sig_col};'>{sig_label}</span></div></div>""", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

        c1, c2 = st.columns([2, 1])
        with c1:
            cap = 960.23
            prog = (math.log(cap/100) / math.log(1000000/100)) * 100
            st.markdown(f"<div class='roadmap-box'><div style='display:flex; justify-content:space-between; font-size:10px;'><span>PROG: {prog:.2f}%</span><span style='color:#ffb000;'>SOLDE: {cap} £</span></div><div style='background:#222; height:6px; margin:5px 0;'><div style='background:#ffb000; height:100%; width:{prog}%;'></div></div></div>", unsafe_allow_html=True)
            st.markdown(f"""<div style="font-size: 11px; color: #888; line-height: 1.6; padding: 15px; background: #0a0a0a; border-radius: 4px; border-left: 4px solid #ffb000; margin: 15px 0;"><b style="color:#ffb000;">⚖️ PROTOCOLE :</b> 🟢 ACHAT > 58% | 🔴 VENTE < 42% | RISQUE 6%.</div>""", unsafe_allow_html=True)

            # CHART
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=df_m15.index, open=df_m15['Open'], high=df_m15['High'], low=df_m15['Low'], close=df_m15['Close'], name="M15"))
            max_v = v_profile.max()
            for b, v in v_profile.items():
                p_l = p_min + (b * (p_max - p_min) / 20)
                fig.add_shape(type="rect", xref="paper", yref="y", x0=0, x1=(v/max_v)*0.15, y0=p_l, y1=p_l+bin_size, fillcolor="rgba(150,150,150,0.1)", line_width=0)
            fig.add_hline(y=poc_p, line_color="#ffb000", line_width=1.5, opacity=0.8)
            fig.add_hrect(y0=val, y1=vah, fillcolor="rgba(255, 255, 255, 0.05)", line_width=0)
            fig.update_layout(template="plotly_dark", paper_bgcolor="#050505", plot_bgcolor="#050505", height=320, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # TRADES
            st.markdown("<p class='label'>● ACTIVE STRATEGIC SETUPS (M5 CLOSE)</p>", unsafe_allow_html=True)
            if st.session_state.trades:
                tc1, tc2 = st.columns(2)
                for idx, tr in enumerate(st.session_state.trades):
                    b_c = "#00ff88" if tr['type'] == "LONG" else "#ff4b4b"
                    with (tc1 if idx==0 else tc2):
                        st.markdown(f"""<div class='kz-card' style='border-left:3px solid {b_c};'><b style='color:{b_c};'>{tr['type']} ACTIVE</b><br><small>{tr['ts'].strftime('%H:%M')}</small><div style='font-family:JetBrains Mono; font-size:10px; margin-top:5px;'>⚪ IN: {tr['in']:,.2f}<br>🟢 TP: {tr['tp']:,.2f}<br>🔴 SL: {tr['sl']:,.2f}</div></div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='kz-card' style='text-align:center; color:#444; padding:20px;'>⌛ WAITING FOR M5 SIGNAL...</div>", unsafe_allow_html=True)

            st.markdown("<p class='label'>● MATRIX ROADMAP : RÉEL | BRUT</p>", unsafe_allow_html=True)
            tr_m, tr_g = cap, cap
            for i in range(1, 7):
                ret = (tr_m * 0.1) if tr_m > 5000 else 0
                tr_m, tr_g = (tr_m * 2) - ret, (tr_g * 2)
                st.markdown(f"""<div class="matrix-row"><div class="m-id">P{i:02}</div><div style="width:200px; color:white; font-weight:bold;">{tr_m:,.0f} £ <span style="color:#444; font-weight:normal; font-size:10px;">/ {tr_g:,.0f} £</span></div><div style="color:#00ff88; font-weight:bold;">LOT: {(tr_m*0.06)/120:.2f}</div>{f"<div class='m-badge-blue'>SORTIE: {ret:,.0f}£</div>" if ret > 0 else "<div class='m-badge-red'>ACCUMULATION</div>"}</div>""", unsafe_allow_html=True)

        with c2:
            # --- MARKET REGIME CLONE ---
            st.markdown(f"""
            <div class="regime-box">
                <div class="regime-header">
                    <div class="regime-title"><div class="dot"></div> MARKET REGIME</div>
                    <div style="color:#333; font-size:8px; font-weight:bold; letter-spacing:1px;">FROM LIVE SCORE REGIME</div>
                </div>
                <div class="regime-cards-container">
                    <div class="regime-card {'active' if regime == 'RANGE' else ''}">
                        <div style="font-size:14px; margin-bottom:5px;">⟷</div>
                        <span>Range</span>
                    </div>
                    <div class="regime-card {'active' if regime == 'TRENDING' else ''}">
                        <div style="font-size:14px; margin-bottom:5px;">↗</div>
                        <span>Trending</span>
                    </div>
                    <div class="regime-card {'active' if regime == 'VOL EXPANSION' else ''}">
                        <div style="font-size:14px; margin-bottom:5px;">~</div>
                        <span>Vol Expansion</span>
                    </div>
                </div>
                <div class="strategy-alert">
                    {strat_txt}
                </div>
                <div class="regime-metrics">
                    <div class="rm-item">
                        <div class="rm-label">Real Yield</div>
                        <div class="rm-val">{yields:.2f}%</div>
                        <div class="rm-sub">live macro feed</div>
                    </div>
                    <div class="rm-item">
                        <div class="rm-label">Vix</div>
                        <div class="rm-val">{vix:.1f}</div>
                        <div class="rm-sub">risk proxy</div>
                    </div>
                    <div class="rm-item">
                        <div class="rm-label">USD Broad</div>
                        <div class="rm-val">{dxy:.1f}</div>
                        <div class="rm-sub">dollar pressure</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"<div style='display:flex; justify-content:space-between; font-weight:bold; margin-top:10px;'><span style='color:#555;'>BULL SCORE</span><span style='color:{sig_col};'>{sig_label} {bull_score:.1f}%</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='bar-container'><div class='p-bull' style='width:{bull_score}%; background:{sig_col};'></div></div>", unsafe_allow_html=True)
            
            st.markdown("<p class='label'>● PRESSURE SENSORS (RAW)</p>", unsafe_allow_html=True)
            for ut, pr in [("H4 TREND", 55.0), ("H2 FLOW", 50.0), ("M15 MOMENTUM", bull_score)]:
                st.markdown(f"<div style='display:flex; justify-content:space-between;'><small>{ut}</small><small style='color:#00ff88; font-weight:bold;'>{pr:.1f}%</small></div><div class='bar-container'><div class='p-bull' style='width:{pr}%'></div></div>", unsafe_allow_html=True)
            
            st.markdown("<p class='label'>● FUNDAMENTAL SCORES</p>", unsafe_allow_html=True)
            st.markdown(f"""<div class='kz-card'><div style='display:grid; grid-template-columns:1fr 1fr 1fr; text-align:center;'><div><small>GEO</small><br><b>{geo}</b></div><div><small>FED</small><br><b>{cb}</b></div><div><small>ETF</small><br><b>{etf}</b></div></div><div style='display:flex; justify-content:space-between; margin-top:5px;'><small>SENTIMENT</small><small style='color:#00ff88;'>{fund_sent:.1f}%</small></div><div class='bar-container'><div class='p-bull' style='width:{fund_sent}%'></div></div></div>""", unsafe_allow_html=True)
            
            st.markdown("<p class='label'>● WEEKLY ECONOMIC CALENDAR</p>", unsafe_allow_html=True)
            st.markdown("<div class='kz-card' style='padding:8px;'><div class='cal-header'><span class='cal-col-ev'>EVENT (WEEK)</span><span style='margin-left:auto;'>ACT / EXP</span></div>" + 
                "".join([f"<div class='cal-row'><span>● {ev['name']}</span><span style='margin-left:auto; color:#00ff88;'>{ev['act']}</span></div>" for ev in cal_data[:3]]) + "</div>", unsafe_allow_html=True)

        st.markdown(f"<div style='background:{sig_col}; color:black; text-align:center; padding:10px; font-weight:900; border-radius:4px; margin-top:10px;'>VERDICT FINAL : {sig_label} | {bull_score:.1f}%</div>", unsafe_allow_html=True)

    except Exception: st.warning("Sync stabilisée...")

sync_terminal()
