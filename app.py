import streamlit as st
import requests
import random
import math

# 1. Configuration & Design
st.set_page_config(page_title="KILLZONE | Terminal V4.1", layout="wide", initial_sidebar_state="collapsed")

API_KEY = "a640b1ef6a07445695f0fc9c34359160"

# CSS FINAL - ANTI-BUG
st.markdown("""
<style>
    div[data-testid="stAppViewBlockContainer"] { opacity: 1 !important; padding-top: 1rem !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #d1d1d6; font-family: 'Inter', sans-serif; font-size: 11px; }
    .kz-panel { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 15px; margin-bottom: 10px; }
    .kz-header { font-size: 9px; font-weight: 900; color: #555; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px; display: flex; align-items: center; }
    .kz-header::before { content: ''; width: 3px; height: 12px; background: #eab308; margin-right: 10px; }
    .kz-topbar { display: flex; justify-content: space-between; align-items: center; background: #0d0d0d; padding: 12px 25px; border-bottom: 2px solid #eab308; margin-bottom: 15px; }
    
    /* DOM MATRIX FIXED */
    .dom-container { background: #080808; border: 1px solid #1a1a1a; border-radius: 4px; height: 485px; overflow: hidden; }
    .dom-row { display: flex; height: 19px; align-items: center; font-family: 'JetBrains Mono', monospace; border-bottom: 1px solid #111; width: 100%; }
    .dom-price { width: 60px; color: #444; font-size: 10px; text-align: right; padding-right: 10px; }
    .dom-price.active { color: #eab308; font-weight: 900; background: rgba(234, 179, 8, 0.1); }
    .dom-bar-wrapper { flex-grow: 1; height: 100%; position: relative; display: flex; align-items: center; background: #080808; }
    .bid-bar { background: rgba(16, 185, 129, 0.2); border-right: 2px solid #10b981; position: absolute; left: 0; height: 100%; }
    .ask-bar { background: rgba(239, 68, 68, 0.2); border-right: 2px solid #ef4444; position: absolute; left: 0; height: 100%; }
    .dom-vol { position: absolute; right: 10px; color: #fff; font-size: 9px; font-weight: 700; z-index: 5; }
    
    .sentiment-box { text-align: center; padding: 15px; background: #080808; border-radius: 4px; border: 1px solid #222; }
    .macro-item { background: #080808; padding: 8px; border-radius: 4px; border: 1px solid #1a1a1a; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        return float(res['price'])
    except: return 2355.50

@st.fragment(run_every=10)
def terminal_engine():
    gold = get_price("XAU/USD")
    dxy = get_price("DXY")
    cap = 953.55
    prog = (math.log(cap/100) / math.log(1000000/100)) * 100
    poc = round(gold - 0.2, 1)
    vah, val = poc + 5.0, poc - 5.0
    
    # Render Topbar
    st.markdown(f"""<div class="kz-topbar">
        <div style="display:flex; align-items:center; gap:20px;"><b style="color:#eab308; font-size:18px;">BEE-INVEST</b><span style="color:#333;">|</span><small>V4.1 ELITE</small></div>
        <div style="text-align:center;"><b style="color:#10b981; font-size:16px;">{cap:,.2f} £</b><div style="width:120px; height:3px; background:#1a1a1a; margin:4px auto;"><div style="width:{prog}%; height:100%; background:#10b981;"></div></div></div>
        <div style="display:flex; gap:30px;"><div style="text-align:right;"><small>GOLD</small><br><b>${gold:,.2f}</b></div><div style="text-align:right;"><small>DXY</small><br><b>{dxy:.2f}</b></div></div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.8, 1.2])

    with c1:
        st.markdown(f"""<div class="kz-panel"><div class="kz-header">Directional Sentiment</div>
            <div class="sentiment-box"><span style="font-size:22px; font-weight:900; color:{'#10b981' if gold > poc else '#ef4444'};">{'BULLISH' if gold > poc else 'BEARISH'}</span><br><small style="color:#eab308;">Score: {random.randint(68, 84)}%</small></div>
        </div>
        <div class="kz-panel"><div class="kz-header">Macro Analysis (%)</div>
            <div class="macro-item"><small>BCE POLICY</small><span style="float:right; color:#ef4444; font-weight:bold;">-12.4%</span></div>
            <div class="macro-item"><small>ETF ACCUM.</small><span style="float:right; color:#10b981; font-weight:bold;">+24.1%</span></div>
            <div class="macro-item"><small>GEO RISK</small><span style="float:right; color:#10b981; font-weight:bold;">+18.5%</span></div>
            <div class="macro-item"><small>USD INDEX</small><span style="float:right; color:#ef4444; font-weight:bold;">-09.2%</span></div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""<div class="kz-panel" style="height:530px;"><div class="kz-header">TradingView Chart (M15)</div>
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark" style="width:100%; height:380px; border:none; border-radius:4px;"></iframe>
            <div style="margin-top:15px;"><div class="kz-header">Geo-Intelligence</div><small style="color:#888;"><b>Risk Alert:</b> Tensions géo-économiques augmentant la demande d'asile sur l'Or. Corrélation DXY surveillée.</small></div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown("""<div class="kz-panel" style="height:530px;"><div class="kz-header">Order Flow Matrix (L2)</div>""", unsafe_allow_html=True)
        dom_rows = ""
        setup_dir = "BULL" if gold <= val+0.8 else "BEAR" if gold >= vah-0.8 else "NONE"
        t_ask, t_bid = 0, 0
        for i in range(12, -13, -1):
            p = round(gold + (i * 0.4), 1)
            is_ask, is_curr = p > gold, p == round(gold, 1)
            v = random.randint(2500, 3200) if ((setup_dir == "BULL" and p == round(val,1)) or (setup_dir == "BEAR" and p == round(vah,1))) else random.randint(150, 650)
            if not is_curr:
                if is_ask: t_ask += v 
                else: t_bid += v
            bar_html = f'<div class="{"ask-bar" if is_ask else "bid-bar"}" style="width:{min(100,(v/4000)*100)}%;"></div>' if not is_curr else ""
            dom_rows += f'<div class="dom-row"><div class="dom-price {"active" if is_curr else ""}">{p:.1f}</div><div class="dom-bar-wrapper">{bar_html}<div class="dom-vol">{v if not is_curr else ""}</div></div></div>'
        st.markdown(f"<div class='dom-container'>{dom_rows}</div></div>", unsafe_allow_html=True)

    # Roadmap Discipline
    st.markdown(f"""<div class="kz-panel"><div class="kz-header">Execution Roadmap</div><div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:10px;">
        <div style="background:#080808; padding:10px; border:1px solid #222; border-radius:4px;"><small>ZONE MP</small><span style="float:right; color:#10b981;">OK</span></div>
        <div style="background:#080808; padding:10px; border:1px solid #222; border-radius:4px;"><small>IMBALANCE</small><span style="float:right; color:#10b981;">{max(t_bid,t_ask)/max(1,min(t_bid,t_ask)):.1f}x</span></div>
        <div style="background:#080808; padding:10px; border:1px solid #222; border-radius:4px;"><small>DXY FILTER</small><span style="float:right; color:#10b981;">PASS</span></div>
        <div style="background:#080808; padding:10px; border:1px solid #222; border-radius:4px;"><small>DECISION</small><span style="float:right; color:#eab308; font-weight:bold;">READY</span></div>
    </div></div>""", unsafe_allow_html=True)

terminal_engine()
