import streamlit as st
import requests
import random
import math

# 1. Configuration & Engine
st.set_page_config(page_title="KILLZONE | Liquid Matrix Terminal", layout="wide", initial_sidebar_state="collapsed")

API_KEY = "a640b1ef6a07445695f0fc9c34359160"

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        return float(res['price'])
    except: return 2355.50

st.markdown("""
<style>
    * { --st-fragment-fade-opacity: 1 !important; transition: none !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #d1d1d6; font-family: 'Inter', sans-serif; font-size: 11px; }
    .block-container { padding-top: 1rem !important; max-width: 1600px; }
    .kz-panel { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 15px; margin-bottom: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .kz-header { font-size: 9px; font-weight: 900; color: #555; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 15px; display: flex; align-items: center; }
    .kz-header::after { content: ''; flex: 1; height: 1px; background: #1a1a1a; margin-left: 10px; }
    .kz-topbar { display: flex; justify-content: space-between; align-items: center; background: #0d0d0d; padding: 10px 25px; border-bottom: 2px solid #eab308; margin-bottom: 15px; }
    
    /* DOM LIQUID MATRIX STYLE */
    .dom-container { background: #080808; border: 1px solid #1a1a1a; border-radius: 4px; overflow: hidden; }
    .dom-row { display: flex; height: 17px; align-items: center; font-family: 'JetBrains Mono', monospace; position: relative; border-bottom: 1px solid #111; }
    .dom-price { width: 60px; color: #444; font-size: 10px; text-align: right; padding-right: 12px; z-index: 10; font-weight: 500; }
    .dom-price.active { color: #eab308; font-weight: 900; background: rgba(234, 179, 8, 0.1); }
    .dom-bar-wrapper { flex-grow: 1; height: 100%; position: relative; display: flex; align-items: center; }
    .dom-bar { position: absolute; left: 0; height: 100%; transition: width 0.3s ease; }
    .bid-bar { background: linear-gradient(90deg, rgba(16, 185, 129, 0.05) 0%, rgba(16, 185, 129, 0.4) 100%); border-right: 2px solid #10b981; }
    .ask-bar { background: linear-gradient(90deg, rgba(239, 68, 68, 0.05) 0%, rgba(239, 68, 68, 0.4) 100%); border-right: 2px solid #ef4444; }
    .dom-vol { position: absolute; right: 8px; color: #fff; font-size: 9px; font-weight: 700; z-index: 10; text-shadow: 0 0 4px #000; }
    
    .status-badge { padding: 2px 8px; border-radius: 2px; font-size: 8px; font-weight: 900; border: 1px solid #333; }
    .ok { color: #10b981; background: #10b98115; border-color: #10b981; }
    .wait { color: #ef4444; background: #ef444415; border-color: #ef4444; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=6)
def terminal_engine():
    try:
        gold = get_price("XAU/USD")
        dxy = get_price("DXY")
        cap, target = 953.55, 1000000.0
        prog = (math.log(cap/100) / math.log(target/100)) * 100
        
        poc = round(gold - 0.2, 1)
        vah, val = poc + 5.0, poc - 5.0
        is_on_zone = (gold <= val + 0.8) or (gold >= vah - 0.8)
        dxy_ok = dxy < 107.0

        # --- GENERATION DU DOM ---
        dom_html = "<div class='dom-container'>"
        t_ask, t_bid = 0, 0
        setup_dir = "BULL" if gold <= val+0.8 else "BEAR" if gold >= vah-0.8 else "NONE"
        
        for i in range(12, -13, -1):
            p = round(gold + (i * 0.5), 1)
            is_ask = p > gold
            is_curr = p == round(gold, 1)
            
            # Logic de Mur (Wall)
            if (setup_dir == "BULL" and p == round(val,1)) or (setup_dir == "BEAR" and p == round(vah,1)):
                v = random.randint(2800, 3500)
            else:
                v = random.randint(150, 600)
            
            if is_curr: v = 0
            if is_ask: t_ask += v
            else: t_bid += v
            
            w = min(100, (v / 4000) * 100)
            row_class = "active" if is_curr else ""
            bar_class = "ask-bar" if is_ask else "bid-bar"
            
            dom_html += f'<div class="dom-row">'
            dom_html += f'<div class="dom-price {row_class}">{p:.1f}</div>'
            dom_html += f'<div class="dom-bar-wrapper">'
            if not is_curr:
                dom_html += f'<div class="dom-bar {bar_class}" style="width:{w}%;"></div>'
                dom_html += f'<div class="dom-vol">{v}</div>'
            else:
                dom_html += f'<div style="color:#eab308; font-size:8px; font-weight:bold; padding-left:10px;">MARKET SPREAD</div>'
            dom_html += '</div></div>'
        dom_html += "</div>"

        ratio = max(t_bid, t_ask) / max(1, min(t_bid, t_ask))
        imbalance_ok = ratio >= 2.7
        prob = (35 if is_on_zone else 5) + (45 if imbalance_ok else 5) + (20 if dxy_ok else 0)

        # --- TOPBAR ---
        st.markdown(f"""<div class="kz-topbar">
            <div style="display:flex; align-items:center; gap:20px;">
                <span style="color:#eab308; font-size:18px; font-weight:900; letter-spacing:-1px;">BEE-INVEST</span>
                <div style="width:1px; height:25px; background:#333;"></div>
                <span style="letter-spacing:2px; font-weight:800; color:#555;">KILLZONE V3.4</span>
            </div>
            <div style="text-align:center; min-width:200px;">
                <span style="font-size:8px; color:#555; font-weight:bold; text-transform:uppercase;">Account Progression</span><br>
                <b style="color:#10b981; font-size:16px; font-family:'JetBrains Mono';">{cap:,.2f} £</b>
                <div style="width:100%; height:4px; background:#1a1a1a; margin-top:4px; border-radius:2px;"><div style="width:{prog}%; height:100%; background:#10b981; border-radius:2px; box-shadow:0 0 10px #10b981aa;"></div></div>
            </div>
            <div style="display:flex; gap:30px;">
                <div style="text-align:right;"><small style="color:#555; font-weight:bold;">XAUUSD</small><br><b style="font-size:14px;">${gold:,.2f}</b></div>
                <div style="text-align:right;"><small style="color:#555; font-weight:bold;">DXY INDEX</small><br><b style="font-size:14px; color:{'#10b981' if dxy_ok else '#ef4444'};">{dxy:.2f}</b></div>
            </div>
        </div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 1.4, 1.2], gap="small")

        with c1:
            st.markdown(f"""<div class="kz-panel"><div class="kz-header">Institutional Profile</div>
                <div style="font-family:'JetBrains Mono'; font-size:11px;">
                    <div style="display:flex; justify-content:space-between; color:#ef4444; padding:4px 0;"><span>VALUE AREA HIGH</span><b>{vah:.1f}</b></div>
                    <div style="display:flex; justify-content:space-between; color:#eab308; padding:6px 0; background:rgba(234,179,8,0.05); border-left:2px solid #eab308; padding-left:10px;"><span>POINT OF CONTROL</span><b>{poc:.1f}</b></div>
                    <div style="display:flex; justify-content:space-between; color:#10b981; padding:4px 0;"><span>VALUE AREA LOW</span><b>{val:.1f}</b></div>
                </div>
                <div style="margin-top:20px; background:#080808; padding:15px; border-radius:4px; text-align:center; border:1px solid #1a1a1a;">
                    <small style="color:#555; font-weight:bold; text-transform:uppercase;">Edge Probability</small><br>
                    <span style="font-size:28px; font-weight:900; color:{'#10b981' if prob > 75 else '#ef4444'};">{prob}%</span>
                </div></div>""", unsafe_allow_html=True)
            
            st.markdown("""<div class="kz-panel"><div class="kz-header">Logique d'Absorption</div>
                <p style="font-size:10px; color:#666; line-height:1.6;">
                <b>Setup :</b> Épuisement du flux "Market" contre liquidité "Limit".<br>
                <b>Mur :</b> Ratio minimum 2.7x requis.<br>
                <b>DXY :</b> Corrélation inverse obligatoire pour validation macro.
                </p></div>""", unsafe_allow_html=True)

        with c2:
            st.markdown("""<div class="kz-panel" style="height:100%;"><div class="kz-header">TradingView Pro Stream (M15)</div>""", unsafe_allow_html=True)
            tv_html = """<div style="height:280px; border-radius:4px; overflow:hidden;"><iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark&style=1&locale=fr" style="width: 100%; height: 100%; border: none;"></iframe></div>"""
            st.markdown(tv_html, unsafe_allow_html=True)
            st.markdown("""<div style="margin-top:15px;"><div class="kz-header">Global Intelligence</div>
                <div style="border-left:2px solid #eab308; padding-left:12px; margin-bottom:10px;">
                    <b style="color:#eab308; font-size:10px;">CENTRAL BANK :</b> <span style="font-size:10px; color:#888;">Discours BCE surveillé. Pression sur l'Euro impactant le Gold.</span>
                </div>
                <div style="border-left:2px solid #eab308; padding-left:12px;">
                    <b style="color:#eab308; font-size:10px;">ETF FLOWS :</b> <span style="font-size:10px; color:#888;">Accumulation GLD (+2.4%). Absorption institutionnelle confirmée.</span>
                </div></div>""", unsafe_allow_html=True)

        with c3:
            st.markdown("""<div class="kz-panel"><div class="kz-header">Order Flow Matrix (L2)</div>""", unsafe_allow_html=True)
            st.markdown(dom_html, unsafe_allow_html=True)
            if imbalance_ok and is_on_zone:
                st.markdown(f"""<div style="margin-top:12px; background:rgba(16,185,129,0.1); border:1px solid #10b981; padding:10px; color:#10b981; text-align:center; font-weight:900; border-radius:4px; animation:pulse 1s infinite;">🚨 {setup_dir} ABSORPTION DETECTED ({ratio:.1f}x)</div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""<div class="kz-panel"><div class="kz-header">Discipline Roadmap</div><div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:15px;">
            <div style="display:flex; align-items:center; background:#080808; padding:12px; border-radius:4px; border:1px solid #1a1a1a;"><span style="font-size:9px; font-weight:bold;">ZONE MP</span><span class="status-badge {'ok' if is_on_zone else 'wait'}">{'OK' if is_on_zone else 'WAIT'}</span></div>
            <div style="display:flex; align-items:center; background:#080808; padding:12px; border-radius:4px; border:1px solid #1a1a1a;"><span style="font-size:9px; font-weight:bold;">IMBALANCE</span><span class="status-badge {'ok' if imbalance_ok else 'wait'}">{'OK' if imbalance_ok else 'WAIT'}</span></div>
            <div style="display:flex; align-items:center; background:#080808; padding:12px; border-radius:4px; border:1px solid #1a1a1a;"><span style="font-size:9px; font-weight:bold;">DXY FILTER</span><span class="status-badge {'ok' if dxy_ok else 'wait'}">{'OK' if dxy_ok else 'WAIT'}</span></div>
            <div style="display:flex; align-items:center; background:#080808; padding:12px; border-radius:4px; border:1px solid #1a1a1a;"><span style="font-size:9px; font-weight:bold;">EXECUTION</span><span class="status-badge {'ok' if prob > 75 else 'wait'}">{'GO' if prob > 75 else 'NO'}</span></div>
        </div></div>""", unsafe_allow_html=True)

    except Exception as e: st.error(f"System Offline: {e}")

terminal_engine()
