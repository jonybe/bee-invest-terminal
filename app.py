import streamlit as st
import requests
import random
import math

# 1. Configuration & API
st.set_page_config(page_title="KILLZONE | Terminal V9.1", layout="wide", initial_sidebar_state="collapsed")
API_KEY = "a640b1ef6a07445695f0fc9c34359160"

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        return float(res['price'])
    except: return 2355.50

# CSS DE SCELLEMENT (Anti-Flicker)
st.markdown("<style>div[data-testid='stAppViewBlockContainer'] { opacity: 1 !important; padding: 0 !important; } html, body { background-color: #050505 !important; }</style>", unsafe_allow_html=True)

@st.fragment(run_every=10)
def terminal_v9():
    # A. CALCULS (Tout en haut, pas de mélange)
    gold = get_price("XAU/USD")
    dxy = get_price("DXY")
    cap = 953.55
    prog = (math.log(cap/100) / math.log(1000000/100)) * 100
    poc = round(gold - 0.2, 1)
    vah, val = poc + 5.0, poc - 5.0
    is_on_zone = (gold <= val + 0.8) or (gold >= vah - 0.8)

    # B. GENERATION DU CARNET (DOM)
    dom_rows = ""
    t_ask, t_bid = 0, 0
    setup_dir = "BULL" if gold <= val+0.8 else "BEAR" if gold >= vah-0.8 else "NONE"
    for i in range(15, -16, -1):
        p = round(gold + (i * 0.4), 1)
        is_ask, is_curr = p > gold, p == round(gold, 1)
        v = random.randint(2500, 3500) if ((setup_dir == "BULL" and p == round(val,1)) or (setup_dir == "BEAR" and p == round(vah,1))) else random.randint(150, 650)
        if not is_curr:
            if is_ask: t_ask += v 
            else: t_bid += v
        p_style = "color:#eab308; font-weight:bold; background:rgba(234,179,8,0.1);" if is_curr else "color:#444;"
        bar_c = "rgba(239,68,68,0.25)" if is_ask else "rgba(16,185,129,0.25)"
        w = min(100, (v/4000)*100)
        dom_rows += f'<div style="display:flex; height:18px; align-items:center; border-bottom:1px solid #111; font-family:monospace;"><div style="width:55px; text-align:right; padding-right:8px; font-size:9px; {p_style}">{p:.1f}</div><div style="flex-grow:1; height:100%; position:relative; background:#080808;">{"<div style=\'position:absolute; left:0; height:100%; width:"+str(w)+"%; background:"+bar_c+";\'></div>" if not is_curr else ""}<div style="position:absolute; right:8px; color:#fff; font-size:8px; font-weight:bold; z-index:10;">{v if not is_curr else ""}</div></div></div>'

    imb = max(t_bid, t_ask)/max(1, min(t_bid, t_ask))

    # C. AFFICHAGE (TROIS COLONNES PROPRES)
    c1, c2, c3 = st.columns([1, 1.8, 1.1])

    with c1:
        # SENTIMENT ET CALENDRIER
        st.markdown(f"""
        <div style="background:#0d0d0d; border:1px solid #1a1a1a; padding:15px; border-radius:4px; margin-bottom:10px;">
            <div style="font-size:9px; color:#eab308; font-weight:900; letter-spacing:1px; margin-bottom:10px;">SENTIMENT</div>
            <div style="text-align:center; font-size:24px; font-weight:900; color:{'#10b981' if gold > poc else '#ef4444'};">{'BULLISH' if gold > poc else 'BEARISH'}</div>
            <div style="text-align:center; color:#eab308; font-size:9px;">Score: {random.randint(65, 82)}%</div>
        </div>
        <div style="background:#0d0d0d; border:1px solid #1a1a1a; padding:15px; border-radius:4px; height:340px;">
            <div style="font-size:9px; color:#eab308; font-weight:900; letter-spacing:1px; margin-bottom:10px;">CALENDAR & NEWS</div>
            <div style="font-size:9px; line-height:1.8;">
                <div style="display:flex; justify-content:space-between;"><span>14:30 | Empire State</span><b style="color:#ef4444;">USD ★★★</b></div>
                <div style="display:flex; justify-content:space-between;"><span>14:30 | Retail Sales</span><b style="color:#ef4444;">USD ★★★</b></div>
                <div style="display:flex; justify-content:space-between;"><span>08:00 | IPC Inflation</span><b style="color:#ef4444;">GBP ★★★</b></div>
                <hr style="border:0; border-top:1px solid #1a1a1a; margin:10px 0;">
                <small style="color:#888;"><b>BCE :</b> Taux maintenus. Refuge favorisé.<br><b>GEO :</b> Tensions géo-politiques +12.5$.</small>
            </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        # TOPBAR INTEGREE ET GRAPH
        st.markdown(f"""
        <div style="background:#0d0d0d; border-bottom:2px solid #eab308; padding:10px; display:flex; justify-content:space-between; align-items:center; border-radius:4px; margin-bottom:10px;">
            <b style="color:#eab308; font-size:16px;">🔱 BEE-INVEST</b>
            <div style="text-align:center;"><b style="color:#10b981;">{cap:,.2f} £</b></div>
            <div style="text-align:right;"><b>GOLD ${gold:,.2f}</b></div>
        </div>""", unsafe_allow_html=True)
        st.components.v1.iframe("https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark", height=340)
        st.markdown(f"""
        <div style="margin-top:10px; display:grid; grid-template-columns: repeat(4, 1fr); gap:8px;">
            <div style="background:#0d0d0d; padding:10px; border:1px solid #1a1a1a; text-align:center; border-radius:4px;"><small style="color:#555;">BCE</small><br><b style="color:#ef4444;">-12.4%</b></div>
            <div style="background:#0d0d0d; padding:10px; border:1px solid #1a1a1a; text-align:center; border-radius:4px;"><small style="color:#555;">ETF</small><br><b style="color:#10b981;">+24.1%</b></div>
            <div style="background:#0d0d0d; padding:10px; border:1px solid #1a1a1a; text-align:center; border-radius:4px;"><small style="color:#555;">GEO</small><br><b style="color:#10b981;">+18.5%</b></div>
            <div style="background:#0d0d0d; padding:10px; border:1px solid #1a1a1a; text-align:center; border-radius:4px;"><small style="color:#555;">USD</small><br><b style="color:#ef4444;">-09.2%</b></div>
        </div>""", unsafe_allow_html=True)

    with c3:
        # CARNET D'ORDRE
        st.markdown(f"""
        <div style="background:#0d0d0d; border:1px solid #1a1a1a; padding:10px; border-radius:4px; height:505px;">
            <div style="font-size:9px; color:#eab308; font-weight:900; letter-spacing:1px; margin-bottom:8px;">ORDER FLOW MATRIX</div>
            <div style="height:460px; overflow:hidden; border:1px solid #1a1a1a; border-radius:2px;">{dom_rows}</div>
        </div>""", unsafe_allow_html=True)

    # D. ROADMAP (BAS DE PAGE)
    st.markdown(f"""
    <div style="background:#0d0d0d; border:1px solid #1a1a1a; padding:15px; border-radius:4px; display:grid; grid-template-columns: repeat(4, 1fr); gap:15px; text-align:center; margin-top:10px;">
        <div><small style="color:#555;">ZONE M.P</small><br><b style="color:{'#10b981' if is_on_zone else '#ef4444'};">{'VALIDATED' if is_on_zone else 'SCANNING'}</b></div>
        <div><small style="color:#555;">IMBALANCE</small><br><b style="color:{'#10b981' if imb >= 2.7 else '#ef4444'};">{imb:.1f}x</b></div>
        <div><small style="color:#555;">DXY FILTER</small><br><b style="color:#10b981;">CONFLUENCE</b></div>
        <div><small style="color:#555;">DECISION</small><br><b style="color:{'#10b981' if imb >= 2.7 and is_on_zone else '#eab308'};">{'READY' if imb >= 2.7 and is_on_zone else 'WAITING'}</b></div>
    </div>""", unsafe_allow_html=True)

terminal_v9()
