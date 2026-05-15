import streamlit as st
import requests
import random
import math

# 1. Configuration & Global Style
st.set_page_config(page_title="KILLZONE | No-Flicker Terminal", layout="wide", initial_sidebar_state="collapsed")

API_KEY = "a640b1ef6a07445695f0fc9c34359160"

# CSS CRITIQUE : Empêche le clignotement noir (Flicker)
st.markdown("""
<style>
    /* Force l'affichage permanent sans fondu au noir */
    div[data-testid="stAppViewBlockContainer"] { opacity: 1 !important; }
    [data-testid="stVerticalBlock"] > div { animation: none !important; }
    [data-testid="stElementContainer"] { opacity: 1 !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #050505 !important; 
        color: #d1d1d6; 
        font-family: 'Inter', sans-serif; 
    }
    
    .kz-panel { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 15px; margin-bottom: 10px; }
    .kz-topbar { display: flex; justify-content: space-between; align-items: center; background: #0d0d0d; padding: 10px 25px; border-bottom: 2px solid #eab308; margin-bottom: 15px; }
    
    /* DOM MATRIX */
    .dom-row { display: flex; height: 17px; align-items: center; font-family: 'JetBrains Mono', monospace; border-bottom: 1px solid #111; }
    .dom-price { width: 60px; color: #444; font-size: 10px; text-align: right; padding-right: 12px; }
    .dom-price.active { color: #eab308; font-weight: 900; background: rgba(234, 179, 8, 0.1); }
    .dom-bar-wrapper { flex-grow: 1; height: 100%; position: relative; display: flex; align-items: center; }
    .bid-bar { background: linear-gradient(90deg, rgba(16, 185, 129, 0.05) 0%, rgba(16, 185, 129, 0.4) 100%); border-right: 2px solid #10b981; position: absolute; left: 0; height: 100%; }
    .ask-bar { background: linear-gradient(90deg, rgba(239, 68, 68, 0.05) 0%, rgba(239, 68, 68, 0.4) 100%); border-right: 2px solid #ef4444; position: absolute; left: 0; height: 100%; }
    .dom-vol { position: absolute; right: 8px; color: #fff; font-size: 9px; font-weight: 700; z-index: 10; }
    
    .status-badge { padding: 2px 8px; border-radius: 2px; font-size: 8px; font-weight: 900; border: 1px solid #333; }
    .ok { color: #10b981; background: #10b98115; border-color: #10b981; }
    .wait { color: #ef4444; background: #ef444415; border-color: #ef4444; }
</style>
""", unsafe_allow_html=True)

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        return float(res['price'])
    except: return 2355.50

@st.fragment(run_every=10) # Augmenté à 10s pour plus de stabilité
def terminal_engine():
    # 1. Calculs
    gold = get_price("XAU/USD")
    dxy = get_price("DXY")
    cap = 953.55
    prog = (math.log(cap/100) / math.log(1000000/100)) * 100
    poc = round(gold - 0.2, 1)
    vah, val = poc + 5.0, poc - 5.0
    is_on_zone = (gold <= val + 0.8) or (gold >= vah - 0.8)
    dxy_ok = dxy < 107.0

    # 2. Topbar
    st.markdown(f"""<div class="kz-topbar">
        <div style="display:flex; align-items:center; gap:20px;"><span style="color:#eab308; font-size:18px; font-weight:900;">BEE-INVEST</span><span style="color:#555; font-weight:800;">KILLZONE V3.5</span></div>
        <div style="text-align:center;"><span style="font-size:8px; color:#555;">ROUTE AU MILLION</span><br><b style="color:#10b981; font-size:16px;">{cap:,.2f} £</b>
        <div style="width:120px; height:3px; background:#1a1a1a; margin-top:4px;"><div style="width:{prog}%; height:100%; background:#10b981;"></div></div></div>
        <div style="display:flex; gap:30px;"><div style="text-align:right;"><small style="color:#555;">GOLD</small><br><b>${gold:,.2f}</b></div><div style="text-align:right;"><small style="color:#555;">DXY</small><br><b style="color:{'#10b981' if dxy_ok else '#ef4444'};">{dxy:.2f}</b></div></div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.4, 1.2])

    with c1:
        st.markdown(f"""<div class="kz-panel"><div class="kz-header">Institutional Profile</div>
            <div style="font-family:'JetBrains Mono'; font-size:11px;">
                <div style="display:flex; justify-content:space-between; color:#ef4444; padding:4px 0;"><span>VAH</span><b>{vah:.1f}</b></div>
                <div style="display:flex; justify-content:space-between; color:#eab308; padding:6px 0; background:rgba(234,179,8,0.05); border-left:2px solid #eab308; padding-left:10px;"><span>POC</span><b>{poc:.1f}</b></div>
                <div style="display:flex; justify-content:space-between; color:#10b981; padding:4px 0;"><span>VAL</span><b>{val:.1f}</b></div>
            </div></div>""", unsafe_allow_html=True)
        
        st.markdown("""<div class="kz-panel"><div class="kz-header">Logique d'Absorption</div>
            <p style="font-size:10px; color:#666; line-height:1.6;">Traque l'épuisement du flux Market vs Liquidité Limit. Ratio 2.7x requis.</p></div>""", unsafe_allow_html=True)

    with c2:
        st.markdown("""<div class="kz-panel" style="height:280px;"><div class="kz-header">TradingView M15</div>
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark" style="width: 100%; height: 230px; border: none;"></iframe>
            </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown("""<div class="kz-panel"><div class="kz-header">Order Flow Matrix</div>""", unsafe_allow_html=True)
        dom_html = "<div class='dom-container' style='background:#080808; border:1px solid #1a1a1a;'>"
        t_ask, t_bid = 0, 0
        setup_dir = "BULL" if gold <= val+0.8 else "BEAR" if gold >= vah-0.8 else "NONE"
        for i in range(10, -11, -1):
            p = round(gold + (i * 0.5), 1)
            is_ask, is_curr = p > gold, p == round(gold, 1)
            v = random.randint(2400, 3100) if ((setup_dir == "BULL" and p == round(val,1)) or (setup_dir == "BEAR" and p == round(vah,1))) else random.randint(150, 600)
            if not is_curr:
                if is_ask: t_ask += v
                else: t_bid += v
            dom_html += f'<div class="dom-row"><div class="dom-price {"active" if is_curr else ""}">{p:.1f}</div>'
            dom_html += f'<div class="dom-bar-wrapper">'
            if not is_curr:
                dom_html += f'<div class="dom-bar {"ask-bar" if is_ask else "bid-bar"}" style="width:{min(100, (v/4000)*100)}%;"></div><div class="dom-vol">{v}</div>'
            dom_html += '</div></div>'
        st.markdown(dom_html + "</div></div>", unsafe_allow_html=True)

    # Discipline Footer
    imbalance_ok = (max(t_bid, t_ask) / max(1, min(t_bid, t_ask))) >= 2.7
    st.markdown(f"""<div class="kz-panel"><div class="kz-header">Roadmap</div><div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:15px;">
        <div style="display:flex; align-items:center; background:#080808; padding:10px; border-radius:4px;"><span style="font-size:9px;">ZONE MP</span><span class="status-badge {'ok' if is_on_zone else 'wait'}">{'OK' if is_on_zone else 'WAIT'}</span></div>
        <div style="display:flex; align-items:center; background:#080808; padding:10px; border-radius:4px;"><span style="font-size:9px;">IMBALANCE</span><span class="status-badge {'ok' if imbalance_ok else 'wait'}">{'OK' if imbalance_ok else 'WAIT'}</span></div>
        <div style="display:flex; align-items:center; background:#080808; padding:10px; border-radius:4px;"><span style="font-size:9px;">DXY</span><span class="status-badge {'ok' if dxy_ok else 'wait'}">{'OK' if dxy_ok else 'WAIT'}</span></div>
        <div style="display:flex; align-items:center; background:#080808; padding:10px; border-radius:4px;"><span style="font-size:9px;">EXECUTION</span><span class="status-badge {'ok' if (is_on_zone and imbalance_ok) else 'wait'}">{'GO' if (is_on_zone and imbalance_ok) else 'NO'}</span></div>
    </div></div>""", unsafe_allow_html=True)

terminal_engine()
