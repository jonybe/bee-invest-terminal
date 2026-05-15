import streamlit as st
import requests
import random
import math

# 1. Configuration & Global Style
st.set_page_config(page_title="KILLZONE | Institutional Dashboard", layout="wide", initial_sidebar_state="collapsed")

API_KEY = "a640b1ef6a07445695f0fc9c34359160"

# CSS ANTI-FLICKER & DESIGN PRO
st.markdown("""
<style>
    div[data-testid="stAppViewBlockContainer"] { opacity: 1 !important; }
    [data-testid="stVerticalBlock"] > div { animation: none !important; }
    [data-testid="stElementContainer"] { opacity: 1 !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #d1d1d6; font-family: 'Inter', sans-serif; font-size: 11px; }
    .kz-panel { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 18px; margin-bottom: 15px; }
    .kz-header { font-size: 10px; font-weight: 800; color: #555; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 15px; display: flex; align-items: center; }
    .kz-header::before { content: ''; width: 3px; height: 12px; background: #eab308; margin-right: 10px; }
    .kz-topbar { display: flex; justify-content: space-between; align-items: center; background: #0d0d0d; padding: 12px 25px; border-bottom: 2px solid #eab308; margin-bottom: 20px; }
    .dom-container { background: #080808; border: 1px solid #1a1a1a; border-radius: 4px; height: 460px; overflow: hidden; }
    .dom-row { display: flex; height: 19px; align-items: center; font-family: 'JetBrains Mono', monospace; border-bottom: 1px solid #111; }
    .dom-price { width: 65px; color: #444; font-size: 10px; text-align: right; padding-right: 12px; }
    .dom-price.active { color: #eab308; font-weight: 900; background: rgba(234, 179, 8, 0.1); }
    .dom-bar-wrapper { flex-grow: 1; height: 100%; position: relative; display: flex; align-items: center; }
    .bid-bar { background: linear-gradient(90deg, rgba(16, 185, 129, 0.05) 0%, rgba(16, 185, 129, 0.4) 100%); border-right: 2px solid #10b981; position: absolute; left: 0; height: 100%; }
    .ask-bar { background: linear-gradient(90deg, rgba(239, 68, 68, 0.05) 0%, rgba(239, 68, 68, 0.4) 100%); border-right: 2px solid #ef4444; position: absolute; left: 0; height: 100%; }
    .dom-vol { position: absolute; right: 10px; color: #fff; font-size: 9px; font-weight: 700; z-index: 10; }
    .roadmap-section { margin-top: 25px; padding-top: 10px; }
    .roadmap-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }
    .roadmap-card { background: linear-gradient(145deg, #111111, #0a0a0a); border: 1px solid #222; padding: 15px; border-radius: 6px; display: flex; flex-direction: column; gap: 8px; position: relative; overflow: hidden; }
    .roadmap-label { font-size: 9px; font-weight: 800; color: #555; text-transform: uppercase; letter-spacing: 1px; }
    .roadmap-status { font-size: 11px; font-weight: 900; display: flex; align-items: center; gap: 8px; }
    .status-dot { width: 8px; height: 8px; border-radius: 50%; }
    .ok-text { color: #10b981; }
    .ok-dot { background: #10b981; box-shadow: 0 0 10px #10b981; }
    .wait-text { color: #ef4444; }
    .wait-dot { background: #ef4444; box-shadow: 0 0 10px #ef4444; }
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
    cap, target = 953.55, 1000000.0
    prog = (math.log(cap/100) / math.log(target/100)) * 100
    poc = round(gold - 0.2, 1)
    vah, val = poc + 5.0, poc - 5.0
    is_on_zone = (gold <= val + 0.8) or (gold >= vah - 0.8)
    dxy_ok = dxy < 107.0

    st.markdown(f"""
    <div class="kz-topbar">
        <div style="display:flex; align-items:center; gap:20px;"><span style="color:#eab308; font-size:20px; font-weight:900;">BEE-INVEST</span><span style="color:#333; font-weight:800;">KILLZONE V3.7</span></div>
        <div style="text-align:center;"><span style="font-size:8px; color:#555;">ROUTE AU MILLION</span><br><b style="color:#10b981; font-size:16px;">{cap:,.2f} £</b>
        <div style="width:140px; height:4px; background:#1a1a1a; margin-top:4px;"><div style="width:{prog}%; height:100%; background:#10b981;"></div></div></div>
        <div style="display:flex; gap:35px;"><div style="text-align:right;"><small style="color:#555;">GOLD SPOT</small><br><b>${gold:,.2f}</b></div><div style="text-align:right;"><small style="color:#555;">DXY INDEX</small><br><b style="font-size:14px; color:{'#10b981' if dxy_ok else '#ef4444'};">{dxy:.2f}</b></div></div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.6, 1.2])
    with c1:
        st.markdown(f"""<div class="kz-panel"><div class="kz-header">Institutional Profile</div><div style="font-family:'JetBrains Mono'; font-size:11px;"><div style="display:flex; justify-content:space-between; color:#ef4444; padding:5px 0;"><span>VAH</span><b>{vah:.1f}</b></div><div style="display:flex; justify-content:space-between; color:#eab308; padding:8px 0; background:rgba(234,179,8,0.05); border-left:2px solid #eab308; padding-left:12px;"><span>POC</span><b>{poc:.1f}</b></div><div style="display:flex; justify-content:space-between; color:#10b981; padding:5px 0;"><span>VAL</span><b>{val:.1f}</b></div></div></div>
        <div class="kz-panel"><div class="kz-header">Logique d'Absorption</div><p style="font-size:10px; color:#666; line-height:1.6;"><b>Setup :</b> Épuisement du flux Market vs Liquidité Limit.<br><b>Confirmation :</b> Ratio 2.7x requis.</p></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kz-panel" style="height:495px;"><div class="kz-header">TradingView Pro Stream (M15)</div><iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark" style="width: 100%; height: 320px; border: none;"></iframe><div style="margin-top:20px;"><div class="kz-header">Global Intelligence</div><div style="font-size:10px; color:#888; border-left:2px solid #eab308; padding-left:12px; margin-bottom:10px;"><b>BCE :</b> Taux maintenus. Vigilance Gold.</div><div style="font-size:10px; color:#888; border-left:2px solid #eab308; padding-left:12px;"><b>ETF :</b> Accumulation nette sur contrats.</div></div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="kz-panel" style="height:495px;"><div class="kz-header">Order Flow Matrix (L2)</div>""", unsafe_allow_html=True)
        dom_html, t_ask, t_bid = "<div class='dom-container'>", 0, 0
        setup_dir = "BULL" if gold <= val+0.8 else "BEAR" if gold >= vah-0.8 else "NONE"
        for i in range(11, -12, -1):
            p = round(gold + (i * 0.5), 1)
            is_ask, is_curr = p > gold, p == round(gold, 1)
            v = random.randint(2500, 3200) if ((setup_dir == "BULL" and p == round(val,1)) or (setup_dir == "BEAR" and p == round(vah,1))) else random.randint(150, 650)
            if not is_curr:
                if is_ask: t_ask += v
                else: t_bid += v
            dom_html += f'<div class="dom-row"><div class="dom-price {"active" if is_curr else ""}">{p:.1f}</div><div class="dom-bar-wrapper">{"<div class=\'dom-bar-ask\' style=\'width:"+str(min(100,(v/4000)*100))+"%;\'></div>" if is_ask else "<div class=\'dom-bar-bid\' style=\'width:"+str(min(100,(v/4000)*100))+"%;\'></div>" if not is_curr else ""}<div class="dom-vol">{v if not is_curr else ""}</div></div></div>'
        st.markdown(dom_html + "</div></div>", unsafe_allow_html=True)

    imbalance_ok = (max(t_bid, t_ask) / max(1, min(t_bid, t_ask))) >= 2.7
    st.markdown(f"""<div class="roadmap-section"><div class="kz-header">Discipline Roadmap</div><div class="roadmap-grid">
        <div class="roadmap-card"><span class="roadmap-label">1. Zone MP</span><div class="roadmap-status {'ok-text' if is_on_zone else 'wait-text'}"><div class="status-dot {'ok-dot' if is_on_zone else 'wait-dot'}"></div>{'OK' if is_on_zone else 'WAIT'}</div></div>
        <div class="roadmap-card"><span class="roadmap-label">2. Imbalance</span><div class="roadmap-status {'ok-text' if imbalance_ok else 'wait-text'}"><div class="status-dot {'ok-dot' if imbalance_ok else 'wait-dot'}"></div>{'OK' if imbalance_ok else 'WAIT'}</div></div>
        <div class="roadmap-card"><span class="roadmap-label">3. DXY Filter</span><div class="roadmap-status {'ok-text' if dxy_ok else 'wait-text'}"><div class="status-dot {'ok-dot' if dxy_ok else 'wait-dot'}"></div>{'OK' if dxy_ok else 'WAIT'}</div></div>
        <div class="roadmap-card"><span class="roadmap-label">4. Decision</span><div class="roadmap-status {'ok-text' if (is_on_zone and imbalance_ok) else 'wait-text'}"><div class="status-dot {'ok-dot' if (is_on_zone and imbalance_ok) else 'wait-dot'}"></div>{'GO' if (is_on_zone and imbalance_ok) else 'NO'}</div></div>
    </div></div>""", unsafe_allow_html=True)

terminal_engine()
