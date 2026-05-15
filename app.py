import streamlit as st
import requests
import random
import math
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. Configuration & Design System
st.set_page_config(page_title="KILLZONE | Professional Execution", layout="wide", initial_sidebar_state="collapsed")

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
    
    /* DOM PRO VISUAL */
    .dom-heatmap { background: #080808; border-radius: 4px; padding: 8px; border: 1px solid #1a1a1a; }
    .dom-row { display: flex; height: 18px; align-items: center; font-family: 'JetBrains Mono'; border-bottom: 1px solid #111; }
    .dom-price { width: 55px; color: #444; font-size: 10px; text-align: right; margin-right: 10px; }
    .dom-bar-container { flex: 1; height: 14px; background: #0c0c0c; position: relative; }
    .dom-bar-bid { position: absolute; left: 0; height: 100%; background: linear-gradient(90deg, #10b98133, #10b981aa); border-right: 2px solid #10b981; }
    .dom-bar-ask { position: absolute; left: 0; height: 100%; background: linear-gradient(90deg, #ef444433, #ef4444aa); border-right: 2px solid #ef4444; }
    .dom-vol { position: absolute; right: 5px; color: #fff; font-size: 9px; font-weight: bold; z-index: 2; }
    
    .trade-card { background: #18181b; border: 1px solid #27272a; padding: 12px; border-radius: 4px; }
    .roadmap-item { display: flex; align-items: flex-start; gap: 8px; margin-bottom: 8px; font-size: 9px; }
    .roadmap-num { background: #eab308; color: #000; font-weight: 900; width: 15px; height: 15px; display: flex; align-items: center; justify-content: center; border-radius: 2px; flex-shrink: 0; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=8)
def order_flow_engine():
    try:
        # A. DATA
        gold = get_realtime_data("XAU/USD")
        dxy = get_realtime_data("DXY")
        cap = 953.55
        prog = (math.log(cap/100) / math.log(1000000/100)) * 100
        
        # B. VOLUME PROFILE CALCULATIONS
        poc = round(gold - 0.5, 1)
        vah, val = poc + 5.0, poc - 5.0
        
        # C. DOM ENGINE & SETUP DETECTION
        dom_data = []
        total_ask, total_bid = 0, 0
        big_wall_price = 0
        
        # Simulation d'un setup (Absorption sur VAL ou VAH)
        setup_type = "NONE"
        if gold <= val + 0.5: setup_type = "BULL_ABSORPTION"
        elif gold >= vah - 0.5: setup_type = "BEAR_ABSORPTION"

        for i in range(8, -9, -1):
            p = round(gold + (i * 0.5), 1)
            is_ask = p > gold
            # Simulation mur institutionnel si setup détecté
            if setup_type == "BULL_ABSORPTION" and p == round(val, 1): vol = random.randint(2100, 2900)
            elif setup_type == "BEAR_ABSORPTION" and p == round(vah, 1): vol = random.randint(2100, 2900)
            else: vol = random.randint(100, 450)
            
            if p == round(gold, 1): vol = 0
            if is_ask: total_ask += vol
            else: total_bid += vol
            dom_data.append({"p": p, "v": vol, "t": "ask" if is_ask else "bid"})

        ratio = total_bid/max(1, total_ask) if total_bid > total_ask else total_ask/max(1, total_bid)
        dxy_safe = dxy < 107.0
        
        # --- RENDER TOPBAR ---
        st.markdown(f"""<div class="kz-topbar"><div style="display:flex; align-items:center; gap:16px;"><div style="background:#eab308; color:#000; font-weight:900; padding:6px 10px; border-radius:4px; font-size:14px;">K</div><div style="color:#e4e4e7; font-weight:800; font-size:14px; letter-spacing:1px;">KILLZONE <span style="color:#71717a; font-weight:normal;">| V2.5 PRO EXECUTION</span></div></div><div style="text-align:right;"><span style="font-size:8px; color:#71717a;">CAPITAL UNIT</span><br><span style="color:#00ff88; font-weight:bold; font-size:14px;">{cap:,.2f} £</span></div></div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 1.2, 1.3], gap="small")
        
        with c1:
            # VOLUME PROFILE & SIGNAL
            st.markdown("""<div class="kz-panel"><div class="kz-header">MARKET PROFILE ZONES</div>""", unsafe_allow_html=True)
            st.markdown(f"""<div style="font-family:'JetBrains Mono'; font-size:10px;"><div style="display:flex; justify-content:space-between; color:#ef4444;"><span>VAH (SELL ZONE)</span><b>{vah:.1f}</b></div><div style="display:flex; justify-content:space-between; color:#eab308; margin:8px 0;"><span>POC (PIVOT)</span><b>{poc:.1f}</b></div><div style="display:flex; justify-content:space-between; color:#10b981;"><span>VAL (BUY ZONE)</span><b>{val:.1f}</b></div></div>""", unsafe_allow_html=True)
            
            if setup_type != "NONE" and ratio >= 2.7:
                color = "#10b981" if "BULL" in setup_type else "#ef4444"
                st.markdown(f"""<div style="background:{color}22; border:1px solid {color}; padding:10px; border-radius:4px; margin-top:10px; text-align:center;"><b style="color:{color}; font-size:11px;">ALERTE : {setup_type.replace('_', ' ')}</b><br><small style="color:#aaa;">Ratio: {ratio:.1f}x | DXY: {dxy:.2f}</small></div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div style="border:1px dashed #333; padding:10px; border-radius:4px; margin-top:10px; text-align:center; color:#555; font-size:10px;">EN ATTENTE DE LIQUIDITÉ...</div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # POSITION CALCULATOR
            st.markdown("""<div class="kz-panel"><div class="kz-header">EXECUTION CALCULATOR</div>""", unsafe_allow_html=True)
            risk = cap * 0.01 # Risque 1%
            # Taille de lot approx: (Risque / 10$ par tick pour 1 lot sur Or)
            lots = round(risk / 150, 2) # Basé sur un SL de 15 ticks
            
            if setup_type == "BULL_ABSORPTION":
                st.markdown(f"""<div class="trade-card"><b style="color:#10b981;">PROPOSITION LONG</b><br><small style="color:#71717a;">LOTS: {lots} | RISQUE: {risk:.2f}£</small><hr style="margin:5px 0; border-color:#333;"><div style="font-size:10px; font-family:'JetBrains Mono';">IN: {gold:.1f}<br>TP: {gold+8:.1f}<br>SL: {gold-4:.1f}</div></div>""", unsafe_allow_html=True)
            elif setup_type == "BEAR_ABSORPTION":
                st.markdown(f"""<div class="trade-card"><b style="color:#ef4444;">PROPOSITION SHORT</b><br><small style="color:#71717a;">LOTS: {lots} | RISQUE: {risk:.2f}£</small><hr style="margin:5px 0; border-color:#333;"><div style="font-size:10px; font-family:'JetBrains Mono';">IN: {gold:.1f}<br>TP: {gold-8:.1f}<br>SL: {gold+4:.1f}</div></div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div style="text-align:center; color:#444; padding:5px;">NO ACTIVE SETUP</div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            # PRICE ACTION GRAPH
            st.markdown("""<div class="kz-panel" style="height:100%;"><div class="kz-header">ORDER FLOW CHART</div>""", unsafe_allow_html=True)
            fig = go.Figure()
            # Simulation prix
            hist_prices = [gold + random.uniform(-1, 1) for _ in range(20)] + [gold]
            fig.add_trace(go.Scatter(y=hist_prices, mode='lines+markers', line=dict(color='#eab308', width=2), marker=dict(size=4)))
            # Zones
            fig.add_hline(y=vah, line_dash="dash", line_color="#ef4444", annotation_text="VAH")
            fig.add_hline(y=poc, line_dash="dot", line_color="#555", annotation_text="POC")
            fig.add_hline(y=val, line_dash="dash", line_color="#10b981", annotation_text="VAL")
            fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=180, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, yaxis=dict(gridcolor='#111', zeroline=False), xaxis=dict(showgrid=False, showticklabels=False))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            # STRATEGY INFO
            st.markdown("""<div style="font-size:9px; color:#666; padding-top:10px;"><b>LOGIQUE :</b> Absorption confirmée si mur > 2.7x sur VAL/VAH. DXY doit confirmer la faiblesse/force du USD.</div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with c3:
            # PRO HEATMAP
            st.markdown("""<div class="kz-panel"><div class="kz-header">L2 HEATMAP (LIVE LIQUIDITY)</div>""", unsafe_allow_html=True)
            dom_html = "<div class='dom-heatmap'>"
            for row in dom_data:
                p_str = f"{row['p']:.1f}"
                is_curr = row['p'] == round(gold, 1)
                bar_class = "dom-bar-ask" if row['t'] == "ask" else "dom-bar-bid"
                width = min(100, (row['v'] / 3000) * 100)
                price_style = "color:#eab308; font-weight:bold;" if is_curr else ""
                dom_html += f"""<div class="dom-row"><div class="dom-price" style="{price_style}">{p_str}</div><div class="dom-bar-container">{"<div class='"+bar_class+"' style='width:"+str(width)+"%;'></div>" if not is_curr else ""}<div class="dom-vol">{row['v'] if row['v']>0 else ""}</div></div></div>"""
            st.markdown(dom_html + "</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # ROADMAP FOOTER
        st.markdown("""<div class="kz-panel"><div class="kz-header">DISCIPLINE ROADMAP</div><div style="display:flex; gap:20px;">
        <div class="roadmap-item"><div class="roadmap-num">1</div><span><b>LOCALISATION :</b> Prix sur VAH/VAL?</span></div>
        <div class="roadmap-item"><div class="roadmap-num">2</div><span><b>DOM :</b> Mur > 2.7x?</span></div>
        <div class="roadmap-item"><div class="roadmap-num">3</div><span><b>DXY :</b> Corrélation OK?</span></div>
        <div class="roadmap-item"><div class="roadmap-num">4</div><span><b>RISK :</b> Taille de lot respectée?</span></div>
        </div></div>""", unsafe_allow_html=True)

    except Exception as e: st.error(f"Sync Issue: {e}")

order_flow_engine()
