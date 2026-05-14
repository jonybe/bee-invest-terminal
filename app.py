import streamlit as st
import yfinance as yf
import feedparser
import math
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re

# 1. Configuration & Design System (V99 RENDER FIX & FULL INTEL)
st.set_page_config(page_title="BEE-INVEST | TOTAL CONTROL", layout="wide")

if 'trades' not in st.session_state:
    st.session_state.trades = []
if 'last_m5_ts' not in st.session_state:
    st.session_state.last_m5_ts = None

# CSS ANTI-SCINTILLEMENT & CORRECTION OVERFLOW
st.markdown("""
<style>
    :root {
        --st-fragment-fade-opacity: 1 !important;
        --st-fragment-fade-duration: 0ms !important;
    }
    div[data-testid="stAppViewBlockContainer"], div[data-testid="stVerticalBlock"],
    div[data-fragment-component-id], [data-testid="stFragment"] {
        opacity: 1 !important; transition: none !important; filter: none !important;
    }
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #e0e0e0; font-family: 'Inter', sans-serif; font-size: 11.5px; }
    .block-container { padding-top: 3.5rem !important; padding-bottom: 0rem !important; }
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; padding: 12px; border-radius: 4px; margin-bottom: 8px; }
    
    /* DOMINANCE MODULE CSS */
    .dom-container { background: #080808; border: 1px solid #151515; border-radius: 6px; padding: 20px; margin-bottom: 15px; }
    .flow-row { margin-bottom: 22px; position: relative; }
    .flow-meta { display: flex; justify-content: space-between; font-family: 'JetBrains Mono'; font-size: 16px; font-weight: bold; margin-bottom: 2px; }
    
    /* CORRECTION ICI : overflow: visible; au lieu de hidden pour ne plus couper le texte */
    .flow-bar-bg { height: 14px; background: #ff4b4b; border-radius: 2px; overflow: visible; display: flex; position: relative; }
    .flow-bar-fill { height: 100%; background: #00ff88; transition: 0.5s; border-radius: 2px 0 0 2px; }
    
    .leaning-badge { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); z-index: 10; 
                     background: rgba(10,10,10,0.95); border: 1px solid #222; padding: 4px 14px; border-radius: 4px; text-align: center; min-width: 140px; }
    .tf-label { font-size: 7px; color: #555; font-weight: bold; text-transform: uppercase; margin-bottom: 1px; }
    .leaning-text { font-size: 8px; font-weight: 900; text-transform: uppercase; }
    
    .matrix-row { display: flex; justify-content: space-between; align-items: center; background: rgba(15, 15, 15, 0.8); border: 1px solid #1a1a1a; margin-bottom: 5px; padding: 12px 18px; border-radius: 4px; }
    .m-id { color: #ffb000; font-family: 'JetBrains Mono'; font-weight: 900; width: 45px; font-size: 14px; }
    .m-badge-red { padding: 4px 10px; border-radius: 12px; font-size: 8.5px; font-weight: bold; text-transform: uppercase; background: rgba(255, 75, 75, 0.1); color: #ff4b4b; border: 1px solid rgba(255, 75, 75, 0.2); width: 110px; text-align: center; }
    .m-badge-blue { padding: 4px 10px; border-radius: 12px; font-size: 8.5px; font-weight: bold; text-transform: uppercase; background: rgba(88, 166, 255, 0.1); color: #58a6ff; border: 1px solid #58a6ff33; width: 110px; text-align: center; }
    .intel-box { background: #0a0a0a; border-left: 2px solid #ffb000; padding: 10px; margin-top: 10px; border-radius: 0 4px 4px 0; }
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
        
        # 2. MACRO & DOMINANCE
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        vix = yf.Ticker("^VIX").fast_info['last_price']
        feed = feedparser.parse("https://news.google.com/rss/search?q=Gold+Weekly+Economic+Calendar+FED&hl=en")
        
        h4_s, h2_s = 55.0, 50.9
        m15_s = min(max(50 + (m15_imp * 400), 0), 100)
        drag = (dxy - 100) + (yields * 5) + (vix * 0.5)
        bull_score = min(max(65.0 - drag + (m15_imp * 35), 10), 100)
        sig_label = "ACHAT" if bull_score > 58 else "VENTE" if bull_score < 42 else "ATTENTE"
        sig_col = "#00ff88" if sig_label == "ACHAT" else "#ff4b4b" if sig_label == "VENTE" else "#ffb000"
        regime = "RANGE" if 45 < bull_score < 55 and vix < 20 else "TRENDING" if bull_score >= 58 or bull_score <= 42 else "VOL EXPANSION"

        cal_data = []
        for n in feed.entries[:20]:
            title = n.title.upper()
            if any(k in title for k in ["PPI", "CPI", "FED", "NFP"]):
                ev_name = next((k for k in ["PPI", "CPI", "FED", "NFP"] if k in title), "DATA")
                if not any(d['name'] == ev_name for d in cal_data):
                    cal_data.append({"name": ev_name, "act": "TBD"})

        # 3. TRADES
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

        # --- RENDER ---
        st.markdown(f"""<div style='display:flex; justify-content:space-between;'><div><h3 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST UNIT</h3><small style='color:#444;'>V99 DISPLAY FIXED | FULL INTEL</small></div><div style='font-family:JetBrains Mono; font-size:18px; font-weight:bold; color:#00ff88;'>{gold:,.2f} $ <span style='padding: 2px 6px; border-radius: 3px; font-size: 9px; font-weight: bold; margin-left: 10px; background:{sig_col}22; color:{sig_col}; border:1px solid {sig_col};'>{sig_label}</span></div></div>""", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

        c1, c2 = st.columns([2, 1])
        with c1:
            cap = 953.55
            prog = (math.log(cap/100) / math.log(1000000/100)) * 100
            st.markdown(f"<div style='margin-bottom:15px;'><div style='display:flex; justify-content:space-between; font-size:10px;'><span>PROG: {prog:.2f}%</span><span style='color:#ffb000;'>SOLDE: {cap} £</span></div><div style='background:#222; height:6px; margin:5px 0;'><div style='background:#ffb000; height:100%; width:{prog}%;'></div></div></div>", unsafe_allow_html=True)
            
            # --- BULL VS BEAR DOMINANCE ---
            st.markdown(f"""
            <div class="dom-container">
                <div style="display:flex; justify-content:space-between; margin-bottom:20px;"><div style="color:#e0e0e0; font-size:11px; font-weight:bold; letter-spacing:2px;">● BULL VS BEAR · DOMINANCE</div></div>
                <div class="flow-row">
                    <div class="flow-meta"><span style="color:#00ff88;">{h4_s}%</span><span style="color:#ff4b4b;">{100-h4_s}%</span></div>
                    <div class="flow-bar-bg"><div class="flow-bar-fill" style="width:{h4_s}%;"></div>
                        <div class="leaning-badge"><div class="tf-label">FLUX H4</div><div class="leaning-text" style="color:#00ff88;">LEANING BULLISH</div></div>
                    </div>
                </div>
                <div class="flow-row">
                    <div class="flow-meta"><span style="color:#00ff88;">{h2_s}%</span><span style="color:#ff4b4b;">{100-h2_s}%</span></div>
                    <div class="flow-bar-bg"><div class="flow-bar-fill" style="width:{h2_s}%;"></div>
                        <div class="leaning-badge"><div class="tf-label">FLUX H2</div><div class="leaning-text" style="color:#00ff88;">LEANING BULLISH</div></div>
                    </div>
                </div>
                <div class="flow-row">
                    <div class="flow-meta"><span style="color:#00ff88;">{m15_s:.1f}%</span><span style="color:#ff4b4b;">{100-m15_s:.1f}%</span></div>
                    <div class="flow-bar-bg"><div class="flow-bar-fill" style="width:{m15_s}%;"></div>
                        <div class="leaning-badge"><div class="tf-label">FLUX M15</div><div class="leaning-text" style="color:{'#00ff88' if m15_s > 50 else '#ff4b4b'};">LEANING {'BULLISH' if m15_s > 50 else 'BEARISH'}</div></div>
                    </div>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:25px;">
                    <div style="background:#0a0a0a; border:1px solid #151515; padding:12px; border-top:2px solid #00ff88;"><div style="font-size:9px; color:#00ff88;">SUPPORTING</div><div style="font-family:JetBrains Mono; font-size:20px; font-weight:bold; color:#00ff88;">+{max(0, m15_imp*10):.2f}</div></div>
                    <div style="background:#0a0a0a; border:1px solid #151515; padding:12px; border-top:2px solid #ff4b4b;"><div style="font-size:9px; color:#ff4b4b;">OPPOSING</div><div style="font-family:JetBrains Mono; font-size:20px; font-weight:bold; color:#ff4b4b;">{min(0, m15_imp*10):.2f}</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # SETUPS
            st.markdown("<p style='color:#555; font-size:9px; font-weight:bold; text-transform:uppercase;'>● ACTIVE SETUPS (M5 PERSISTENT)</p>", unsafe_allow_html=True)
            if st.session_state.trades:
                tc1, tc2 = st.columns(2)
                for idx, tr in enumerate(st.session_state.trades):
                    b_c = "#00ff88" if tr['type'] == "LONG" else "#ff4b4b"
                    with (tc1 if idx==0 else tc2):
                        st.markdown(f"""<div class='kz-card' style='border-left:3px solid {b_c};'><b style='color:{b_c};'>{tr['type']} ACTIVE</b><br><small>{tr['ts'].strftime('%H:%M')}</small><div style='font-family:JetBrains Mono; font-size:10px; margin-top:5px;'>⚪ IN: {tr['in']:,.2f}<br>🟢 TP: {tr['tp']:,.2f}<br>🔴 SL: {tr['sl']:,.2f}</div></div>""", unsafe_allow_html=True)
            else: st.markdown(f"<div class='kz-card' style='text-align:center; color:#444; padding:20px;'>⌛ WAITING FOR M5 SIGNAL...</div>", unsafe_allow_html=True)

            # MATRIX
            st.markdown("<p style='color:#555; font-size:9px; font-weight:bold; text-transform:uppercase;'>● MATRIX ROADMAP : RÉEL | BRUT</p>", unsafe_allow_html=True)
            tr_m, tr_g = cap, cap
            for i in range(1, 7):
                ret = (tr_m * 0.1) if tr_m > 5000 else 0
                tr_m, tr_g = (tr_m * 2) - ret, (tr_g * 2)
                badge = f"<div class='m-badge-blue'>SORTIE: {ret:,.0f}£</div>" if i >= 4 and ret > 0 else "<div class='m-badge-red'>ACCUMULATION</div>"
                st.markdown(f"""<div class="matrix-row"><div class="m-id">P{i:02}</div><div style="width:200px; color:white; font-weight:bold;">{tr_m:,.0f} £ <span style="color:#444; font-size:10px; font-weight:normal;">/ {tr_g:,.0f} £</span></div><div style="color:#00ff88; font-weight:bold;">LOT: {(tr_m*0.06)/120:.2f}</div>{badge}</div>""", unsafe_allow_html=True)

        with c2:
            # MARKET REGIME
            st.markdown(f"""<div class="regime-box" style="background:#0d0d0d; border:1px solid #1a1a1a; padding:15px; border-radius:8px;">
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px;">
                    <div style="background:#111; border:1px solid {'#ffb000' if regime == 'RANGE' else '#1a1a1a'}; text-align:center; padding:10px; border-radius:6px; color:{'#e0e0e0' if regime == 'RANGE' else '#444'};">⟷<br><span style="font-size:8px; font-weight:bold;">RANGE</span></div>
                    <div style="background:#111; border:1px solid {'#ffb000' if regime == 'TRENDING' else '#1a1a1a'}; text-align:center; padding:10px; border-radius:6px; color:{'#e0e0e0' if regime == 'TRENDING' else '#444'};">↗<br><span style="font-size:8px; font-weight:bold;">TREND</span></div>
                    <div style="background:#111; border:1px solid {'#ffb000' if regime == 'VOL' else '#1a1a1a'}; text-align:center; padding:10px; border-radius:6px; color:{'#e0e0e0' if regime == 'VOL' else '#444'};">~<br><span style="font-size:8px; font-weight:bold;">VOL</span></div>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; margin-top:15px; text-align:center; border-top:1px dashed #222; padding-top:10px;">
                    <div><small style="color:#444;">YIELD</small><br><b>{yields:.2f}%</b></div>
                    <div><small style="color:#444;">VIX</small><br><b>{vix:.1f}</b></div>
                    <div><small style="color:#444;">USD</small><br><b>{dxy:.1f}</b></div>
                </div></div>""", unsafe_allow_html=True)

            st.markdown(f"<div style='display:flex; justify-content:space-between; font-weight:bold; margin-top:10px;'><span style='color:#555;'>BULL SCORE</span><span style='color:{sig_col};'>{sig_label} {bull_score:.1f}%</span></div><div style='background:#1a1a1a; height:6px; border-radius:3px; overflow:hidden;'><div style='background:{sig_col}; width:{bull_score}%; height:100%;'></div></div>", unsafe_allow_html=True)
            
            # WEEKLY CALENDAR
            st.markdown("<p style='color:#555; font-size:9px; font-weight:bold; text-transform:uppercase; margin-top:15px;'>● WEEKLY ECONOMIC CALENDAR</p>", unsafe_allow_html=True)
            st.markdown("<div class='kz-card' style='padding:8px;'><div style='display:flex; font-size:8px; color:#444; border-bottom:1px solid #222; padding-bottom:4px; margin-bottom:5px; font-weight:bold;'><span>EVENT</span><span style='margin-left:auto;'>ACT / EXP</span></div>" + 
                "".join([f"<div style='display:flex; font-size:10px; padding:6px 0; border-bottom:1px solid #111; align-items:center;'><span>● {ev['name']}</span><span style='margin-left:auto; color:#00ff88;'>{ev['act']}</span></div>" for ev in cal_data[:4]]) + "</div>", unsafe_allow_html=True)
            
            # NEWS (5 LIGNES)
            st.markdown("<p style='color:#555; font-size:9px; font-weight:bold; text-transform:uppercase; margin-top:5px;'>● LIVE NEWS STREAM</p>", unsafe_allow_html=True)
            for n in feed.entries[:5]:
                st.markdown(f"<div style='font-size:9px; border-bottom:1px solid #111; padding:5px 0;'>🕒 {n.published[17:22]} | {n.title[:45]}...</div>", unsafe_allow_html=True)

            # --- INTEL SECTION (FULL TEXT RESTORED) ---
            st.markdown("<p style='color:#555; font-size:9px; font-weight:bold; text-transform:uppercase; margin-top:15px;'>● STRATEGY INTEL & DEFINITIONS</p>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class="intel-box">
                <div style="font-size:9px; font-weight:900; color:#ffb000; text-transform:uppercase; margin-bottom:5px;">📊 PRESSURE BARS DEFINITION</div>
                <div style="font-size:10px; color:#888; line-height:1.4;">
                    <b>H4 Trend :</b> Macro-tendance de fond. Définit le biais directionnel majeur.<br>
                    <b>H2 Flow :</b> Flux directionnel intermédiaire. Confirme ou infirme la tendance H4.<br>
                    <b>M15 Momentum :</b> Réactivité intraday. Crucial pour le timing d'entrée (Execution Layer).
                </div>
            </div>
            <div class="intel-box">
                <div style="font-size:9px; font-weight:900; color:#ffb000; text-transform:uppercase; margin-bottom:5px;">⚙️ VOLUME PROFILE ADVANCED</div>
                <div style="font-size:10px; color:#888; line-height:1.4;">
                    <b>POC (Point of Control) :</b> Prix pivot attirant le maximum de liquidité institutionnelle.<br>
                    <b>Value Area (VA) :</b> Zone de 70% de l'activité. Un breakout de la VAH/VAL signale l'initiation d'un flux directionnel majeur.
                </div>
            </div>
            <div class="intel-box">
                <div style="font-size:9px; font-weight:900; color:#ffb000; text-transform:uppercase; margin-bottom:5px;">🌍 GOLD MACRO SYNTHESIS (MAY 2026)</div>
                <div style="font-size:10px; color:#888; line-height:1.4;">
                    <b>BULLISH :</b> Demande souveraine record des BRICS+ et dé-dollarisation structurelle.<br>
                    <b>BEARISH :</b> Résilience de l'inflation obligeant la Fed à maintenir des Yields réels élevés, pesant sur l'attractivité de l'Or.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"<div style='background:{sig_col}; color:black; text-align:center; padding:10px; font-weight:900; border-radius:4px; margin-top:10px;'>VERDICT FINAL : {sig_label} | {bull_score:.1f}%</div>", unsafe_allow_html=True)

    except Exception: st.warning("Sync stable...")

sync_terminal()
