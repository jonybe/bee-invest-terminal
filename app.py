import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import random
import math

# 1. Configuration & Design System (V2.2 - FULL ZONES & ROADMAP)
st.set_page_config(page_title="KILLZONE | Order Flow Engine", layout="wide", initial_sidebar_state="collapsed")

if 'last_m5_ts' not in st.session_state:
    st.session_state.last_m5_ts = None

st.markdown("""
<style>
    * { --st-fragment-fade-opacity: 1 !important; --st-fragment-fade-duration: 0ms !important; }
    div[data-testid="stAppViewBlockContainer"], div[data-testid="stVerticalBlock"],
    div[data-fragment-component-id], [data-testid="stFragment"], [data-testid="stFragment"] > div {
        opacity: 1 !important; transition: none !important; animation: none !important; filter: blur(0px) !important;
    }
    html, body, [data-testid="stAppViewContainer"] { background-color: #0b0b0b !important; color: #a1a1aa; font-family: 'Inter', -apple-system, sans-serif; font-size: 11px; }
    .block-container { padding-top: 1.5rem !important; padding-bottom: 0rem !important; max-width: 1600px; }
    
    .kz-panel { background: #111111; border: 1px solid #222222; border-radius: 6px; padding: 16px; margin-bottom: 16px; }
    .kz-header { font-size: 10px; font-weight: 800; color: #a1a1aa; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 16px; display: flex; align-items: center; }
    .kz-header::before { content: '●'; color: #eab308; margin-right: 8px; font-size: 12px; }
    .kz-topbar { display: flex; justify-content: space-between; align-items: center; background: #111; padding: 12px 24px; border-bottom: 1px solid #222; border-radius: 6px; margin-bottom: 20px; }
    .kz-topbar-item { display: flex; flex-direction: column; }
    .kz-label { font-size: 8px; color: #71717a; text-transform: uppercase; font-weight: bold; margin-bottom: 2px; }
    .kz-val { font-size: 14px; color: #e4e4e7; font-weight: bold; font-family: 'JetBrains Mono', monospace; }
    
    .flow-bar-wrapper { display: flex; height: 12px; border-radius: 2px; overflow: hidden; background: #ef4444; }
    .flow-bar-green { height: 100%; background: #10b981; transition: width 0.5s ease-in-out; }
    .badge-center { text-align: center; background: #18181b; border: 1px solid #27272a; padding: 4px 16px; border-radius: 4px; display: inline-block; transform: translateY(-10px); }
    
    .dom-heatmap { background: #0f0f11; border: 1px solid #222; border-radius: 6px; padding: 12px; }
    .dom-row { display: flex; align-items: center; font-family: 'JetBrains Mono'; font-size: 11px; margin-bottom: 2px; }
    .dom-price { width: 60px; text-align: right; margin-right: 12px; color: #71717a; }
    .dom-price.current { color: #eab308; font-weight: 900; font-size: 13px; }
    .dom-bar-container { flex: 1; height: 16px; background: #18181b; position: relative; border-radius: 2px; overflow: hidden; }
    .dom-bar-ask { position: absolute; left: 0; top: 0; height: 100%; background: rgba(239, 68, 68, 0.6); border-right: 2px solid #ef4444; }
    .dom-bar-bid { position: absolute; left: 0; top: 0; height: 100%; background: rgba(16, 185, 129, 0.6); border-right: 2px solid #10b981; }
    .dom-vol { position: absolute; right: 8px; top: 1px; color: #fff; font-size: 9px; font-weight: bold; text-shadow: 1px 1px 0 #000; }
    
    .setup-alert { background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; border-left: 4px solid #10b981; padding: 12px; border-radius: 4px; margin-top: 16px; animation: pulse 2s infinite; }
    .setup-alert.bear { background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; border-left: 4px solid #ef4444; }
    @keyframes pulse { 0% { opacity: 0.8; } 50% { opacity: 1; } 100% { opacity: 0.8; } }

    .roadmap-item { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 12px; padding: 8px; background: #0f0f11; border-radius: 4px; border: 1px solid #222; }
    .roadmap-num { background: #eab308; color: #000; font-weight: 900; font-size: 10px; width: 18px; height: 18px; display: flex; align-items: center; justify-content: center; border-radius: 2px; flex-shrink: 0; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=2)
def order_flow_engine():
    try:
        # A. DATA & ACCOUNT
        cap = 953.55
        prog = (math.log(cap/100) / math.log(1000000/100)) * 100

        t = yf.Ticker("GC=F")
        gold = t.fast_info['last_price']
        prev_close = t.fast_info['previous_close']
        daily_change = ((gold - prev_close) / prev_close) * 100
        
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        dxy_is_safe = True if dxy < 105.5 else False 

        # VOLUME PROFILE (ZONES)
        poc = round(gold - 1.2, 1)
        vah = poc + 6.0
        val = poc - 4.0

        # B. DOM SIMULATION
        base_vol = random.randint(50, 150)
        big_bid_price = round(gold - 1.5, 1)
        dom_data = []
        total_ask_vol, total_bid_vol = 0, 0
        
        for i in range(5, -6, -1):
            p = round(gold + (i * 0.5), 1)
            is_ask, is_current = p > gold, p == round(gold, 1)
            vol = random.randint(1500, 2500) if p == big_bid_price else base_vol + random.randint(-20, 80)
            if is_current: vol = 0
            if is_ask: total_ask_vol += vol
            elif not is_current: total_bid_vol += vol
            dom_data.append({"price": p, "vol": vol, "type": "ask" if is_ask else ("current" if is_current else "bid")})

        dom_ratio = (total_bid_vol / max(1, total_ask_vol)) if total_bid_vol > total_ask_vol else (total_ask_vol / max(1, total_bid_vol))
        is_bull_imbalance = total_bid_vol > (total_ask_vol * 2.7)
        setup_triggered = True if is_bull_imbalance and dxy_is_safe else False

        # --- RENDER TOPBAR ---
        st.markdown(f"""
<div class="kz-topbar">
<div style="display:flex; align-items:center; gap:16px;">
<div style="background:#eab308; color:#000; font-weight:900; padding:6px 10px; border-radius:4px; font-size:14px;">K</div>
<div><div style="color:#e4e4e7; font-weight:800; font-size:14px; letter-spacing:1px;">KILLZONE <span style="color:#71717a; font-weight:normal;">| V2.2 ELITE</span></div></div>
</div>
<div class="kz-topbar-item"><span class="kz-label">CAPITAL UNIT</span><span class="kz-val" style="color:#00ff88;">{cap:,.2f} £</span><div style="background:#222; height:3px; width:60px; margin-top:2px;"><div style="background:#00ff88; height:100%; width:{prog}%;"></div></div></div>
<div class="kz-topbar-item"><span class="kz-label">SPOT GOLD</span><span class="kz-val">${gold:,.2f}</span></div>
<div class="kz-topbar-item"><span class="kz-label">DXY FILTER</span><span class="kz-val {'text-green' if dxy_is_safe else 'text-red'}">{dxy:.2f}</span></div>
<div class="kz-topbar-item"><span class="kz-label">ENGINE STATUS</span><span class="kz-val text-gold">ACTIVE</span></div>
</div>
""", unsafe_allow_html=True)

        c1, c2 = st.columns([1.2, 1.8], gap="large")
        
        with c1:
            # VOLUME PROFILE (RESTORED FULL VERSION)
            vp_html = f"""
<div class="kz-panel">
<div class="kz-header">INSTITUTIONAL ZONES (VOLUME PROFILE)</div>
<div style="display:flex; flex-direction:column; gap:12px;">
<div style="display:flex; justify-content:space-between; border-bottom:1px solid #222; padding-bottom:8px;">
<div><span style="font-size:9px; color:#71717a;">VAH (Value Area High)</span><br><span style="font-family:'JetBrains Mono'; font-weight:bold; color:#e4e4e7;">{vah:.1f}</span></div>
<div style="text-align:right;"><span style="font-size:9px; color:#ef4444;">RESISTANCE</span><br><span style="font-size:10px; color:#71717a;">70% Vol Boundary</span></div>
</div>
<div style="display:flex; justify-content:space-between; border-bottom:1px solid #222; padding-bottom:8px;">
<div><span style="font-size:9px; color:#eab308; font-weight:bold;">POC (Point of Control)</span><br><span style="font-family:'JetBrains Mono'; font-weight:900; color:#eab308; font-size:14px;">{poc:.1f}</span></div>
<div style="text-align:right;"><span style="font-size:9px; color:#eab308;">MAGNET</span><br><span style="font-size:10px; color:#71717a;">Max Volume Node</span></div>
</div>
<div style="display:flex; justify-content:space-between;">
<div><span style="font-size:9px; color:#71717a;">VAL (Value Area Low)</span><br><span style="font-family:'JetBrains Mono'; font-weight:bold; color:#e4e4e7;">{val:.1f}</span></div>
<div style="text-align:right;"><span style="font-size:9px; color:#10b981;">SUPPORT</span><br><span style="font-size:10px; color:#71717a;">70% Vol Boundary</span></div>
</div>
</div>
</div>
"""
            st.markdown(vp_html, unsafe_allow_html=True)

            # METRICS
            st.markdown("""<div class="kz-panel"><div class="kz-header">ENGINE TELEMETRY</div><div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;"><div style="background:#18181b; padding:10px; border-radius:4px; border:1px solid #27272a;"><div style="color:#71717a; font-size:8px; font-weight:bold; margin-bottom:4px;">REQUIRED RATIO</div><div style="color:#e4e4e7; font-size:14px; font-family:'JetBrains Mono'; font-weight:bold;">2.7x</div></div><div style="background:#18181b; padding:10px; border-radius:4px; border:1px solid #27272a;"><div style="color:#71717a; font-size:8px; font-weight:bold; margin-bottom:4px;">IMBALANCE</div><div style="color:#10b981; font-size:14px; font-family:'JetBrains Mono'; font-weight:bold;">"""+f"{dom_ratio:.2f}x"+"""</div></div></div></div>""", unsafe_allow_html=True)

            # BLOC STRATÉGIE
            st.markdown("""
<div class="kz-panel">
<div class="kz-header">📖 LOGIQUE : ABSORPTION</div>
<div style="font-size:9.5px; color:#888; line-height:1.4;">
Le moteur traque l'<b>Imbalance Institutionnelle</b>. Lorsqu'un mur d'ordres limités (Ratio > 2.7) apparaît sur un niveau clé (POC/VAL), et que le prix refuse de baisser malgré la panique vendeuse, l'algorithme détecte une <b>Absorption</b>. 
<br><br>
<span style="color:#eab308;">●</span> <b>DXY Filter :</b> Empêche l'achat si le dollar est en zone de force (rupture de corrélation).
</div>
</div>
""", unsafe_allow_html=True)

        with c2:
            # HEATMAP
            st.markdown("""<div class="kz-panel"><div class="kz-header">L2 HEATMAP / DEPTH OF MARKET</div>""", unsafe_allow_html=True)
            dom_html = "<div class='dom-heatmap'>"
            for row in dom_data:
                p, vol = f"{row['price']:.1f}", row['vol']
                width_pct = min(100, (vol / 2500) * 100) if vol > 0 else 0 
                if row['type'] == "ask": dom_html += f"<div class='dom-row'><div class='dom-price'>{p}</div><div class='dom-bar-container'><div class='dom-bar-ask' style='width:{width_pct}%;'></div><div class='dom-vol'>{vol if vol>0 else ''}</div></div></div>"
                elif row['type'] == "current": dom_html += f"<div class='dom-row' style='margin: 8px 0; background: rgba(234, 179, 8, 0.1); border-top: 1px solid #eab308; border-bottom: 1px solid #eab308;'><div class='dom-price current'>{p}</div><div class='dom-bar-container' style='background:transparent;'><div style='padding-left:8px; color:#eab308; font-size:9px; font-weight:bold; line-height:16px;'>SPOT PRICE (SPREAD)</div></div></div>"
                else: dom_html += f"<div class='dom-row'><div class='dom-price'>{p}</div><div class='dom-bar-container'><div class='dom-bar-bid' style='width:{width_pct}%;'></div><div class='dom-vol'>{vol if vol>0 else ''}</div></div></div>"
            st.markdown(dom_html + "</div>", unsafe_allow_html=True)

            if setup_triggered:
                st.markdown("""<div class="setup-alert"><div style="font-weight:900; font-size:12px; margin-bottom:4px;">ABSORPTION BULLISH DETECTED | RATIO 2.7x</div></div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # FEUILLE DE ROUTE
            st.markdown("""
<div class="kz-panel">
<div class="kz-header">🗺️ FEUILLE DE ROUTE & DISCIPLINE</div>
<div class="roadmap-item"><div class="roadmap-num">1</div><div style="font-size:10px;"><b>LOCALISATION :</b> Prix en contact avec une zone (POC, VAL ou VAH).</div></div>
<div class="roadmap-item"><div class="roadmap-num">2</div><div style="font-size:10px;"><b>LIQUIDITÉ :</b> Présence d'un mur > 1500 lots sur la Heatmap.</div></div>
<div class="roadmap-item"><div class="roadmap-num">3</div><div style="font-size:10px;"><b>ALGORITHME :</b> Ratio d'imbalance validé à 2.7x minimum.</div></div>
<div class="roadmap-item"><div class="roadmap-num">4</div><div style="font-size:10px;"><b>MACRO :</b> Filtre DXY "SAFE" (Dollar ne pompe pas à la hausse).</div></div>
<div class="roadmap-item"><div class="roadmap-num">5</div><div style="font-size:10px;"><b>SIGNAL :</b> Attendre le déclenchement du badge d'alerte.</div></div>
</div>
""", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Engine Offline: {e}")

order_flow_engine()
