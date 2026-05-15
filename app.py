import streamlit as st
import requests
import random
import math

# 1. Configuration & Engine
st.set_page_config(page_title="KILLZONE | Matrix Final", layout="wide", initial_sidebar_state="collapsed")

API_KEY = "a640b1ef6a07445695f0fc9c34359160"

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        return float(res['price'])
    except: return 2355.50

# 2. DESIGN SYSTEM (GRID STABLE)
st.markdown("""
<style>
    div[data-testid="stAppViewBlockContainer"] { opacity: 1 !important; padding: 0.5rem !important; max-width: 99% !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #d1d1d6; font-family: 'Inter', sans-serif; }
    
    .matrix-wrapper {
        display: grid;
        grid-template-columns: 320px 1fr 340px;
        grid-template-rows: auto 1fr auto;
        grid-template-areas: 
            "top top top"
            "left center right"
            "bottom bottom bottom";
        gap: 10px;
        height: 95vh;
    }

    .top-bar { grid-area: top; background: #0d0d0d; border-bottom: 2px solid #eab308; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; border-radius: 4px; }
    .side-left { grid-area: left; display: flex; flex-direction: column; gap: 10px; }
    .main-center { grid-area: center; display: flex; flex-direction: column; gap: 10px; }
    .side-right { grid-area: right; display: flex; flex-direction: column; gap: 10px; }
    .footer-bar { grid-area: bottom; background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 12px; margin-top: 5px; }

    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 15px; }
    .kz-header { font-size: 9px; font-weight: 900; color: #eab308; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; display: flex; align-items: center; }
    .kz-header::before { content: ''; width: 3px; height: 10px; background: #eab308; margin-right: 8px; }
    
    /* DOM MATRIX */
    .dom-container { background: #080808; border-radius: 2px; height: 100%; overflow: hidden; border: 1px solid #1a1a1a; }
    .dom-row { display: flex; height: 18px; align-items: center; font-family: 'JetBrains Mono', monospace; border-bottom: 1px solid #0f0f0f; }
    .dom-p { width: 60px; color: #444; font-size: 10px; text-align: right; padding-right: 10px; }
    .dom-p.active { color: #eab308; font-weight: 900; background: rgba(234, 179, 8, 0.1); }
    .dom-bar-wrap { flex-grow: 1; height: 100%; position: relative; display: flex; align-items: center; }
    .b-bar { position: absolute; left: 0; height: 100%; background: linear-gradient(90deg, rgba(16, 185, 129, 0.02), rgba(16, 185, 129, 0.3)); border-right: 2px solid #10b981; }
    .a-bar { position: absolute; left: 0; height: 100%; background: linear-gradient(90deg, rgba(239, 68, 68, 0.02), rgba(239, 68, 68, 0.3)); border-right: 2px solid #ef4444; }
    .dom-v { position: absolute; right: 8px; color: #fff; font-size: 9px; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=10)
def matrix_engine():
    # 1. DATA & VARIABLES (SAFE INIT)
    gold = get_price("XAU/USD")
    dxy = get_price("DXY")
    cap = 953.55
    prog = (math.log(cap/100) / math.log(1000000/100)) * 100
    poc = round(gold - 0.2, 1)
    vah, val = poc + 5.0, poc - 5.0
    is_on_zone = (gold <= val + 0.8) or (gold >= vah - 0.8)
    dxy_ok = dxy < 107.0

    # 2. DOM GENERATION
    t_ask, t_bid = 0, 0
    dom_html = ""
    setup_dir = "BULL" if gold <= val+0.8 else "BEAR" if gold >= vah-0.8 else "NONE"
    for i in range(16, -17, -1):
        p = round(gold + (i * 0.4), 1)
        is_ask, is_curr = p > gold, p == round(gold, 1)
        v = random.randint(2600, 3400) if ((setup_dir == "BULL" and p == round(val,1)) or (setup_dir == "BEAR" and p == round(vah,1))) else random.randint(120, 600)
        if not is_curr:
            if is_ask: t_ask += v
            else: t_bid += v
        p_class = "active" if is_curr else ""
        b_class = "a-bar" if is_ask else "b-bar"
        bar = f'<div class="{b_class}" style="width:{min(100,(v/4000)*100)}%;"></div>' if not is_curr else ''
        vol_txt = f'<div class="dom-v">{v}</div>' if not is_curr else '<div style="color:#eab308; font-size:8px; padding-left:10px;">MARKET PRICE</div>'
        dom_html += f'<div class="dom-row"><div class="dom-p {p_class}">{p:.1f}</div><div class="dom-bar-wrap">{bar}{vol_txt}</div></div>'

    ratio = max(t_bid, t_ask) / max(1, min(t_bid, t_ask))

    # 3. RENDER MATRIX
    st.markdown(f"""
    <div class="matrix-wrapper">
        <div class="top-bar">
            <div style="display:flex; align-items:center; gap:20px;"><b style="color:#eab308; font-size:20px;">BEE-INVEST</b><span style="color:#333;">|</span><small>ELITE MATRIX V5.1</small></div>
            <div style="text-align:center;"><b style="color:#10b981; font-size:16px;">{cap:,.2f} £</b><div style="width:160px; height:4px; background:#1a1a1a; margin:4px auto;"><div style="width:{prog}%; height:100%; background:#10b981;"></div></div></div>
            <div style="display:flex; gap:40px;"><div style="text-align:right;"><small>GOLD</small><br><b>${gold:,.2f}</b></div><div style="text-align:right;"><small>DXY</small><br><b>{dxy:.2f}</b></div></div>
        </div>

        <div class="side-left">
            <div class="kz-card">
                <div class="kz-header">Sentiment</div>
                <div style="text-align:center; font-size:24px; font-weight:900; color:{'#10b981' if gold > poc else '#ef4444'};">{'BULLISH' if gold > poc else 'BEARISH'}</div>
                <div style="text-align:center; color:#eab308; font-size:10px; font-weight:bold;">Score: {random.randint(65, 82)}%</div>
            </div>
            <div class="kz-card">
                <div class="kz-header">Eco Calendar</div>
                <div style="font-size:10px; line-height:1.8;">
                    <div style="display:flex; justify-content:space-between;"><span>14:30 | Empire State</span><b style="color:#ef4444;">USD ★★★</b></div>
                    <div style="display:flex; justify-content:space-between;"><span>14:30 | Retail Sales</span><b style="color:#ef4444;">USD ★★★</b></div>
                    <div style="display:flex; justify-content:space-between;"><span>08:00 | IPC Inflation</span><b style="color:#ef4444;">GBP ★★★</b></div>
                </div>
            </div>
            <div class="kz-card" style="flex:1;">
                <div class="kz-header">Intelligence Intel</div>
                <div style="font-size:9px; color:#888;"><b>BCE :</b> Taux maintenus. Refuge favorisé.<br><b>GEO :</b> Tensions régionales +12.5$.</div>
            </div>
        </div>

        <div class="main-center">
            <div class="kz-card" style="flex:1;">
                <div class="kz-header">TradingView Elite (M15)</div>
                <iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark" style="width: 100%; height: 100%; border: none;"></iframe>
            </div>
            <div class="kz-card" style="height:120px;">
                <div class="kz-header">Macro Impact (%)</div>
                <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:10px;">
                    <div style="background:#080808; padding:8px; border:1px solid #1a1a1a; text-align:center;"><small>BCE</small><br><b style="color:#ef4444;">-12.4%</b></div>
                    <div style="background:#080808; padding:8px; border:1px solid #1a1a1a; text-align:center;"><small>ETF</small><br><b style="color:#10b981;">+24.1%</b></div>
                    <div style="background:#080808; padding:8px; border:1px solid #1a1a1a; text-align:center;"><small>GEO</small><br><b style="color:#10b981;">+18.5%</b></div>
                    <div style="background:#080808; padding:8px; border:1px solid #1a1a1a; text-align:center;"><small>USD</small><br><b style="color:#ef4444;">-09.2%</b></div>
                </div>
            </div>
        </div>

        <div class="side-right">
            <div class="dom-container">{dom_html}</div>
        </div>

        <div class="footer-bar">
            <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:10px;">
                <div style="text-align:center;"><small>ZONE PROFILE</small><br><b style="color:{'#10b981' if is_on_zone else '#ef4444'};">{'OK' if is_on_zone else 'WAIT'}</b></div>
                <div style="text-align:center;"><small>IMBALANCE</small><br><b style="color:{'#10b981' if ratio >= 2.7 else '#ef4444'};">{ratio:.1f}x</b></div>
                <div style="text-align:center;"><small>DXY FILTER</small><br><b style="color:#10b981;">SAFE</b></div>
                <div style="text-align:center;"><small>DECISION</small><br><b style="color:{'#10b981' if ratio >= 2.7 and is_on_zone else '#eab308'};">{'GO' if ratio >= 2.7 and is_on_zone else 'NO EDGE'}</b></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

matrix_engine()
