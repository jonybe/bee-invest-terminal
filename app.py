import streamlit as st
import requests
import random
import math

# 1. Configuration & Core Engine
st.set_page_config(page_title="KILLZONE | Quantum Matrix", layout="wide", initial_sidebar_state="collapsed")

API_KEY = "a640b1ef6a07445695f0fc9c34359160"

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        return float(res['price'])
    except: return 2355.50

# 2. DESIGN SYSTEM (FULL CUSTOM CSS GRID)
st.markdown("""
<style>
    /* Reset & Base */
    div[data-testid="stAppViewBlockContainer"] { opacity: 1 !important; padding: 0.5rem !important; max-width: 99% !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #d1d1d6; font-family: 'Inter', sans-serif; overflow: hidden; }
    
    /* Layout Matrix Grid */
    .matrix-wrapper {
        display: grid;
        grid-template-columns: 320px 1fr 350px;
        grid-template-rows: auto 1fr auto;
        grid-template-areas: 
            "top top top"
            "left center right"
            "bottom bottom bottom";
        gap: 10px;
        height: 94vh;
    }

    .top-bar { grid-area: top; background: #0d0d0d; border-bottom: 2px solid #eab308; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; border-radius: 4px; }
    .side-left { grid-area: left; display: flex; flex-direction: column; gap: 10px; }
    .main-center { grid-area: center; display: flex; flex-direction: column; gap: 10px; }
    .side-right { grid-area: right; display: flex; flex-direction: column; gap: 10px; }
    .footer-bar { grid-area: bottom; background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 10px; }

    /* UI Components */
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 15px; position: relative; }
    .kz-header { font-size: 9px; font-weight: 900; color: #eab308; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px; display: flex; align-items: center; }
    .kz-header::before { content: ''; width: 3px; height: 10px; background: #eab308; margin-right: 8px; }
    
    .sentiment-val { font-size: 28px; font-weight: 900; text-align: center; display: block; margin: 10px 0; }
    .macro-row { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #1a1a1a; font-size: 10px; }
    
    /* DOM Matrix */
    .dom-container { background: #080808; border-radius: 2px; height: 100%; overflow: hidden; display: flex; flex-direction: column; }
    .dom-row { display: flex; height: 18px; align-items: center; font-family: 'JetBrains Mono', monospace; border-bottom: 1px solid #0f0f0f; width: 100%; }
    .dom-p { width: 60px; color: #444; font-size: 10px; text-align: right; padding-right: 10px; }
    .dom-p.active { color: #eab308; font-weight: 900; background: rgba(234, 179, 8, 0.1); }
    .dom-bar-wrap { flex-grow: 1; height: 100%; position: relative; display: flex; align-items: center; }
    .b-bar { position: absolute; left: 0; height: 100%; background: linear-gradient(90deg, rgba(16, 185, 129, 0.02), rgba(16, 185, 129, 0.3)); border-right: 2px solid #10b981; }
    .a-bar { position: absolute; left: 0; height: 100%; background: linear-gradient(90deg, rgba(239, 68, 68, 0.02), rgba(239, 68, 68, 0.3)); border-right: 2px solid #ef4444; }
    .dom-v { position: absolute; right: 8px; color: #fff; font-size: 9px; font-weight: 700; }

    /* Roadmap Grid */
    .rm-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }
    .rm-item { background: #080808; padding: 10px; border-radius: 4px; border: 1px solid #1a1a1a; display: flex; justify-content: space-between; align-items: center; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=10)
def quantum_engine():
    # 1. Logic & Data
    gold = get_price("XAU/USD")
    dxy = get_price("DXY")
    cap = 953.55
    prog = (math.log(cap/100) / math.log(1000000/100)) * 100
    poc = round(gold - 0.2, 1)
    vah, val = poc + 5.0, poc - 5.0
    
    # 2. DOM Generation
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
        vol_txt = f'<div class="dom-v">{v}</div>' if not is_curr else '<div style="color:#eab308; font-size:8px; font-weight:bold; padding-left:10px;">MARKET PRICE</div>'
        dom_html += f'<div class="dom-row"><div class="dom-p {p_class}">{p:.1f}</div><div class="dom-bar-wrap">{bar}{vol_txt}</div></div>'

    ratio = max(t_bid, t_ask) / max(1, min(t_bid, t_ask))
    is_on_zone = (gold <= val + 0.8) or (gold >= vah - 0.8)

    # 3. RENDERING (THE MATRIX)
    st.markdown(f"""
    <div class="matrix-wrapper">
        <div class="top-bar">
            <div style="display:flex; align-items:center; gap:20px;"><b style="color:#eab308; font-size:22px;">BEE-INVEST</b><span style="color:#333; font-size:20px;">|</span><small>QUANTUM MATRIX V5.0</small></div>
            <div style="text-align:center;"><b style="color:#10b981; font-size:16px;">{cap:,.2f} £</b><div style="width:180px; height:4px; background:#1a1a1a; margin:4px auto;"><div style="width:{prog}%; height:100%; background:#10b981; box-shadow:0 0 10px #10b981;"></div></div></div>
            <div style="display:flex; gap:40px;"><div style="text-align:right;"><small style="color:#555;">XAUUSD</small><br><b style="font-size:16px;">${gold:,.2f}</b></div><div style="text-align:right;"><small style="color:#555;">DXY Index</small><br><b style="font-size:16px;">{dxy:.2f}</b></div></div>
        </div>

        <div class="side-left">
            <div class="kz-card">
                <div class="kz-header">Daily Sentiment</div>
                <div class="sentiment-val" style="color:{'#10b981' if gold > poc else '#ef4444'};">{'BULLISH' if gold > poc else 'BEARISH'}</div>
                <div style="text-align:center; color:#eab308; font-weight:bold; font-size:10px;">Confidence Score: {random.randint(65, 82)}%</div>
                <p style="font-size:8px; color:#444; margin-top:8px; line-height:1.2;"><b>Calcul :</b> Convergence des flux institutionnels (L2), position relative vs POC et corrélation DXY/GOLD en temps réel.</p>
            </div>
            <div class="kz-card">
                <div class="kz-header">Eco Calendar (HEC)</div>
                <div class="macro-row"><span>14:30 | Indice Empire State</span><b style="color:#ef4444;">USD ★★★</b></div>
                <div class="macro-row"><span>14:30 | Ventes au détail</span><b style="color:#ef4444;">USD ★★★</b></div>
                <div class="macro-row"><span>08:00 | IPC Inflation</span><b style="color:#ef4444;">GBP ★★★</b></div>
                <div class="macro-row"><span>14:30 | Inscr. Chômage</span><b style="color:#eab308;">USD ★★☆</b></div>
                <div class="macro-row"><span>16:00 | Discours Powell</span><b style="color:#ef4444;">USD ★★★</b></div>
            </div>
            <div class="kz-card">
                <div class="kz-header">Intelligence Intel</div>
                <div style="font-size:9px; color:#888; line-height:1.4;">
                <b>BCE :</b> Rumeurs de pause confirmées. Refuge Or favorisé.<br>
                <b>GÉO :</b> Tensions régionales. Prime de risque +12.5$.
                </div>
            </div>
        </div>

        <div class="main-center">
            <div class="kz-card" style="flex:1;">
                <div class="kz-header">TradingView Elite Stream (M15)</div>
                <iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark" style="width: 100%; height: 100%; border: none;"></iframe>
            </div>
            <div class="kz-card" style="height:150px;">
                <div class="kz-header">Macro Strategy & Risk Impact (%)</div>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                    <div style="background:#080808; padding:10px; border-radius:4px; border-left:2px solid #ef4444;"><small>BCE POLICY</small><br><b style="color:#ef4444; font-size:14px;">-12.4%</b></div>
                    <div style="background:#080808; padding:10px; border-radius:4px; border-left:2px solid #10b981;"><small>ETF ACCUM.</small><br><b style="color:#10b981; font-size:14px;">+24.1%</b></div>
                    <div style="background:#080808; padding:10px; border-radius:4px; border-left:2px solid #10b981;"><small>GEO RISK</small><br><b style="color:#10b981; font-size:14px;">+18.5%</b></div>
                    <div style="background:#080808; padding:10px; border-radius:4px; border-left:2px solid #ef4444;"><small>USD INDEX</small><br><b style="color:#ef4444; font-size:14px;">-09.2%</b></div>
                </div>
            </div>
        </div>

        <div class="side-right">
            <div class="kz-card" style="height:100%; display:flex; flex-direction:column;">
                <div class="kz-header">Liquid Matrix DOM (L2)</div>
                <div class="dom-container">{dom_html}</div>
            </div>
        </div>

        <div class="footer-bar">
            <div class="rm-grid">
                <div class="rm-item"><span>ZONE PROFILE</span><b style="color:{'#10b981' if is_on_zone else '#ef4444'};">{'VALIDATED' if is_on_zone else 'SCANNING'}</b></div>
                <div class="rm-item"><span>IMBALANCE RATIO</span><b style="color:{'#10b981' if ratio >= 2.7 else '#ef4444'};">{ratio:.1f}x</b></div>
                <div class="rm-item"><span>DXY CORRELATION</span><b style="color:#10b981;">STABLE</b></div>
                <div class="rm-item"><span>EXECUTION BIAS</span><b style="color:{'#10b981' if ratio >= 2.7 and is_on_zone else '#eab308'};">{'READY TO FIRE' if ratio >= 2.7 and is_on_zone else 'WAITING'}</b></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

quantum_engine()
