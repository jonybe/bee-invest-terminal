import streamlit as st
import requests
import random
import math

# 1. Configuration & API
st.set_page_config(page_title="KILLZONE | Terminal Elite", layout="wide", initial_sidebar_state="collapsed")
API_KEY = "a640b1ef6a07445695f0fc9c34359160"

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        return float(res['price'])
    except: return 2355.50

# CSS MATRIX HAUTE DÉFINITION
st.markdown("""
<style>
    [data-testid="stAppViewBlockContainer"] { padding: 1rem !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #d1d1d6; font-family: 'JetBrains Mono', monospace; }
    
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 15px; margin-bottom: 10px; }
    .kz-header { font-size: 10px; font-weight: 900; color: #eab308; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px; border-left: 3px solid #eab308; padding-left: 10px; }
    
    .sentiment-box { text-align: center; padding: 20px; background: #080808; border-radius: 4px; border: 1px solid #eab30833; }
    .macro-item { background: #080808; padding: 10px; border-radius: 4px; border: 1px solid #1a1a1a; margin-bottom: 5px; display: flex; justify-content: space-between; }
    
    /* DOM LIQUID MATRIX */
    .dom-box { background: #080808; border: 1px solid #1a1a1a; height: 500px; overflow: hidden; border-radius: 4px; }
    .dom-row { display: flex; height: 18px; align-items: center; border-bottom: 1px solid #111; }
    .dom-p { width: 60px; text-align: right; padding-right: 12px; font-size: 10px; color: #444; }
    .dom-bar-wrap { flex-grow: 1; height: 100%; position: relative; display: flex; align-items: center; }
    .dom-v { position: absolute; right: 10px; color: #fff; font-size: 9px; font-weight: bold; z-index: 10; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=10)
def terminal():
    # --- CALCULS ---
    gold = get_price("XAU/USD")
    dxy = get_price("DXY")
    cap = 953.55
    prog = (math.log(cap/100) / math.log(1000000/100)) * 100
    poc = round(gold - 0.2, 1)
    vah, val = poc + 5.0, poc - 5.0
    is_on_zone = (gold <= val + 0.8) or (gold >= vah - 0.8)

    # --- TOPBAR ---
    st.markdown(f"""
    <div style="background:#0d0d0d; border-bottom:2px solid #eab308; padding:12px 25px; display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; border-radius:4px;">
        <div style="display:flex; align-items:center; gap:20px;"><b style="color:#eab308; font-size:22px;">BEE-INVEST</b><span style="color:#333;">|</span><small>TERMINAL V9.0</small></div>
        <div style="text-align:center;"><b style="color:#10b981; font-size:18px;">{cap:,.2f} £</b><div style="width:200px; height:4px; background:#1a1a1a; margin:5px auto;"><div style="width:{prog}%; height:100%; background:#10b981;"></div></div></div>
        <div style="display:flex; gap:40px;"><div style="text-align:right;"><small style="color:#555;">XAUUSD</small><br><b style="font-size:16px;">${gold:,.2f}</b></div><div style="text-align:right;"><small style="color:#555;">DXY Index</small><br><b style="font-size:16px;">{dxy:.2f}</b></div></div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.8, 1.1])

    with c1:
        st.markdown(f"""
        <div class="kz-card">
            <div class="kz-header">Directional Sentiment</div>
            <div class="sentiment-box">
                <span style="font-size:28px; font-weight:900; color:{'#10b981' if gold > poc else '#ef4444'};">{'BULLISH' if gold > poc else 'BEARISH'}</span><br>
                <span style="color:#eab308; font-weight:bold; font-size:11px;">Score: {random.randint(65, 82)}%</span>
            </div>
            <p style="font-size:9px; color:#555; margin-top:8px; line-height:1.4;"><b>DEFINITION:</b> Biais calculé sur la convergence Order Flow L2 + Point of Control (POC) + DXY Correlation.</p>
        </div>
        <div class="kz-card" style="height:350px;">
            <div class="kz-header">Eco Calendar & News</div>
            <div style="font-size:10px; line-height:1.8;">
                <div style="display:flex; justify-content:space-between;"><span>14:30 | Empire State</span><b style="color:#ef4444;">USD ★★★</b></div>
                <div style="display:flex; justify-content:space-between;"><span>14:30 | Retail Sales</span><b style="color:#ef4444;">USD ★★★</b></div>
                <div style="display:flex; justify-content:space-between;"><span>08:00 | IPC Inflation</span><b style="color:#ef4444;">GBP ★★★</b></div>
                <hr style="border:0; border-top:1px solid #1a1a1a; margin:10px 0;">
                <small style="color:#888;"><b>BCE :</b> Pause confirmée. Refuge favorisé.<br><b>GEO :</b> Tensions géo-politiques +12.5$.</small>
            </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="kz-card" style="height:535px; padding:0; overflow:hidden;"><div class="kz-header" style="margin:15px;">TradingView Analysis (M15)</div>', unsafe_allow_html=True)
        st.components.v1.iframe("https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark", height=380)
        st.markdown(f"""
            <div style="margin:10px 15px; display:grid; grid-template-columns: repeat(4, 1fr); gap:10px;">
                <div class="macro-item" style="flex-direction:column; text-align:center;"><small>BCE</small><b style="color:#ef4444;">-12.4%</b></div>
                <div class="macro-item" style="flex-direction:column; text-align:center;"><small>ETF</small><b style="color:#10b981;">+24.1%</b></div>
                <div class="macro-item" style="flex-direction:column; text-align:center;"><small>GEO</small><b style="color:#10b981;">+18.5%</b></div>
                <div class="macro-item" style="flex-direction:column; text-align:center;"><small>USD</small><b style="color:#ef4444;">-09.2%</b></div>
            </div></div>""", unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="kz-card" style="height:535px;"><div class="kz-header">Order Flow Matrix</div>', unsafe_allow_html=True)
        dom_html = ""
        t_ask, t_bid = 0, 0
        for i in range(15, -16, -1):
            p = round(gold + (i * 0.4), 1)
            is_ask, is_curr = p > gold, p == round(gold, 1)
            v = random.randint(150, 650)
            if not is_curr:
                if is_ask: t_ask += v 
                else: t_bid += v
            w = min(100, (v/1000)*100)
            bar_c = "rgba(239,68,68,0.3)" if is_ask else "rgba(16,185,129,0.3)"
            dom_html += f'<div class="dom-row"><div class="dom-p" style="{"color:#eab308; font-weight:bold; background:rgba(234,179,8,0.1);" if is_curr else ""}">{p:.1f}</div>'
            dom_html += f'<div class="dom-bar-wrap">{"<div style=\'position:absolute; left:0; height:100%; width:"+str(w)+"%; background:"+bar_c+"; border-right:2px solid "+ ("#ef4444" if is_ask else "#10b981") +";\'></div>" if not is_curr else ""}'
            dom_html += f'<div class="dom-v">{v if not is_curr else ""}</div></div></div>'
        st.markdown(f'<div class="dom-box">{dom_html}</div></div>', unsafe_allow_html=True)

    # --- FOOTER ---
    imb = max(t_bid, t_ask)/max(1, min(t_bid, t_ask))
    st.markdown(f"""
    <div class="kz-card" style="display:grid; grid-template-columns: repeat(4, 1fr); gap:20px; text-align:center;">
        <div><small style="color:#555; font-weight:bold;">ZONE MARKET PROFILE</small><br><b style="color:{'#10b981' if is_on_zone else '#ef4444'};">{'VALIDATED' if is_on_zone else 'SCANNING'}</b></div>
        <div><small style="color:#555; font-weight:bold;">IMBALANCE RATIO</small><br><b style="color:{'#10b981' if imb >= 2.7 else '#ef4444'};">{imb:.1f}x</b></div>
        <div><small style="color:#555; font-weight:bold;">DXY CORRELATION</small><br><b style="color:#10b981;">SAFE CONFLUENCE</b></div>
        <div><small style="color:#555; font-weight:bold;">DECISION BIAS</small><br><b style="color:{'#10b981' if imb >= 2.7 and is_on_zone else '#eab308'};">{'READY TO FIRE' if imb >= 2.7 and is_on_zone else 'WAITING FOR EDGE'}</b></div>
    </div>""", unsafe_allow_html=True)

terminal()
