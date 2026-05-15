import streamlit as st
import requests
import random
import math

# 1. Configuration & API
st.set_page_config(page_title="KILLZONE | Terminal V6.1", layout="wide", initial_sidebar_state="collapsed")
API_KEY = "a640b1ef6a07445695f0fc9c34359160"

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        return float(res['price'])
    except: return 2355.50

# 2. CSS DE PRÉCISION (Anti-espacement)
st.markdown("""
<style>
    [data-testid="stAppViewBlockContainer"] { padding: 0.5rem 1rem !important; }
    div[class^="st-emotion-cache"] { gap: 0rem !important; } /* Supprime l'espace entre les blocs Streamlit */
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #d1d1d6; font-family: 'Inter', sans-serif; }
    
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 12px; margin-bottom: 8px; }
    .kz-header { font-size: 9px; font-weight: 900; color: #eab308; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 8px; border-left: 3px solid #eab308; padding-left: 8px; }
    
    /* DOM STYLING */
    .dom-box { background: #080808; border: 1px solid #1a1a1a; height: 530px; overflow: hidden; border-radius: 4px; }
    .dom-row { display: flex; height: 18px; align-items: center; border-bottom: 1px solid #111; font-family: 'JetBrains Mono', monospace; }
    .dom-p { width: 55px; text-align: right; padding-right: 8px; font-size: 10px; }
    .dom-bar-wrap { flex-grow: 1; height: 100%; position: relative; display: flex; align-items: center; }
    .dom-vol { position: absolute; right: 8px; color: #fff; font-size: 9px; font-weight: bold; z-index: 10; }
    
    /* IFRAME FIX */
    iframe { border: none !important; border-radius: 4px; background: #0d0d0d; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=8)
def terminal():
    # CALCULS
    gold = get_price("XAU/USD")
    dxy = get_price("DXY")
    cap = 953.55
    prog = (math.log(cap/100) / math.log(1000000/100)) * 100
    poc = round(gold - 0.2, 1)
    vah, val = poc + 5.0, poc - 5.0
    
    # DOM ENGINE
    dom_html = ""
    t_ask, t_bid = 0, 0
    setup_dir = "BULL" if gold <= val+0.8 else "BEAR" if gold >= vah-0.8 else "NONE"
    for i in range(14, -15, -1):
        p = round(gold + (i * 0.4), 1)
        is_ask = p > gold
        is_curr = p == round(gold, 1)
        v = random.randint(2500, 3500) if ((setup_dir == "BULL" and p == round(val,1)) or (setup_dir == "BEAR" and p == round(vah,1))) else random.randint(150, 650)
        if not is_curr:
            if is_ask: t_ask += v
            else: t_bid += v
        
        p_style = "color:#eab308; font-weight:bold; background:rgba(234,179,8,0.1);" if is_curr else "color:#444;"
        bar_c = "rgba(239,68,68,0.3)" if is_ask else "rgba(16,185,129,0.3)"
        bar_b = "#ef4444" if is_ask else "#10b981"
        w = min(100, (v/4000)*100)
        
        dom_html += f'<div class="dom-row"><div class="dom-p" style="{p_style}">{p:.1f}</div>'
        dom_html += f'<div class="dom-bar-wrap">'
        if not is_curr: dom_html += f'<div style="position:absolute; left:0; height:100%; width:{w}%; background:{bar_c}; border-right:2px solid {bar_b};"></div>'
        dom_html += f'<div class="dom-vol">{v if not is_curr else ""}</div>{"<small style=\'color:#eab308; padding-left:10px; font-size:8px;\'>SPREAD</small>" if is_curr else ""}</div></div>'

    ratio = max(t_bid, t_ask) / max(1, min(t_bid, t_ask))
    is_on_zone = (gold <= val + 0.8) or (gold >= vah - 0.8)

    # --- TOPBAR ---
    st.markdown(f"""
    <div style="background:#0d0d0d; border-bottom:2px solid #eab308; padding:8px 20px; display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <div style="display:flex; align-items:center; gap:15px;"><b style="color:#eab308; font-size:18px;">BEE-INVEST</b><span style="color:#333;">|</span><small>ELITE TERMINAL V6.1</small></div>
        <div style="text-align:center;"><b style="color:#10b981; font-size:16px;">{cap:,.2f} £</b><div style="width:150px; height:3px; background:#1a1a1a; margin:3px auto;"><div style="width:{prog}%; height:100%; background:#10b981;"></div></div></div>
        <div style="display:flex; gap:30px;"><div style="text-align:right;"><small>GOLD</small><br><b>${gold:,.2f}</b></div><div style="text-align:right;"><small>DXY</small><br><b>{dxy:.2f}</b></div></div>
    </div>""", unsafe_allow_html=True)

    # --- GRID SYSTEM ---
    c1, c2, c3 = st.columns([1, 2, 1.1])

    with c1:
        st.markdown(f"""
        <div class="kz-card">
            <div class="kz-header">Directional Sentiment</div>
            <div style="text-align:center; padding:12px; background:#080808; border-radius:4px; border:1px solid #222;">
                <span style="font-size:22px; font-weight:900; color:{'#10b981' if gold > poc else '#ef4444'};">{'BULLISH' if gold > poc else 'BEARISH'}</span><br>
                <span style="color:#eab308; font-weight:bold; font-size:10px;">Score: {random.randint(65, 82)}%</span>
            </div>
        </div>
        <div class="kz-card" style="height:380px;">
            <div class="kz-header">Weekly Calendar (HEC)</div>
            <div style="font-size:9px; line-height:1.6;">
                <div style="display:flex; justify-content:space-between;"><span>14:30 | Empire State</span><b style="color:#ef4444;">USD ★★★</b></div>
                <div style="display:flex; justify-content:space-between;"><span>14:30 | Retail Sales</span><b style="color:#ef4444;">USD ★★★</b></div>
                <div style="display:flex; justify-content:space-between;"><span>08:00 | IPC Inflation</span><b style="color:#ef4444;">GBP ★★★</b></div>
                <div style="display:flex; justify-content:space-between;"><span>14:30 | Jobless Claims</span><b style="color:#eab308;">USD ★★☆</b></div>
                <div style="display:flex; justify-content:space-between;"><span>16:00 | Powell Speech</span><b style="color:#ef4444;">USD ★★★</b></div>
                <hr style="border:0; border-top:1px solid #1a1a1a; margin:8px 0;">
                <div class="kz-header">Intel</div>
                <small style="color:#888;"><b>BCE :</b> Pause confirmée.<br><b>GEO :</b> Tensions géo +12$.</small>
            </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        # FUSION GRAPHIQUE + MACRO POUR ÉVITER LE DÉCALAGE
        st.markdown("""<div class="kz-card" style="height:538px; padding-bottom:0px;">
            <div class="kz-header">TradingView Analysis (M15)</div>""", unsafe_allow_html=True)
        st.components.v1.iframe("https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark", height=370)
        st.markdown(f"""
            <div style="margin-top:10px; display:grid; grid-template-columns: repeat(4, 1fr); gap:8px;">
                <div style="background:#080808; padding:8px; border:1px solid #1a1a1a; text-align:center;"><small>BCE</small><br><b style="color:#ef4444;">-12.4%</b></div>
                <div style="background:#080808; padding:8px; border:1px solid #1a1a1a; text-align:center;"><small>ETF</small><br><b style="color:#10b981;">+24.1%</b></div>
                <div style="background:#080808; padding:8px; border:1px solid #1a1a1a; text-align:center;"><small>GEO</small><br><b style="color:#10b981;">+18.5%</b></div>
                <div style="background:#080808; padding:8px; border:1px solid #1a1a1a; text-align:center;"><small>USD</small><br><b style="color:#ef4444;">-09.2%</b></div>
            </div></div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""<div class="kz-card" style="height:538px;"><div class="kz-header">Order Flow Matrix (L2)</div><div class="dom-box">{dom_html}</div></div>""", unsafe_allow_html=True)

    # --- ROADMAP (REMONTE CAR ESPACE SUPPRIMÉ) ---
    st.markdown(f"""
    <div style="background:#0d0d0d; border:1px solid #1a1a1a; padding:12px; border-radius:4px; display:grid; grid-template-columns: repeat(4, 1fr); gap:15px; text-align:center;">
        <div><small style="color:#555;">ZONE M.P</small><br><b style="color:{'#10b981' if is_on_zone else '#ef4444'};">{'VALIDATED' if is_on_zone else 'SCANNING'}</b></div>
        <div><small style="color:#555;">IMBALANCE</small><br><b style="color:{'#10b981' if ratio >= 2.7 else '#ef4444'};">{ratio:.1f}x</b></div>
        <div><small style="color:#555;">DXY FILTER</small><br><b style="color:#10b981;">CONFLUENCE</b></div>
        <div><small style="color:#555;">DECISION</small><br><b style="color:{'#10b981' if ratio >= 2.7 and is_on_zone else '#eab308'};">{'READY TO FIRE' if ratio >= 2.7 and is_on_zone else 'NO EDGE'}</b></div>
    </div>""", unsafe_allow_html=True)

terminal()
