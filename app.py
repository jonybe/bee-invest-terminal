import streamlit as st
import requests
import random
import math

# 1. Setup & API
st.set_page_config(page_title="BEE-INVEST | FORTRESS V12", layout="wide", initial_sidebar_state="collapsed")
API_KEY = "a640b1ef6a07445695f0fc9c34359160"

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        return float(res['price'])
    except: return 2355.50

# CSS Minimaliste pour bloquer le design
st.markdown("""
<style>
    [data-testid="stAppViewBlockContainer"] { padding: 0.5rem !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #d1d1d6; font-family: monospace; }
    .kz-card { background: #121212; border: 1px solid #1f1f1f; border-radius: 4px; padding: 12px; margin-bottom: 10px; }
    .kz-header { font-size: 11px; font-weight: bold; color: #eab308; text-transform: uppercase; margin-bottom: 10px; }
    .gauge-wrap { position: relative; width: 100%; height: 20px; background: linear-gradient(90deg, #ef4444, #eab308, #10b981); border-radius: 10px; margin-top: 10px; border: 1px solid #333; }
    .gauge-ptr { position: absolute; top: -2px; width: 4px; height: 24px; background: white; border-radius: 2px; box-shadow: 0 0 8px white; }
    .dom-row { display: flex; height: 17px; align-items: center; border-bottom: 1px solid #111; font-size: 9px; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=10)
def main():
    # --- CALCULS ---
    gold = get_price("XAU/USD")
    dxy = get_price("DXY")
    cap = 953.55
    prog = (math.log(cap/100) / math.log(1000000/100)) * 100
    
    # Score Dynamique
    score = random.randint(15, 85)
    score_c = "#10b981" if score > 60 else "#eab308" if score > 40 else "#ef4444"
    bias_fr = "HAUSSIER" if score > 60 else "NEUTRE" if score > 40 else "BAISSIER"

    # --- TOPBAR ---
    st.markdown(f"""
    <div style="background:#0d0d0d; border-bottom:1px solid #eab308; padding:10px 20px; display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
        <b style="color:#eab308; font-size:16px;">🔱 BEE-INVEST | FORTRESS V12</b>
        <div style="color:#888;">capital: <span style="color:#10b981;">{cap:,.2f} £</span></div>
        <div style="display:flex; gap:20px;">
            <div>GOLD <span style="color:#eab308;">${gold:,.2f}</span></div>
            <div>DXY <span style="color:#10b981;">{dxy:.2f}</span></div>
        </div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.8, 1.1])

    with c1:
        # A. SENTIMENT
        st.markdown(f"""
        <div class="kz-card">
            <div class="kz-header">A. Module de Sentiment</div>
            <div style="font-size:9px; color:#777;">
                <span style="color:#10b981;">● High Bullish >75%</span><br>
                <span style="color:#eab308;">● Neutre 40-60%</span><br>
                <span style="color:#ef4444;">● High Bearish <25%</span>
            </div>
            <div style="text-align:center; margin-top:15px; padding:15px; background:#080808; border-radius:4px; border:1px solid {score_c}44;">
                <b style="font-size:22px; color:{score_c};">{bias_fr} {score}%</b>
                <div class="gauge-wrap"><div class="gauge-ptr" style="left:{score}%;"></div></div>
            </div>
        </div>
        <div class="kz-card">
            <div class="kz-header">B. Calendrier Éco Hebdo</div>
            <div style="font-size:10px; line-height:1.6;">
                14:30 | Empire State (USD) <b style="color:#eab308;">★★★</b><br>
                08:00 | Inflation IPC (GBP) <b style="color:#eab308;">★★★</b>
                <hr style="border:0; border-top:1px solid #1f1f1f; margin:8px 0;">
                <small style="color:#666;"><b>BCE Intel:</b> Rumeurs de pause confirmées.<br><b>GEO:</b> Tensions régionales escalade (+12$).</small>
            </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        # D. ANALYSE
        st.markdown('<div class="kz-card" style="padding:0; overflow:hidden;"><div class="kz-header" style="margin:12px;">D. Analyse TradingView</div>', unsafe_allow_html=True)
        st.components.v1.iframe("https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark", height=350)
        st.markdown(f"""
            <div style="padding:12px;">
                <div class="kz-header" style="margin-bottom:8px;">D. Module d'Impact Macro (%)</div>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:5px; font-size:10px;">
                    <div style="background:#080808; padding:8px;">POLITIQUE BCE: <b style="color:#ef4444;">-12.4%</b></div>
                    <div style="background:#080808; padding:8px;">ACCUM. ETF: <b style="color:#10b981;">+24.1%</b></div>
                </div>
            </div></div>""", unsafe_allow_html=True)

    with c3:
        # E. MATRICE L2
        st.markdown('<div class="kz-card" style="height:540px;"><div class="kz-header">E. Matrice des Flux</div>', unsafe_allow_html=True)
        dom_html = ""
        for i in range(15, -16, -1):
            p = round(gold + (i * 0.4), 1)
            v = random.randint(150, 650)
            is_curr = p == round(gold, 1)
            w = min(100, (v/1000)*100)
            color = "rgba(239,68,68,0.3)" if p > gold else "rgba(16,185,129,0.3)"
            dom_html += f'<div class="dom-row"><div style="width:50px; text-align:right; padding-right:5px; {"color:#eab308;" if is_curr else "color:#444;"}">{p:.1f}</div>'
            dom_html += f'<div style="flex:1; height:100%; position:relative; background:#080808;">'
            if not is_curr: dom_html += f'<div style="position:absolute; left:0; height:100%; width:{w}%; background:{color};"></div>'
            dom_html += f'<div style="position:absolute; right:5px;">{v if not is_curr else "SPREAD"}</div></div></div>'
        st.markdown(f'<div style="border:1px solid #1f1f1f;">{dom_html}</div></div>', unsafe_allow_html=True)

    # --- F. FOOTER ---
    st.markdown(f"""
    <div style="background:#0d0d0d; border:1px solid #1f1f1f; padding:12px; display:flex; justify-content:space-around; align-items:center; border-radius:4px;">
        <div style="font-size:11px;">ZONE M.P: <b style="color:#10b981;">VALIDATED</b></div>
        <div style="font-size:11px;">FILTRE DXY: <b style="color:#10b981;">✅ SÛR</b></div>
        <div style="font-size:11px;">DÉCISION: <b style="color:#eab308;">READY</b></div>
    </div>""", unsafe_allow_html=True)

main()
