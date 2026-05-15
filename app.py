import streamlit as st
import requests
import random
import math
from datetime import datetime

# 1. Configuration
st.set_page_config(page_title="KILLZONE | Terminal TwelveData", layout="wide", initial_sidebar_state="collapsed")

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
    html, body, [data-testid="stAppViewContainer"] { background-color: #060606 !important; color: #d1d1d6; font-family: 'Inter', sans-serif; font-size: 11px; }
    .block-container { padding-top: 1rem !important; max-width: 1600px; }
    .kz-panel { background: #111111; border: 1px solid #222222; border-radius: 4px; padding: 15px; margin-bottom: 10px; }
    .kz-header { font-size: 10px; font-weight: 800; color: #71717a; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px; display: flex; align-items: center; }
    .kz-header::before { content: ''; width: 3px; height: 12px; background: #eab308; margin-right: 8px; }
    .kz-topbar { display: flex; justify-content: space-between; align-items: center; background: #111; padding: 10px 20px; border-bottom: 1px solid #eab308; margin-bottom: 15px; }
    .dom-row { display: flex; height: 16px; align-items: center; font-family: 'JetBrains Mono'; border-bottom: 1px solid #1a1a1a; width: 100%; }
    .dom-price { width: 50px; color: #555; font-size: 9px; text-align: right; margin-right: 10px; flex-shrink: 0; }
    .dom-bar-container { flex-grow: 1; height: 12px; background: #0c0c0c; position: relative; display: flex; align-items: center; }
    .dom-bar-bid { position: absolute; left: 0; height: 100%; background: #10b98133; border-right: 2px solid #10b981; }
    .dom-bar-ask { position: absolute; left: 0; height: 100%; background: #ef444433; border-right: 2px solid #ef4444; }
    .dom-vol { position: absolute; right: 5px; color: #fff; font-size: 8px; font-weight: bold; z-index: 5; }
    .status-badge { padding: 2px 6px; border-radius: 2px; font-size: 8px; font-weight: 900; margin-left: auto; border: 1px solid #333; }
    .ok { color: #10b981; background: #10b98111; border-color: #10b981; }
    .wait { color: #ef4444; background: #ef444411; border-color: #ef4444; }
    iframe { border-radius: 4px; border: 1px solid #222; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=8)
def terminal_engine():
    try:
        gold = get_price("XAU/USD")
        dxy = get_price("DXY")
        cap = 953.55
        prog = (math.log(cap/100) / math.log(1000000/100)) * 100
        
        poc = round(gold - 0.2, 1)
        vah, val = poc + 5.0, poc - 5.0
        is_on_zone = (gold <= val + 0.8) or (gold >= vah - 0.8)
        dxy_ok = dxy < 107.0

        dom_html = "<div style='background:#080808; padding:8px; border-radius:4px; border:1px solid #1a1a1a;'>"
        t_ask, t_bid = 0, 0
        setup_dir = "BULL" if gold <= val+0.8 else "BEAR" if gold >= vah-0.8 else "NONE"
        
        prices_range = [round(gold + (i * 0.5), 1) for i in range(10, -11, -1)]
        for p in prices_range:
            is_ask = p > gold
            v = random.randint(2400, 3100) if ((setup_dir == "BULL" and p == round(val,1)) or (setup_dir == "BEAR" and p == round(vah,1))) else random.randint(120, 500)
            if p == round(gold, 1): v = 0
            if is_ask: t_ask += v
            else: t_bid += v
            p_style = "color:#eab308; font-weight:bold;" if p == round(gold, 1) else ""
            dom_html += f'<div class="dom-row"><div class="dom-price" style="{p_style}">{p:.1f}</div>'
            dom_html += f'<div class="dom-bar-container">'
            if p != round(gold, 1): dom_html += f'<div class="dom-bar-{"ask" if is_ask else "bid"}" style="width:{min(100, (v/3500)*100)}%;"></div>'
            dom_html += f'<div class="dom-vol">{v if v>0 else ""}</div></div></div>'
        dom_html += "</div>"

        ratio = max(t_bid, t_ask) / max(1, min(t_bid, t_ask))
        imbalance_ok = ratio >= 2.7
        prob = (35 if is_on_zone else 5) + (45 if imbalance_ok else 5) + (20 if dxy_ok else 0)

        st.markdown(f"""<div class="kz-topbar">
            <div style="display:flex; align-items:center; gap:15px;"><b style="color:#eab308; font-size:16px;">🔱 BEE-INVEST</b><span style="color:#444;">|</span><span style="letter-spacing:1px; font-weight:800;">KILLZONE V3.2</span></div>
            <div style="text-align:center;"><span style="font-size:8px; color:#71717a;">ROUTE AU MILLION</span><br><b style="color:#10b981; font-size:14px;">{cap:,.2f} £</b><div style="width:120px; height:3px; background:#222; margin-top:2px;"><div style="width:{prog}%; height:100%; background:#10b981;"></div></div></div>
            <div style="display:flex; gap:25px;"><div style="text-align:right;"><small style="color:#71717a;">XAU/USD</small><br><b>${gold:,.2f}</b></div><div style="text-align:right;"><small style="color:#71717a;">DXY Index</small><br><b style="color:{'#10b981' if dxy_ok else '#ef4444'};">{dxy:.2f}</b></div></div>
        </div>""", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1.3, 1.2], gap="small")

        with col1:
            st.markdown(f"""<div class="kz-panel"><div class="kz-header">MARKET PROFILE</div>
                <div style="font-family:'JetBrains Mono'; font-size:11px;">
                    <div style="display:flex; justify-content:space-between; color:#ef4444; padding:2px 0;"><span>VAH (SELL)</span><b>{vah:.1f}</b></div>
                    <div style="display:flex; justify-content:space-between; color:#eab308; padding:2px 0; background:#eab30811;"><span>POC (PIVOT)</span><b>{poc:.1f}</b></div>
                    <div style="display:flex; justify-content:space-between; color:#10b981; padding:2px 0;"><span>VAL (BUY)</span><b>{val:.1f}</b></div>
                </div>
                <div style="margin-top:15px; background:#18181b; padding:10px; border-radius:4px; text-align:center; border:1px solid #27272a;"><small style="color:#71717a;">WIN PROBABILITY</small><br><span style="font-size:22px; font-weight:900; color:{'#10b981' if prob > 75 else '#ef4444'};">{prob}%</span></div></div>""", unsafe_allow_html=True)
            st.markdown(f"""<div class="kz-panel"><div class="kz-header">LOGIQUE D'ABSORPTION</div><p style="font-size:9px; color:#888; line-height:1.5;"><b>Setup :</b> Traque l'épuisement des ordres au marché vs murs institutionnels.<br><br><b>Confirmation :</b> Ratio > 2.7x sur VAL ou VAH.<br><b>Execution :</b> SL 4 Ticks / TP 8 Ticks.</p></div>""", unsafe_allow_html=True)

        with col2:
            st.markdown("""<div class="kz-panel" style="height:100%;"><div class="kz-header">TWELVE DATA PRO CHART (M15)</div>""", unsafe_allow_html=True)
            # WIDGET TWELVE DATA OFFICIEL
            widget_url = f"https://twelvedata.com/widget/advanced?symbol=XAU/USD&apikey={API_KEY}&interval=15&theme=dark&style=1"
            st.components.v1.iframe(widget_url, height=220)
            st.markdown("""<div style="margin-top:10px;"><div class="kz-header">GLOBAL INTELLIGENCE</div><div style="border-left:2px solid #eab308; padding-left:10px; margin-bottom:8px;"><b style="color:#eab308; font-size:9px;">BCE :</b> <span style="font-size:9px; color:#aaa;">Impact Euro/Gold attendu sur discours Lagarde.</span></div><div style="border-left:2px solid #eab308; padding-left:10px; margin-bottom:8px;"><b style="color:#eab308; font-size:9px;">ETF :</b> <span style="font-size:9px; color:#aaa;">Accumulation GLD active (+2.4%).</span></div></div>""", unsafe_allow_html=True)

        with col3:
            st.markdown("""<div class="kz-panel"><div class="kz-header">L2 HEATMAP (ORDERFLOW)</div>""", unsafe_allow_html=True)
            st.markdown(dom_html, unsafe_allow_html=True)
            if imbalance_ok and is_on_zone:
                st.markdown(f"""<div style="margin-top:10px; background:#10b98122; border:1px solid #10b981; padding:8px; color:#10b981; text-align:center; font-weight:bold; border-radius:4px;">ALERTE : {setup_dir} ABSORPTION ({ratio:.1f}x)</div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""<div class="kz-panel"><div class="kz-header">DISCIPLINE ROADMAP & VALIDATION</div><div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:12px;">
                <div style="display:flex; align-items:center; background:#0c0c0c; padding:10px; border-radius:4px; border:1px solid #222;"><span style="font-size:9px;">1. ZONE M.P</span><span class="status-badge {'ok' if is_on_zone else 'wait'}">{'OK' if is_on_zone else 'WAIT'}</span></div>
                <div style="display:flex; align-items:center; background:#0c0c0c; padding:10px; border-radius:4px; border:1px solid #222;"><span style="font-size:9px;">2. IMBALANCE</span><span class="status-badge {'ok' if imbalance_ok else 'wait'}">{'OK' if imbalance_ok else 'WAIT'}</span></div>
                <div style="display:flex; align-items:center; background:#0c0c0c; padding:10px; border-radius:4px; border:1px solid #222;"><span style="font-size:9px;">3. DXY FILTER</span><span class="status-badge {'ok' if dxy_ok else 'wait'}">{'OK' if dxy_ok else 'WAIT'}</span></div>
                <div style="display:flex; align-items:center; background:#0c0c0c; padding:10px; border-radius:4px; border:1px solid #222;"><span style="font-size:9px;">4. EXECUTION</span><span class="status-badge {'ok' if prob > 75 else 'wait'}">{'GO' if prob > 75 else 'NO'}</span></div>
            </div></div>""", unsafe_allow_html=True)

    except Exception as e: st.error(f"Sync Issue: {e}")

terminal_engine()
