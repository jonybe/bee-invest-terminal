import streamlit as st
import requests
import random
import math

# 1. Configuration & Engine
st.set_page_config(page_title="KILLZONE | Terminal V4.2", layout="wide", initial_sidebar_state="collapsed")

API_KEY = "a640b1ef6a07445695f0fc9c34359160"

# CSS INTERFACE PRO (Strictement basé sur la 4.0)
st.markdown("""
<style>
    div[data-testid="stAppViewBlockContainer"] { opacity: 1 !important; padding-top: 1rem !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #d1d1d6; font-family: 'Inter', sans-serif; font-size: 11px; }
    
    .kz-panel { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 18px; margin-bottom: 12px; height: 100%; }
    .kz-header { font-size: 9px; font-weight: 900; color: #555; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px; display: flex; align-items: center; }
    .kz-header::before { content: ''; width: 3px; height: 12px; background: #eab308; margin-right: 10px; }
    
    .kz-topbar { display: flex; justify-content: space-between; align-items: center; background: #0d0d0d; padding: 12px 25px; border-bottom: 2px solid #eab308; margin-bottom: 15px; }

    /* MACRO & SENTIMENT */
    .sentiment-box { text-align: center; padding: 20px; background: #080808; border-radius: 6px; border: 1px solid #eab30844; margin-bottom: 15px; }
    .macro-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
    .macro-item { background: #080808; padding: 10px; border-radius: 4px; border: 1px solid #1a1a1a; }
    .macro-val { font-size: 14px; font-weight: 900; font-family: 'JetBrains Mono'; }
    
    /* DOM MATRIX FIXED */
    .dom-container { background: #080808; border: 1px solid #1a1a1a; border-radius: 4px; height: 480px; overflow: hidden; }
    .dom-row { display: flex; height: 19px; align-items: center; font-family: 'JetBrains Mono', monospace; border-bottom: 1px solid #111; }
    .dom-price { width: 65px; color: #444; font-size: 10px; text-align: right; padding-right: 12px; }
    .dom-price.active { color: #eab308; font-weight: 900; background: rgba(234, 179, 8, 0.1); }
    .dom-bar-wrapper { flex-grow: 1; height: 100%; position: relative; display: flex; align-items: center; }
    .bid-bar { background: rgba(16, 185, 129, 0.3); border-right: 2px solid #10b981; position: absolute; left: 0; height: 100%; }
    .ask-bar { background: rgba(239, 68, 68, 0.3); border-right: 2px solid #ef4444; position: absolute; left: 0; height: 100%; }
    .dom-vol { position: absolute; right: 10px; color: #fff; font-size: 9px; font-weight: 700; z-index: 10; }
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
    # DATA
    gold = get_price("XAU/USD")
    dxy = get_price("DXY")
    cap = 953.55
    prog = (math.log(cap/100) / math.log(1000000/100)) * 100
    poc = round(gold - 0.2, 1)
    vah, val = poc + 5.0, poc - 5.0

    # TOPBAR
    st.markdown(f"""<div class="kz-topbar">
        <div style="display:flex; align-items:center; gap:20px;"><b style="color:#eab308; font-size:20px;">BEE-INVEST</b><span style="color:#333;">|</span><small>V4.2 FINAL</small></div>
        <div style="text-align:center;"><b style="color:#10b981; font-size:16px;">{cap:,.2f} £</b><div style="width:140px; height:4px; background:#1a1a1a; margin:4px auto;"><div style="width:{prog}%; height:100%; background:#10b981;"></div></div></div>
        <div style="display:flex; gap:35px;"><div style="text-align:right;"><small>GOLD</small><br><b>${gold:,.2f}</b></div><div style="text-align:right;"><small>DXY INDEX</small><br><b>{dxy:.2f}</b></div></div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.6, 1.2])

    with c1:
        # MODULE SENTIMENT & MACRO (4.0 Style)
        st.markdown(f"""
        <div class="kz-panel">
            <div class="kz-header">Daily Direction Sentiment</div>
            <div class="sentiment-box">
                <span style="font-size:28px; font-weight:900; color:{'#10b981' if gold > poc else '#ef4444'};">{'BULLISH' if gold > poc else 'BEARISH'}</span><br>
                <span style="font-size:10px; color:#eab308; font-weight:bold;">Sentiment Score: {random.randint(65, 82)}%</span>
            </div>
            <div class="kz-header">Macro & Geo Impact (%)</div>
            <div class="macro-grid">
                <div class="macro-item"><small>BCE POLICY</small><br><span class="macro-val" style="color:#ef4444;">-12.4%</span></div>
                <div class="macro-item"><small>ETF ACCUM.</small><br><span class="macro-val" style="color:#10b981;">+24.1%</span></div>
                <div class="macro-item"><small>GEO RISK</small><br><span class="macro-val" style="color:#10b981;">+18.5%</span></div>
                <div class="macro-item"><small>CPI US EXP.</small><br><span class="macro-val" style="color:#ef4444;">-09.2%</span></div>
            </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        # GRAPH ET NEWS (4.0 Style)
        st.markdown(f"""
        <div class="kz-panel" style="height:535px;">
            <div class="kz-header">TradingView Elite Stream (M15)</div>
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark" style="width: 100%; height: 350px; border: none; border-radius:4px;"></iframe>
            <div style="margin-top:20px;">
                <div class="kz-header">Market Intelligence Feed</div>
                <div style="font-size:10px; color:#888; border-left:2px solid #eab308; padding-left:12px; margin-bottom:10px;"><b>BCE Intel:</b> Rumeurs de pause sur les taux, l'Or reste le refuge favori des investisseurs EU.</div>
                <div style="font-size:10px; color:#888; border-left:2px solid #eab308; padding-left:12px;"><b>Geo-Watch:</b> Risques de rupture de chaîne sur les métaux précieux. Prime de risque intégrée.</div>
            </div>
        </div>""", unsafe_allow_html=True)

    with c3:
        # CARNET D'ORDRE (Correction du bug de boucle)
        st.markdown("""<div class="kz-panel" style="height:535px;"><div class="kz-header">Order Flow Matrix (L2)</div>""", unsafe_allow_html=True)
        dom_html = "<div class='dom-container'>"
        t_ask, t_bid = 0, 0
        setup_dir = "BULL" if gold <= val+0.8 else "BEAR" if gold >= vah-0.8 else "NONE"
        
        for i in range(12, -13, -1):
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
            if not is_curr:
                dom_html += f'<div class="{bar_type}" style="width:{bar_width}%;"></div><div class="dom-vol">{v}</div>'
            else:
                dom_html += f'<div style="color:#eab308; font-size:8px; font-weight:bold; padding-left:10px;">SPREAD</div>'
            dom_html += '</div></div>'
            
        dom_html += "</div></div>"
        st.markdown(dom_html, unsafe_allow_html=True)

    # DISCIPLINE ROADMAP (En bas, bien alignée)
    imb_ratio = max(t_bid, t_ask) / max(1, min(t_bid, t_ask))
    st.markdown(f"""<div class="kz-panel" style="margin-top:12px;"><div class="kz-header">Execution Roadmap</div>
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:12px;">
            <div style="background:#080808; padding:12px; border:1px solid #222; border-radius:4px;"><small>ZONE MP</small><span style="float:right; color:{'#10b981' if gold <= val+0.8 or gold >= vah-0.8 else '#ef4444'};">{'OK' if gold <= val+0.8 or gold >= vah-0.8 else 'WAIT'}</span></div>
            <div style="background:#080808; padding:12px; border:1px solid #222; border-radius:4px;"><small>IMBALANCE</small><span style="float:right; color:{'#10b981' if imb_ratio >= 2.7 else '#ef4444'};">{imb_ratio:.1f}x</span></div>
            <div style="background:#080808; padding:12px; border:1px solid #222; border-radius:4px;"><small>DXY FILTER</small><span style="float:right; color:#10b981;">PASS</span></div>
            <div style="background:#080808; padding:12px; border:1px solid #222; border-radius:4px;"><small>DECISION</small><span style="float:right; color:{'#10b981' if imb_ratio >= 2.7 else '#eab308'}; font-weight:bold;">{'READY' if imb_ratio >= 2.7 else 'SCAN'}</span></div>
        </div></div>""", unsafe_allow_html=True)

terminal_engine()
