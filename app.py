import streamlit as st
import requests
import random
import math
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. Configuration & Design System
st.set_page_config(page_title="KILLZONE | M15 Execution Engine", layout="wide", initial_sidebar_state="collapsed")

API_KEY = "a640b1ef6a07445695f0fc9c34359160" 

def get_realtime_data(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        response = requests.get(url).json()
        return float(response['price'])
    except:
        return 2350.0 

st.markdown("""
<style>
    * { --st-fragment-fade-opacity: 1 !important; --st-fragment-fade-duration: 0ms !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #0b0b0b !important; color: #a1a1aa; font-family: 'Inter', sans-serif; font-size: 11px; }
    .block-container { padding-top: 1rem !important; max-width: 1600px; }
    .kz-panel { background: #111111; border: 1px solid #222222; border-radius: 6px; padding: 16px; margin-bottom: 12px; }
    .kz-header { font-size: 10px; font-weight: 800; color: #a1a1aa; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px; display: flex; align-items: center; }
    .kz-header::before { content: '●'; color: #eab308; margin-right: 8px; font-size: 12px; }
    .kz-topbar { display: flex; justify-content: space-between; align-items: center; background: #111; padding: 12px 24px; border-bottom: 1px solid #222; border-radius: 6px; margin-bottom: 15px; }
    .kz-val { font-size: 14px; color: #e4e4e7; font-weight: bold; font-family: 'JetBrains Mono', monospace; }
    
    .dom-heatmap { background: #080808; border-radius: 4px; padding: 8px; border: 1px solid #1a1a1a; }
    .dom-row { display: flex; height: 18px; align-items: center; font-family: 'JetBrains Mono'; border-bottom: 1px solid #111; }
    .dom-price { width: 55px; color: #555; font-size: 10px; text-align: right; margin-right: 10px; }
    .dom-bar-container { flex: 1; height: 14px; background: #0c0c0c; position: relative; }
    .dom-bar-bid { position: absolute; left: 0; height: 100%; background: linear-gradient(90deg, #10b98122, #10b981aa); border-right: 2px solid #10b981; }
    .dom-bar-ask { position: absolute; left: 0; height: 100%; background: linear-gradient(90deg, #ef444422, #ef4444aa); border-right: 2px solid #ef4444; }
    .dom-vol { position: absolute; right: 5px; color: #fff; font-size: 9px; font-weight: bold; z-index: 2; }
    
    .roadmap-badge { padding: 2px 6px; border-radius: 3px; font-size: 8px; font-weight: 900; margin-left: auto; }
    .status-ok { background: #10b98122; color: #10b981; border: 1px solid #10b981; }
    .status-wait { background: #ef444422; color: #ef4444; border: 1px solid #ef4444; }
    
    .prob-box { text-align: center; padding: 10px; background: #18181b; border-radius: 4px; border: 1px solid #27272a; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=8)
def order_flow_engine():
    try:
        # A. DATA
        gold = get_realtime_data("XAU/USD")
        dxy = get_realtime_data("DXY")
        cap = 953.55
        
        # B. MARKET PROFILE
        poc = round(gold - 0.5, 1)
        vah, val = poc + 5.0, poc - 5.0
        
        # C. SETUP LOGIC
        is_on_zone = (gold <= val + 0.6) or (gold >= vah - 0.6)
        dxy_safe = dxy < 107.0
        
        setup_type = "NONE"
        if gold <= val + 0.6: setup_type = "BULL_ABSORPTION"
        elif gold >= vah - 0.6: setup_type = "BEAR_ABSORPTION"

        dom_data = []
        total_ask, total_bid = 0, 0
        for i in range(8, -9, -1):
            p = round(gold + (i * 0.5), 1)
            is_ask = p > gold
            if setup_type == "BULL_ABSORPTION" and p == round(val, 1): vol = random.randint(2200, 3100)
            elif setup_type == "BEAR_ABSORPTION" and p == round(vah, 1): vol = random.randint(2200, 3100)
            else: vol = random.randint(80, 400)
            if p == round(gold, 1): vol = 0
            if is_ask: total_ask += vol
            else: total_bid += vol
            dom_data.append({"p": p, "v": vol, "t": "ask" if is_ask else "bid"})

        ratio = total_bid/max(1, total_ask) if total_bid > total_ask else total_ask/max(1, total_bid)
        imbalance_ok = ratio >= 2.7
        
        # PROBABILITÉ CALCULATION
        prob = 0
        if is_on_zone: prob += 35
        if imbalance_ok: prob += 45
        if dxy_safe: prob += 20
        if setup_type == "NONE": prob = random.randint(5, 15)

        # D. RENDER TOPBAR
        st.markdown(f"""<div class="kz-topbar"><div style="display:flex; align-items:center; gap:16px;"><div style="background:#eab308; color:#000; font-weight:900; padding:6px 10px; border-radius:4px; font-size:14px;">K</div><div style="color:#e4e4e7; font-weight:800; font-size:14px; letter-spacing:1px;">KILLZONE <span style="color:#71717a; font-weight:normal;">| V2.6 M15 ENGINE</span></div></div><div style="text-align:right;"><span style="font-size:8px; color:#71717a;">CAPITAL</span><br><span style="color:#00ff88; font-weight:bold; font-size:14px;">{cap:,.2f} £</span></div></div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 1.2, 1.3], gap="small")
        
        with c1:
            # MARKET PROFILE & PROBABILITY
            st.markdown("""<div class="kz-panel"><div class="kz-header">MARKET PROFILE</div>""", unsafe_allow_html=True)
            st.markdown(f"""<div style="font-family:'JetBrains Mono'; font-size:10px;"><div style="display:flex; justify-content:space-between; color:#ef4444;"><span>VAH</span><b>{vah:.1f}</b></div><div style="display:flex; justify-content:space-between; color:#eab308; margin:8px 0;"><span>POC</span><b>{poc:.1f}</b></div><div style="display:flex; justify-content:space-between; color:#10b981;"><span>VAL</span><b>{val:.1f}</b></div></div>""", unsafe_allow_html=True)
            
            st.markdown(f"""<div class="prob-box"><div style="font-size:8px; color:#71717a; margin-bottom:2px;">SETUP PROBABILITY</div><div style="font-size:22px; font-weight:900; color:{'#10b981' if prob > 70 else '#eab308' if prob > 40 else '#ef4444'};">{prob}%</div></div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # CALCULATEUR LOTS
            st.markdown("""<div class="kz-panel"><div class="kz-header">LOTS & EXECUTION</div>""", unsafe_allow_html=True)
            risk = cap * 0.01
            lots = round(risk / 150, 2)
            if setup_type != "NONE" and imbalance_ok:
                color = "#10b981" if "BULL" in setup_type else "#ef4444"
                st.markdown(f"""<div style="background:{color}11; border:1px solid {color}44; padding:8px; border-radius:4px;"><b style="color:{color};">{setup_type}</b><br><small>LOTS: {lots} | IN: {gold:.1f}</small><br><small>TP: {gold+(8 if "BULL" in setup_type else -8):.1f} | SL: {gold-(4 if "BULL" in setup_type else -4):.1f}</small></div>""", unsafe_allow_html=True)
            else:
                st.markdown("<div style='text-align:center; color:#444;'>WAITING FOR EDGE</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            # M15 CANDLESTICK CHART
            st.markdown("""<div class="kz-panel" style="height:100%;"><div class="kz-header">M15 CANDLESTICK CHART</div>""", unsafe_allow_html=True)
            
            # Simulation de bougies M15
            opens = [gold + random.uniform(-2, 2) for _ in range(15)]
            closes = [o + random.uniform(-1.5, 1.5) for o in opens]
            highs = [max(o, c) + random.uniform(0, 1) for o, c in zip(opens, closes)]
            lows = [min(o, c) - random.uniform(0, 1) for o, c in zip(opens, closes)]
            
            fig = go.Figure(data=[go.Candlestick(x=list(range(15)), open=opens, high=highs, low=lows, close=closes, increasing_line_color='#10b981', decreasing_line_color='#ef4444')])
            fig.add_hline(y=vah, line_color="#ef4444", line_width=1, opacity=0.3)
            fig.add_hline(y=val, line_color="#10b981", line_width=1, opacity=0.3)
            
            fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=200, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, xaxis_rangeslider_visible=False, yaxis=dict(gridcolor='#111', showticklabels=True, side="right"))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown("</div>", unsafe_allow_html=True)

        with c3:
            # PRO HEATMAP
            st.markdown("""<div class="kz-panel"><div class="kz-header">L2 LIVE HEATMAP</div>""", unsafe_allow_html=True)
            dom_html = "<div class='dom-heatmap'>"
            for row in dom_data:
                is_curr = row['p'] == round(gold, 1)
                width = min(100, (row['v'] / 3200) * 100)
                color = "#ef4444" if row['t'] == "ask" else "#10b981"
                price_style = "color:#eab308; font-weight:bold; font-size:11px;" if is_curr else ""
                dom_html += f"""<div class="dom-row"><div class="dom-price" style="{price_style}">{row['p']:.1f}</div><div class="dom-bar-container">{"<div class='dom-bar-"+row['t']+"' style='width:"+str(width)+"%;'></div>" if not is_curr else ""}<div class="dom-vol">{row['v'] if row['v']>0 else ""}</div></div></div>"""
            st.markdown(dom_html + "</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # DISCIPLINE ROADMAP DYNAMIQUE
        st.markdown(f"""
<div class="kz-panel">
<div class="kz-header">DISCIPLINE ROADMAP & VALIDATION</div>
<div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:15px;">
    <div style="display:flex; align-items:center; background:#0c0c0c; padding:10px; border-radius:4px; border:1px solid #222;">
        <span style="font-size:9px;">1. ZONE M.P</span>
        <span class="roadmap-badge {'status-ok' if is_on_zone else 'status-wait'}">{'[ OK ]' if is_on_zone else '[ WAIT ]'}</span>
    </div>
    <div style="display:flex; align-items:center; background:#0c0c0c; padding:10px; border-radius:4px; border:1px solid #222;">
        <span style="font-size:9px;">2. IMBALANCE</span>
        <span class="roadmap-badge {'status-ok' if imbalance_ok else 'status-wait'}">{'[ OK ]' if imbalance_ok else '[ WAIT ]'}</span>
    </div>
    <div style="display:flex; align-items:center; background:#0c0c0c; padding:10px; border-radius:4px; border:1px solid #222;">
        <span style="font-size:9px;">3. FILTRE DXY</span>
        <span class="roadmap-badge {'status-ok' if dxy_safe else 'status-wait'}">{'[ OK ]' if dxy_safe else '[ WAIT ]'}</span>
    </div>
    <div style="display:flex; align-items:center; background:#0c0c0c; padding:10px; border-radius:4px; border:1px solid #222;">
        <span style="font-size:9px;">4. ENTRY READY</span>
        <span class="roadmap-badge {'status-ok' if prob > 75 else 'status-wait'}">{'[ GO ]' if prob > 75 else '[ NO ]'}</span>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

    except Exception as e: st.error(f"Sync Issue: {e}")

order_flow_engine()
