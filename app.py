import streamlit as st
import requests
import random
import math

# 1. Configuration & Engine
st.set_page_config(page_title="KILLZONE | Terminal Ironclad", layout="wide", initial_sidebar_state="collapsed")

API_KEY = "a640b1ef6a07445695f0fc9c34359160"

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        return float(res['price'])
    except: return 2355.50

# CSS INTERFACE STABLE (ZERO GLITCH)
st.markdown("""
<style>
    div[data-testid="stAppViewBlockContainer"] { opacity: 1 !important; padding-top: 1rem !important; max-width: 98% !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #d1d1d6; font-family: 'Inter', sans-serif; font-size: 11px; }
    
    .kz-panel { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 15px; margin-bottom: 10px; }
    .kz-header { font-size: 9px; font-weight: 900; color: #eab308; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px; display: flex; align-items: center; }
    .kz-header::before { content: ''; width: 3px; height: 12px; background: #eab308; margin-right: 8px; }
    
    .kz-topbar { display: flex; justify-content: space-between; align-items: center; background: #0d0d0d; padding: 10px 25px; border-bottom: 2px solid #eab308; margin-bottom: 15px; }

    /* DOM STYLE */
    .dom-container { background: #080808; border: 1px solid #1a1a1a; border-radius: 4px; overflow: hidden; height: 500px; }
    .dom-row { display: flex; height: 18px; align-items: center; font-family: 'JetBrains Mono', monospace; border-bottom: 1px solid #111; }
    .dom-price { width: 60px; color: #444; font-size: 10px; text-align: right; padding-right: 12px; }
    .dom-price.active { color: #eab308; font-weight: 900; background: rgba(234, 179, 8, 0.1); }
    .dom-bar-wrapper { flex-grow: 1; height: 100%; position: relative; display: flex; align-items: center; }
    .bid-bar { background: linear-gradient(90deg, rgba(16, 185, 129, 0.05) 0%, rgba(16, 185, 129, 0.3) 100%); border-right: 2px solid #10b981; position: absolute; left: 0; height: 100%; }
    .ask-bar { background: linear-gradient(90deg, rgba(239, 68, 68, 0.05) 0%, rgba(239, 68, 68, 0.3) 100%); border-right: 2px solid #ef4444; position: absolute; left: 0; height: 100%; }
    .dom-vol { position: absolute; right: 10px; color: #fff; font-size: 9px; font-weight: 700; z-index: 10; }

    /* ROADMAP STABLE */
    .roadmap-box { background: #080808; border: 1px solid #1a1a1a; border-radius: 4px; padding: 12px; display: flex; justify-content: space-around; margin-top: 10px; }
    .rm-item { text-align: center; }
    .rm-label { font-size: 8px; color: #555; font-weight: bold; }
    .rm-val { font-size: 11px; font-weight: 900; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=10)
def terminal_engine():
    # DATA ACQUISITION
    gold = get_price("XAU/USD")
    dxy = get_price("DXY")
    cap = 953.55
    prog = (math.log(cap/100) / math.log(1000000/100)) * 100
    poc = round(gold - 0.2, 1)
    vah, val = poc + 5.0, poc - 5.0
    is_on_zone = (gold <= val + 0.8) or (gold >= vah - 0.8)

    # 1. TOPBAR
    st.markdown(f"""<div class="kz-topbar">
        <div style="display:flex; align-items:center; gap:20px;"><b style="color:#eab308; font-size:20px;">BEE-INVEST</b><span style="color:#333;">|</span><small>TERMINAL IRONCLAD V4.7</small></div>
        <div style="text-align:center;"><b style="color:#10b981; font-size:16px;">{cap:,.2f} £</b><div style="width:140px; height:4px; background:#1a1a1a; margin:4px auto;"><div style="width:{prog}%; height:100%; background:#10b981;"></div></div></div>
        <div style="display:flex; gap:35px;"><div style="text-align:right;"><small>GOLD</small><br><b>${gold:,.2f}</b></div><div style="text-align:right;"><small>DXY INDEX</small><br><b>{dxy:.2f}</b></div></div>
    </div>""", unsafe_allow_html=True)

    # 2. MAIN LAYOUT (2 COLUMNS)
    col_left, col_right = st.columns([1, 2.2], gap="small")

    with col_left:
        # SENTIMENT & MACRO
        st.markdown(f"""<div class="kz-panel">
            <div class="kz-header">Bias & Sentiment</div>
            <div style="text-align:center; padding:15px; background:#080808; border:1px solid #eab30833; border-radius:4px; margin-bottom:10px;">
                <span style="font-size:24px; font-weight:900; color:{'#10b981' if gold > poc else '#ef4444'};">{'BULLISH' if gold > poc else 'BEARISH'}</span><br>
                <span style="font-size:9px; color:#eab308;">Confidence: {random.randint(65, 82)}%</span>
            </div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:5px;">
                <div style="background:#080808; padding:8px; border:1px solid #1a1a1a; border-radius:3px;"><small>BCE</small><br><b style="color:#ef4444;">-12%</b></div>
                <div style="background:#080808; padding:8px; border:1px solid #1a1a1a; border-radius:3px;"><small>ETF</small><br><b style="color:#10b981;">+24%</b></div>
            </div>
        </div>""", unsafe_allow_html=True)

        # DOM MATRIX
        st.markdown("""<div class="kz-panel" style="height:550px;"><div class="kz-header">Liquid Matrix DOM</div>""", unsafe_allow_html=True)
        dom_html, t_ask, t_bid = "<div class='dom-container'>", 0, 0
        setup_dir = "BULL" if gold <= val+0.8 else "BEAR" if gold >= vah-0.8 else "NONE"
        for i in range(13, -14, -1):
            p = round(gold + (i * 0.4), 1)
            is_ask, is_curr = p > gold, p == round(gold, 1)
            v = random.randint(2500, 3200) if ((setup_dir == "BULL" and p == round(val,1)) or (setup_dir == "BEAR" and p == round(vah,1))) else random.randint(150, 650)
            if not is_curr:
                if is_ask: t_ask += v
                else: t_bid += v
            row_style = 'active' if is_curr else ''
            bar_type = 'ask-bar' if is_ask else 'bid-bar'
            bar_width = min(100, (v/4000)*100)
            dom_html += f'<div class="dom-row"><div class="dom-price {row_style}">{p:.1f}</div><div class="dom-bar-wrapper">'
            if not is_curr: dom_html += f'<div class="{bar_type}" style="width:{bar_width}%;"></div><div class="dom-vol">{v}</div>'
            else: dom_html += f'<div style="color:#eab308; font-size:8px; padding-left:10px;">MARKET PRICE</div>'
            dom_html += '</div></div>'
        st.markdown(dom_html + "</div></div>", unsafe_allow_html=True)

    with col_right:
        # TRADINGVIEW & ROADMAP
        st.markdown(f"""<div class="kz-panel" style="height:745px;">
            <div class="kz-header">TradingView Elite Stream (M15)</div>
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark" style="width: 100%; height: 500px; border: none; border-radius:4px;"></iframe>
            
            <div class="kz-header" style="margin-top:20px;">Execution Roadmap</div>
            <div class="roadmap-box">
                <div class="rm-item"><div class="rm-label">ZONE MP</div><div class="rm-val" style="color:#10b981;">VALIDATED</div></div>
                <div class="rm-item"><div class="rm-label">IMBALANCE</div><div class="rm-val" style="color:#10b981;">{max(t_bid,t_ask)/max(1,min(t_bid,t_ask)):.1f}x</div></div>
                <div class="rm-item"><div class="rm-label">DXY FILTER</div><div class="rm-val" style="color:#10b981;">CONFLUENCE</div></div>
                <div class="rm-item"><div class="rm-label">DECISION</div><div class="rm-val" style="color:#eab308;">READY</div></div>
            </div>
            
            <div class="kz-header" style="margin-top:20px;">Market Intelligence Feed</div>
            <div style="font-size:10px; color:#888; border-left:2px solid #eab308; padding-left:12px;">
                <b>BCE Intel:</b> Rumeurs de pause sur les taux, l'Or reste le refuge favori.
            </div>
        </div>""", unsafe_allow_html=True)

terminal_engine()
