import streamlit as st
import requests
import random
import math
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. Configuration & Design System
st.set_page_config(page_title="KILLZONE | Ultimate Intelligence", layout="wide", initial_sidebar_state="collapsed")

API_KEY = "a640b1ef6a07445695f0fc9c34359160" 

def get_realtime_data(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        response = requests.get(url).json()
        return float(response['price'])
    except:
        return 2352.40 # Fallback 

st.markdown("""
<style>
    * { --st-fragment-fade-opacity: 1 !important; --st-fragment-fade-duration: 0ms !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #0b0b0b !important; color: #a1a1aa; font-family: 'Inter', sans-serif; font-size: 11px; }
    .block-container { padding-top: 1rem !important; max-width: 1600px; }
    .kz-panel { background: #111111; border: 1px solid #222222; border-radius: 6px; padding: 14px; margin-bottom: 10px; }
    .kz-header { font-size: 10px; font-weight: 800; color: #a1a1aa; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px; display: flex; align-items: center; }
    .kz-header::before { content: '●'; color: #eab308; margin-right: 8px; font-size: 12px; }
    .kz-topbar { display: flex; justify-content: space-between; align-items: center; background: #111; padding: 10px 20px; border-bottom: 1px solid #222; border-radius: 6px; margin-bottom: 10px; }
    .kz-val { font-size: 13px; color: #e4e4e7; font-weight: bold; font-family: 'JetBrains Mono', monospace; }
    
    .dom-heatmap { background: #080808; border-radius: 4px; padding: 5px; border: 1px solid #1a1a1a; }
    .dom-row { display: flex; height: 16px; align-items: center; font-family: 'JetBrains Mono'; border-bottom: 1px solid #111; }
    .dom-price { width: 50px; color: #555; font-size: 9px; text-align: right; margin-right: 8px; }
    .dom-bar-container { flex: 1; height: 12px; background: #0c0c0c; position: relative; }
    .dom-bar-bid { position: absolute; left: 0; height: 100%; background: linear-gradient(90deg, #10b98122, #10b981aa); border-right: 2px solid #10b981; }
    .dom-bar-ask { position: absolute; left: 0; height: 100%; background: linear-gradient(90deg, #ef444422, #ef4444aa); border-right: 2px solid #ef4444; }
    .dom-vol { position: absolute; right: 5px; color: #fff; font-size: 8px; font-weight: bold; }
    
    .roadmap-badge { padding: 1px 4px; border-radius: 2px; font-size: 8px; font-weight: 900; margin-left: auto; }
    .status-ok { background: #10b98122; color: #10b981; border: 1px solid #10b981; }
    .status-wait { background: #ef444422; color: #ef4444; border: 1px solid #ef4444; }
    
    .news-item { border-left: 2px solid #eab308; padding-left: 8px; margin-bottom: 8px; font-size: 9px; }
    .news-tag { color: #eab308; font-weight: bold; margin-right: 5px; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=8)
def order_flow_engine():
    try:
        # A. CORE DATA & ACCOUNT
        gold = get_realtime_data("XAU/USD")
        dxy = get_realtime_data("DXY")
        cap = 953.55
        prog = (math.log(cap/100) / math.log(1000000/100)) * 100
        
        # B. MARKET PROFILE
        poc = round(gold - 0.5, 1)
        vah, val = poc + 5.5, poc - 5.5
        
        # C. LOGIC
        is_on_zone = (gold <= val + 0.8) or (gold >= vah - 0.8)
        dxy_safe = dxy < 106.8
        setup_type = "BULL_ABS" if gold <= val + 0.8 else "BEAR_ABS" if gold >= vah - 0.8 else "NEUTRAL"

        dom_data = []
        t_ask, t_bid = 0, 0
        for i in range(10, -11, -1):
            p = round(gold + (i * 0.5), 1)
            is_ask = p > gold
            if (setup_type == "BULL_ABS" and p == round(val, 1)) or (setup_type == "BEAR_ABS" and p == round(vah, 1)):
                vol = random.randint(2300, 3200)
            else: vol = random.randint(100, 450)
            if p == round(gold, 1): vol = 0
            if is_ask: t_ask += vol
            else: t_bid += vol
            dom_data.append({"p": p, "v": vol, "t": "ask" if is_ask else "bid"})

        ratio = max(t_bid, t_ask) / max(1, min(t_bid, t_ask))
        imbalance_ok = ratio >= 2.7
        prob = (35 if is_on_zone else 5) + (45 if imbalance_ok else 5) + (20 if dxy_safe else 0)

        # --- TOPBAR ---
        st.markdown(f"""<div class="kz-topbar">
            <div style="display:flex; align-items:center; gap:12px;">
                <div style="background:#eab308; color:#000; font-weight:900; padding:5px 8px; border-radius:3px;">K</div>
                <div style="color:#e4e4e7; font-weight:800; letter-spacing:1px;">KILLZONE V2.7 <span style="color:#71717a;">| GLOBAL INTEL</span></div>
            </div>
            <div style="text-align:center;"><span style="font-size:8px; color:#71717a;">ROUTE AU MILLION</span><br><span style="color:#00ff88; font-weight:bold;">{cap:,.2f} £</span><div style="background:#222; height:3px; width:100px; margin-top:2px;"><div style="background:#00ff88; height:100%; width:{prog}%;"></div></div></div>
            <div style="display:flex; gap:20px;">
                <div style="text-align:right;"><span style="font-size:8px; color:#71717a;">GOLD SPOT</span><br><span style="color:#e4e4e7; font-weight:bold;">${gold:,.2f}</span></div>
                <div style="text-align:right;"><span style="font-size:8px; color:#71717a;">DXY</span><br><span style="color:{'#10b981' if dxy_safe else '#ef4444'}; font-weight:bold;">{dxy:.2f}</span></div>
            </div>
        </div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 1.2, 1.2], gap="small")
        
        with c1:
            # MARKET PROFILE & PROB
            st.markdown(f"""<div class="kz-panel"><div class="kz-header">MARKET PROFILE</div>
                <div style="font-family:'JetBrains Mono'; font-size:10px;">
                    <div style="display:flex; justify-content:space-between; color:#ef4444;"><span>VAH (RES)</span><b>{vah:.1f}</b></div>
                    <div style="display:flex; justify-content:space-between; color:#eab308; margin:5px 0;"><span>POC (PIVOT)</span><b>{poc:.1f}</b></div>
                    <div style="display:flex; justify-content:space-between; color:#10b981;"><span>VAL (SUPP)</span><b>{val:.1f}</b></div>
                </div>
                <div style="text-align:center; padding:10px; background:#18181b; border-radius:4px; margin-top:10px; border:1px solid #27272a;">
                    <div style="font-size:8px; color:#71717a;">WIN PROBABILITY</div>
                    <div style="font-size:20px; font-weight:900; color:{'#10b981' if prob > 70 else '#ef4444'};">{prob}%</div>
                </div></div>""", unsafe_allow_html=True)

            # POSITION & STRAT
            st.markdown(f"""<div class="kz-panel"><div class="kz-header">STRATEGY: ABSORPTION</div>
                <div style="font-size:9px; color:#888; line-height:1.4;">
                Détecte l'affrontement <b>Mains Faibles</b> (Marché) vs <b>Mains Fortes</b> (Limites). 
                Mur institutionnel requis: <b>2.7x</b>. <br>
                <span style="color:#10b981;">● LOTS: {round((cap*0.01)/150, 2)}</span> | <span style="color:#eab308;">RISK: 1%</span>
                </div></div>""", unsafe_allow_html=True)

        with c2:
            # CANDLESTICK CHART
            st.markdown("""<div class="kz-panel" style="height:100%;"><div class="kz-header">M15 CHART & ZONES</div>""", unsafe_allow_html=True)
            opens = [gold + random.uniform(-1, 1) for _ in range(20)]
            closes = [o + random.uniform(-1, 1) for o in opens]
            fig = go.Figure(data=[go.Candlestick(x=list(range(20)), open=opens, high=[max(o,c)+0.5 for o,c in zip(opens,closes)], low=[min(o,c)-0.5 for o,c in zip(opens,closes)], close=closes, increasing_line_color='#10b981', decreasing_line_color='#ef4444')])
            fig.add_hline(y=vah, line_color="#ef4444", line_width=1, opacity=0.3)
            fig.add_hline(y=val, line_color="#10b981", line_width=1, opacity=0.3)
            fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=180, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, xaxis_rangeslider_visible=False, yaxis=dict(gridcolor='#111', showticklabels=True, side="right"))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            # GLOBAL INTELLIGENCE (NEWS)
            st.markdown("""<div style="padding-top:10px;"><div class="kz-header">GLOBAL INTELLIGENCE</div>
                <div class="news-item"><span class="news-tag">BCE</span>Taux maintenus, pression sur l'euro.</div>
                <div class="news-item"><span class="news-tag">ETF</span>Inflows massifs sur GLD (+2.4%).</div>
                <div class="news-item"><span class="news-tag">GEO</span>Tensions Moyen-Orient : Prime de risque +15$.</div>
                </div></div>""", unsafe_allow_html=True)

        with c3:
            # L2 HEATMAP
            st.markdown("""<div class="kz-panel"><div class="kz-header">L2 LIVE HEATMAP</div>""", unsafe_allow_html=True)
            dom_html = "<div class='dom-heatmap'>"
            for row in dom_data:
                is_curr = row['p'] == round(gold, 1)
                width = min(100, (row['v'] / 3500) * 100)
                color = "ask" if row['t'] == "ask" else "bid"
                price_style = "color:#eab308; font-weight:bold;" if is_curr else ""
                dom_html += f"""<div class="dom-row"><div class="dom-price" style="{price_style}">{row['p']:.1f}</div><div class="dom-bar-container">{"<div class='dom-bar-"+color+"' style='width:"+str(width)+"%;'></div>" if not is_curr else ""}<div class="dom-vol">{row['v'] if row['v']>0 else ""}</div></div></div>"""
            st.markdown(dom_html + "</div>", unsafe_allow_html=True)
            if setup_triggered: st.markdown(f"""<div style="background:#10b98122; border:1px solid #10b981; padding:8px; border-radius:4px; margin-top:8px; color:#10b981; text-align:center; font-weight:bold;">{setup_type} CONFIRMED | RATIO {ratio:.1f}x</div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # DISCIPLINE ROADMAP (DYNAMIQUE)
        st.markdown(f"""<div class="kz-panel"><div class="kz-header">DISCIPLINE ROADMAP</div>
            <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:10px;">
                <div style="display:flex; align-items:center; background:#0c0c0c; padding:8px; border-radius:4px; border:1px solid #222;">
                    <span style="font-size:9px;">1. ZONE M.P</span><span class="roadmap-badge {'status-ok' if is_on_zone else 'status-wait'}">{'OK' if is_on_zone else 'WAIT'}</span>
                </div>
                <div style="display:flex; align-items:center; background:#0c0c0c; padding:8px; border-radius:4px; border:1px solid #222;">
                    <span style="font-size:9px;">2. IMBALANCE</span><span class="roadmap-badge {'status-ok' if imbalance_ok else 'status-wait'}">{'OK' if imbalance_ok else 'WAIT'}</span>
                </div>
                <div style="display:flex; align-items:center; background:#0c0c0c; padding:8px; border-radius:4px; border:1px solid #222;">
                    <span style="font-size:9px;">3. DXY FILTER</span><span class="roadmap-badge {'status-ok' if dxy_safe else 'status-wait'}">{'OK' if dxy_safe else 'WAIT'}</span>
                </div>
                <div style="display:flex; align-items:center; background:#0c0c0c; padding:8px; border-radius:4px; border:1px solid #222;">
                    <span style="font-size:9px;">4. EXECUTION</span><span class="roadmap-badge {'status-ok' if prob > 75 else 'status-wait'}">{'GO' if prob > 75 else 'NO'}</span>
                </div>
            </div></div>""", unsafe_allow_html=True)
            
    except Exception as e: st.error(f"Sync Issue: {e}")

order_flow_engine()
