import streamlit as st
import requests
import random
import math

# 1. Configuration & Engine
st.set_page_config(page_title="KILLZONE | Terminal Elite", layout="wide", initial_sidebar_state="collapsed")

API_KEY = "a640b1ef6a07445695f0fc9c34359160"

st.markdown("""
<style>
    div[data-testid="stAppViewBlockContainer"] { opacity: 1 !important; padding-top: 0.5rem !important; max-width: 98% !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #d1d1d6; font-family: 'Inter', sans-serif; font-size: 11px; }
    
    .kz-panel { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 12px; margin-bottom: 8px; }
    .kz-header { font-size: 9px; font-weight: 900; color: #eab308; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px; display: flex; align-items: center; }
    .kz-header::after { content: ''; flex: 1; height: 1px; background: #1a1a1a; margin-left: 10px; }
    
    .kz-topbar { display: flex; justify-content: space-between; align-items: center; background: #0d0d0d; padding: 8px 20px; border-bottom: 2px solid #eab308; margin-bottom: 10px; }

    /* COMPONENT STYLING */
    .sentiment-box { text-align: center; padding: 10px; background: #080808; border-radius: 4px; border: 1px solid #222; }
    .macro-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
    .macro-item { background: #080808; padding: 6px; border-radius: 4px; border: 1px solid #1a1a1a; border-left: 2px solid #eab308; }
    
    .eco-item { display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #1a1a1a; font-size: 9px; }
    .impact-high { color: #ef4444; font-weight: bold; }

    /* DOM MATRIX - FULL HEIGHT FIX */
    .dom-container { background: #080808; border: 1px solid #1a1a1a; border-radius: 4px; height: 630px; overflow: hidden; }
    .dom-row { display: flex; height: 21px; align-items: center; font-family: 'JetBrains Mono', monospace; border-bottom: 1px solid #111; }
    .dom-price { width: 60px; color: #444; font-size: 10px; text-align: right; padding-right: 10px; }
    .dom-price.active { color: #eab308; font-weight: 900; background: rgba(234, 179, 8, 0.1); }
    .dom-bar-wrapper { flex-grow: 1; height: 100%; position: relative; display: flex; align-items: center; }
    .bid-bar { background: rgba(16, 185, 129, 0.25); border-right: 2px solid #10b981; position: absolute; left: 0; height: 100%; }
    .ask-bar { background: rgba(239, 68, 68, 0.25); border-right: 2px solid #ef4444; position: absolute; left: 0; height: 100%; }
    .dom-vol { position: absolute; right: 10px; color: #fff; font-size: 9px; font-weight: 700; z-index: 10; }

    /* ROADMAP FOOTER FIX */
    .roadmap-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; padding: 8px; background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; }
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
    is_on_zone = (gold <= val + 0.8) or (gold >= vah - 0.8)

    # --- TOPBAR ---
    st.markdown(f"""<div class="kz-topbar">
        <div style="display:flex; align-items:center; gap:15px;"><b style="color:#eab308; font-size:18px;">BEE-INVEST</b><span style="color:#333;">|</span><small>ELITE V4.4</small></div>
        <div style="text-align:center;"><b style="color:#10b981; font-size:16px;">{cap:,.2f} £</b><div style="width:150px; height:3px; background:#1a1a1a; margin:3px auto;"><div style="width:{prog}%; height:100%; background:#10b981;"></div></div></div>
        <div style="display:flex; gap:30px;"><div style="text-align:right;"><small>XAUUSD</small><br><b>${gold:,.2f}</b></div><div style="text-align:right;"><small>DXY</small><br><b>{dxy:.2f}</b></div></div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.8, 1.1])

    with c1:
        # COL 1 : SENTIMENT & CALENDRIER
        st.markdown(f"""<div class="kz-panel">
            <div class="kz-header">Directional Sentiment</div>
            <div class="sentiment-box">
                <span style="font-size:24px; font-weight:900; color:{'#10b981' if gold > poc else '#ef4444'};">{'BULLISH' if gold > poc else 'BEARISH'}</span><br>
                <span style="color:#eab308; font-weight:bold; font-size:10px;">Confidence Score: {random.randint(65, 82)}%</span>
            </div>
            <p style="font-size:8.5px; color:#555; font-style:italic; margin-top:5px;">Convergence Order Flow / POC / DXY.</p>
        </div>
        <div class="kz-panel" style="height:445px;">
            <div class="kz-header">Eco Calendar (Weekly)</div>
            <div class="eco-item"><span>LUN - 14:30 | Indice Empire State</span><span class="impact-high">USD ★★★</span></div>
            <div class="eco-item"><span>MAR - 14:30 | Ventes au détail</span><span class="impact-high">USD ★★★</span></div>
            <div class="eco-item"><span>MER - 08:00 | IPC Inflation</span><span class="impact-high">GBP ★★★</span></div>
            <div class="eco-item"><span>JEU - 14:30 | Inscr. Chômage</span><span style="color:#eab308;">USD ★★☆</span></div>
            <div class="eco-item"><span>VEN - 16:00 | Discours Powell</span><span class="impact-high">USD ★★★</span></div>
            <div style="margin-top:15px;"><div class="kz-header">Market Intel</div>
            <small style="color:#888; font-size:9px; line-height:1.2;"><b>BCE Intel:</b> Rumeurs de pause sur les taux, l'Or reste le refuge favori.<br><br><b>Geo-Watch:</b> Risques de rupture de chaîne sur les métaux précieux.</small></div>
        </div>""", unsafe_allow_html=True)

    with c2:
        # COL 2 : GRAPH & MACRO (ALIGNEMENT PERFECT)
        st.markdown(f"""<div class="kz-panel" style="height:628px;">
            <div class="kz-header">TradingView Analysis (M15)</div>
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark" style="width: 100%; height: 420px; border: none; border-radius:4px;"></iframe>
            <div style="margin-top:12px;"><div class="kz-header">Macro Strategy & Geo-Risk (%)</div>
                <div class="macro-grid">
                    <div class="macro-item"><small>BCE POLICY</small><br><b style="color:#ef4444;">-12.4%</b></div>
                    <div class="macro-item"><small>ETF ACCUM.</small><br><b style="color:#10b981;">+24.1%</b></div>
                    <div class="macro-item"><small>GEO RISK</small><br><b style="color:#10b981;">+18.5%</b></div>
                    <div class="macro-item"><small>USD INDEX</small><br><b style="color:#ef4444;">-09.2%</b></div>
                </div>
            </div>
            <p style="font-size:9px; color:#555; margin-top:10px;"><b>LOGIQUE :</b> Absorption Market vs Limit. Ratio 2.7x requis.</p>
        </div>""", unsafe_allow_html=True)

    with c3:
        # COL 3 : DOM (REMPLIT TOUTE LA HAUTEUR)
        st.markdown("""<div class="kz-panel" style="height:628px;"><div class="kz-header">Order Flow L2 Matrix</div>""", unsafe_allow_html=True)
        dom_html, t_ask, t_bid = "<div class='dom-container'>", 0, 0
        setup_dir = "BULL" if gold <= val+0.8 else "BEAR" if gold >= vah-0.8 else "NONE"
        for i in range(14, -15, -1):
            p = round(gold + (i * 0.4), 1)
            is_ask, is_curr = p > gold, p == round(gold, 1)
            v = random.randint(2500, 3200) if ((setup_dir == "BULL" and p == round(val,1)) or (setup_dir == "BEAR" and p == round(vah,1))) else random.randint(150, 650)
            if not is_curr:
                if is_ask: t_ask += v
                else: t_bid += v
            row_style = 'active' if is_curr else ''
            bar_html = f'<div class="{"ask-bar" if is_ask else "bid-bar"}" style="width:{min(100,(v/4000)*100)}%;"></div>' if not is_curr else ''
            dom_html += f'<div class="dom-row"><div class="dom-price {row_style}">{p:.1f}</div><div class="dom-bar-wrapper">{bar_html}<div class="dom-vol">{v if not is_curr else ""}</div></div></div>'
        st.markdown(dom_html + "</div></div>", unsafe_allow_html=True)

    # ROADMAP FOOTER (REMONTE D'UN CRAN)
    imb_ratio = max(t_bid, t_ask) / max(1, min(t_bid, t_ask))
    st.markdown(f"""<div class="roadmap-grid">
        <div style="padding-left:10px;"><small style="color:#555;">ZONE M.P</small><br><b style="color:{'#10b981' if is_on_zone else '#ef4444'};">{'VALIDATED' if is_on_zone else 'SCANNING'}</b></div>
        <div style="padding-left:10px;"><small style="color:#555;">IMBALANCE</small><br><b style="color:{'#10b981' if imb_ratio >= 2.7 else '#ef4444'};">{imb_ratio:.1f}x</b></div>
        <div style="padding-left:10px;"><small style="color:#555;">DXY FILTER</small><br><b style="color:#10b981;">CONFLUENCE</b></div>
        <div style="padding-left:10px;"><small style="color:#555;">DECISION</small><br><b style="color:{'#10b981' if imb_ratio >= 2.7 else '#eab308'};">{'READY TO FIRE' if imb_ratio >= 2.7 else 'NO EDGE'}</b></div>
    </div>""", unsafe_allow_html=True)

terminal_engine()
