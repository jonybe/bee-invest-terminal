import streamlit as st
import yfinance as yf
import feedparser
import math
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re

# 1. Configuration & Design System (V90 FULL RESTORE)
st.set_page_config(page_title="BEE-INVEST | TOTAL CONTROL", layout="wide")

if 'trades' not in st.session_state:
    st.session_state.trades = []
if 'last_m5_ts' not in st.session_state:
    st.session_state.last_m5_ts = None

st.markdown("""
<style>
    /* ANTI-FLICKER & STABILITY */
    div[data-testid="stAppViewBlockContainer"], div[data-testid="stVerticalBlock"], div[data-fragment-component-id] {
        opacity: 1 !important; transition: none !important; filter: none !important;
    }
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #e0e0e0; font-family: 'Inter', sans-serif; font-size: 11.5px; }
    .block-container { padding-top: 3.5rem !important; padding-bottom: 0rem !important; }
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; padding: 12px; border-radius: 4px; margin-bottom: 8px; }
    
    /* DOMINANCE MODULE CSS */
    .dom-container { background: #080808; border: 1px solid #151515; border-radius: 6px; padding: 20px; margin-bottom: 15px; }
    .dom-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
    .dom-title { color: #e0e0e0; font-size: 11px; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; }
    .flow-row { margin-bottom: 22px; position: relative; }
    .flow-label { color: #444; font-size: 8px; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
    .flow-meta { display: flex; justify-content: space-between; font-family: 'JetBrains Mono'; font-size: 16px; font-weight: bold; margin-bottom: 2px; }
    .flow-bar-bg { height: 12px; background: #ff4b4b; border-radius: 2px; overflow: hidden; display: flex; position: relative; }
    .flow-bar-fill { height: 100%; background: #00ff88; transition: 0.5s; }
    .leaning-badge { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); z-index: 10; 
                     background: rgba(10,10,10,0.9); border: 1px solid #222; padding: 3px 12px; border-radius: 4px; text-align: center; min-width: 120px; }
    .leaning-text { font-size: 8px; font-weight: 900; text-transform: uppercase; }
    .force-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 25px; }
    .force-card { background: #0a0a0a; border: 1px solid #151515; padding: 12px; border-radius: 4px; }
    .force-val { font-family: 'JetBrains Mono'; font-size: 20px; font-weight: bold; }

    /* LAYOUT COMPONENTS */
    .label { color: #555; font-size: 9px; text-transform: uppercase; font-weight: bold; letter-spacing: 1.2px; }
    .val-quant { font-family: 'JetBrains Mono', monospace; font-size: 18px; font-weight: bold; color: #00ff88; }
    .matrix-row { display: flex; justify-content: space-between; align-items: center; background: rgba(15, 15, 15, 0.8); border: 1px solid #1a1a1a; margin-bottom: 5px; padding: 12px 18px; border-radius: 4px; }
    .m-id { color: #ffb000; font-family: 'JetBrains Mono'; font-weight: 900; width: 45px; font-size: 14px; }
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
        
        # 2. CALCS & MACRO
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        vix = yf.Ticker("^VIX").fast_info['last_price']
        feed = feedparser.parse("https://news.google.com/rss/search?q=Gold+Economic+Calendar+Weekly+FED&hl=en")
        text_f = " ".join([n.title.lower() for n in feed.entries])
        
        geo, cb, etf = (32.5, 21.4, 11.2) if any(x in text_f for x in ["war", "conflict", "tension"]) else (28.0, 18.0, 9.5)
        fund_sent = ((geo + cb + etf) / 65.1) * 100
        drag = (dxy - 100) + (yields * 5) + (vix * 0.5)
        bull_score = min(max((geo + cb + etf) - drag + (m15_imp * 35), 10), 100)
        sig_label = "ACHAT" if bull_score > 58 else "VENTE" if bull_score < 42 else "ATTENTE"
        sig_col = "#00ff88" if sig_label == "ACHAT" else "#ff4b4b" if sig_label == "VENTE" else "#ffb000"
        regime = "RANGE" if 45 < bull_score < 55 and vix < 20 else "TRENDING" if bull_score >= 58 or bull_score <= 42 else "VOL EXPANSION"

        # DOMINANCE VALUES
        h4_s, h2_s = 55.0, 50.9
        m15_s = min(max(50 + (m15_imp * 400), 0), 100)
        
        # 3. TRADES MANAGEMENT (M5)
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
                if sig_label == "ACHAT" and bull_score > 58:
                    st.session_state.trades.append({'type': "LONG", 'in': gold, 'tp': gold+24, 'sl': gold-12, 'ts': curr_m5})
                elif sig_label == "VENTE" and bull_score < 42:
                    st.session_state.trades.append({'type': "SHORT", 'in': gold, 'tp': gold-24, 'sl': gold+12, 'ts': curr_m5})
            st.session_state.last_m5_ts = curr_m5

        # 4. CALENDAR DATA
        cal_data = []
        kw = ["PPI", "CPI", "PMI", "FED", "NFP", "JOBS"]
        for n in feed.entries[:20]:
            title = n.title.upper()
            if any(k in title for k in kw):
                ev_name = next((k for k in kw if k in title), "DATA")
                if not any(d['name'] == ev_name for d in cal_data):
                    nums = re.findall(r'\d+\.\d+', title)
                    cal_data.append({"name": ev_name, "act": nums[-1]+"%" if nums else "TBD", "exp": nums[0]+"%" if len(nums)>1 else "--", "col": "#ff4b4b" if "FED" in ev_name or "CPI" in ev_name else "#ffb000"})

        # --- RENDER ---
        st.markdown(f"""<div style='display:flex; justify-content:space-between;'><div><h3 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST UNIT</h3><small style='color:#444;'>V90 TOTAL RESTORE | M5 TRIGGER | SOLDE: 953.55 GBP</small></div><div class='val-quant'>{gold:,.2f} $ <span style='padding: 2px 6px; border-radius: 3px; font-size: 9px; font-weight: bold; margin-left: 10px; background:{sig_col}22; color:{sig_col}; border:1px solid {sig_col};'>{sig_label}</span></div></div>""", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

        c1, c2 = st.columns([2, 1])
        with c1:
            cap = 953.55
            prog = (math.log(cap/100) / math.log(1000000/100)) * 100
            st.markdown(f"<div class='roadmap-box'><div style='display:flex; justify-content:space-between; font-size:10px;'><span>PROG: {prog:.2f}%</span><span style='color:#ffb000;'>SOLDE: {cap} £</span></div><div style='background:#222; height:6px; margin:5px 0;'><div style='background:#ffb000; height:100%; width:{prog}%;'></div></div></div>", unsafe_allow_html=True)
            st.markdown(f"""<div style="font-size: 11px; color: #888; padding: 12px; background: #0a0a0a; border-radius: 4px; border-left: 4px solid #ffb000; margin: 15px 0;"><b style="color:#ffb000;">⚖️ PROTOCOLE :</b> 🟢 ACHAT > 58% | 🔴 VENTE < 42% | RISQUE 6%.</div>""", unsafe_allow_html=True)

            # --- MODULE DOMINANCE ---
            st.markdown(f"""
            <div class="dom-container">
                <div class="dom-header"><div class="dom-title">● BULL VS BEAR · DOMINANCE</div><div style="color:#333; font-size:8px;">MACRO = BIAS | INTRADAY = TIMING</div></div>
                <div class="flow-row">
                    <div class="flow-label">INTRADAY FLOW (4H)</div>
                    <div class="flow-meta"><span style="color:#00ff88;">{h4_s}%</span><span style="color:#ff4b4b;">{100-h4_s}%</span></div>
                    <div class="flow-bar-bg"><div class="flow-bar-fill" style="width:{h4_s}%;"></div>
                        <div class="leaning-badge"><div class="leaning-text" style="color:#00ff88;">LEANING BULLISH</div></div>
                    </div>
                </div>
                <div class="flow-row">
                    <div class="flow-label">INTRADAY FLOW (2H)</div>
                    <div class="flow-meta"><span style="color:#00ff88;">{h2_s}%</span><span style="color:#ff4b4b;">{100-h2_s}%</span></div>
                    <div class="flow-bar-bg"><div class="flow-bar-fill" style="width:{h2_s}%;"></div>
                        <div class="leaning-badge"><div class="leaning-text" style="color:#00ff88;">LEANING BULLISH</div></div>
                    </div>
                </div>
                <div class="flow-row">
                    <div class="flow-label">FAST INTRADAY FLOW (15M/1H)</div>
                    <div class="flow-meta"><span style="color:#00ff88;">{m15_s:.1f}%</span><span style="color:#ff4b4b;">{100-m15_s:.1f}%</span></div>
                    <div class="flow-bar-bg"><div class="flow-bar-fill" style="width:{m15_s}%;"></div>
                        <div class="leaning-badge"><div class="leaning-text" style="color:{'#00ff88' if m15_s > 50 else '#ff4b4b'};">LEANING {'BULLISH' if m15_s > 50 else 'BEARISH'}</div></div>
                    </div>
                </div>
                <div class="force-grid">
                    <div class="force-card" style="border-top: 2px solid #00ff88;"><div class="force-title" style="color:#00ff88;">SUPPORTING</div><div class="force-val" style="color:#00ff88;">+{max(0, m15_imp*10):.2f}</div></div>
                    <div class="force-card" style="border-top: 2px solid #ff4b4b;"><div class="force-title" style="color:#ff4b4b;">OPPOSING</div><div class="force-val" style="color:#ff4b4b;">{min(0, m15_imp*10):.2f}</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # --- SETUP PROPOSITION (RESTORED) ---
            st.markdown("<p class='label'>● ACTIVE STRATEGIC SETUPS (M5 PERSISTENT)</p>", unsafe_allow_html=True)
            if st.session_state.trades:
                tc1, tc2 = st.columns(2)
                for idx, tr in enumerate(st.session_state.trades):
                    b_c = "#00ff88" if tr['type'] == "LONG" else "#ff4b4b"
                    with (tc1 if idx==0 else tc2):
                        st.markdown(f"""<div class='kz-card' style='border-left:3px solid {b_c};'><b style='color:{b_c};'>{tr['type']} ACTIVE</b><br><small>{tr['ts'].strftime('%H:%M')}</small><div style='font-family:JetBrains Mono; font-size:10px; margin-top:5px;'>⚪ IN: {tr['in']:,.2f}<br>🟢 TP: {tr['tp']:,.2f}<br>🔴 SL: {tr['sl']:,.2f}</div></div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='kz-card' style='text-align:center; color:#444; padding:20px;'>⌛ WAITING FOR M5 SIGNAL...</div>", unsafe_allow_html=True)

            # MATRIX
            st.markdown("<p class='label'>● MATRIX ROADMAP : RÉEL | BRUT</p>", unsafe_allow_html=True)
            tr_m, tr_g = cap, cap
            for i in range(1, 7):
                ret = (tr_m * 0.1) if tr_m > 5000 else 0
                tr_m, tr_g = (tr_m * 2) - ret, (tr_g * 2)
                st.markdown(f"""<div class="matrix-row"><div class="m-id">P{i:02}</div><div style="width:200px; color:white; font-weight:bold;">{tr_m:,.0f} £ <span style="color:#444; font-size:10px; font-weight:normal;">/ {tr_g:,.0f} £</span></div><div style="color:#00ff88; font-weight:bold;">LOT: {(tr_m*0.06)/120:.2f}</div>{f"<div class='m-badge-blue'>SORTIE: {ret:,.0f}£</div>" if ret > 0 else "<div class='m-badge-red'>ACCUMULATION</div>"}</div>""", unsafe_allow_html=True)

        with c2:
            # MARKET REGIME
            st.markdown(f"""
            <div class="regime-box">
                <div class="regime-header"><div style="color:#e0e0e0; font-size:10px; font-weight:bold;">MARKET REGIME</div></div>
                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:8px;">
                    <div class="regime-card {'active' if regime == 'RANGE' else ''}">⟷<br><span>Range</span></div>
                    <div class="regime-card {'active' if regime == 'TRENDING' else ''}">↗<br><span>Trending</span></div>
                    <div class="regime-card {'active' if regime == 'VOL' else ''}">~<br><span>Vol</span></div>
                </div>
                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; margin-top:15px; border-top:1px dashed #222; padding-top:10px;">
                    <div><small style="color:#444;">YIELD</small><br><b>{yields:.2f}%</b></div>
                    <div><small style="color:#444;">VIX</small><br><b>{vix:.1f}</b></div>
                    <div><small style="color:#444;">USD</small><br><b>{dxy:.1f}</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # SENSORS
            st.markdown(f"<div style='display:flex; justify-content:space-between; font-weight:bold;'><span style='color:#555;'>BULL SCORE</span><span style='color:{sig_col};'>{sig_label} {bull_score:.1f}%</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='bar-container'><div class='p-bull' style='width:{bull_score}%; background:{sig_col};'></div></div>", unsafe_allow_html=True)
            for ut, pr in [("H4 TREND", h4_s), ("H2 FLOW", h2_s), ("M15 MOMENTUM", m15_s)]:
                st.markdown(f"<div style='display:flex; justify-content:space-between;'><small>{ut}</small><small style='color:#00ff88;'>{pr:.1f}%</small></div><div class='bar-container'><div class='p-bull' style='width:{pr}%'></div></div>", unsafe_allow_html=True)
            
            # CALENDAR (RESTORED)
            st.markdown("<p class='label'>● WEEKLY ECONOMIC CALENDAR</p>", unsafe_allow_html=True)
            st.markdown("<div class='kz-card' style='padding:8px;'><div class='cal-header'><span>EVENT</span><span style='margin-left:auto;'>ACT / EXP</span></div>" + 
                "".join([f"<div class='cal-row'><span>● {ev['name']}</span><span style='margin-left:auto; color:#00ff88;'>{ev['act']}</span></div>" for ev in cal_data[:4]]) + "</div>", unsafe_allow_html=True)
            
            # NEWS (RESTORED)
            st.markdown("<p class='label'>● LIVE NEWS FEED</p>", unsafe_allow_html=True)
            for n in feed.entries[:3]:
                st.markdown(f"<div style='font-size:9px; border-bottom:1px solid #111; padding:4px 0;'>🕒 {n.published[17:22]} | {n.title[:45]}...</div>", unsafe_allow_html=True)

        st.markdown(f"<div style='background:{sig_col}; color:black; text-align:center; padding:10px; font-weight:900; border-radius:4px; margin-top:10px;'>VERDICT FINAL : {sig_label} | {bull_score:.1f}%</div>", unsafe_allow_html=True)

    except Exception: st.warning("Re-sync stable...")

sync_terminal()
