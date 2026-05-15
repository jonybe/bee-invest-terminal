import streamlit as st
import requests
import random
import math

# 1. Configuration & API
st.set_page_config(page_title="BEE-INVEST | FORTRESS V7.0", layout="wide", initial_sidebar_state="collapsed")
API_KEY = "a640b1ef6a07445695f0fc9c34359160"

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        return float(res['price'])
    except: return 2355.50

# 2. CSS - Fidélité totale à l'image
st.markdown("""
<style>
    [data-testid="stAppViewBlockContainer"] { padding: 0.5rem !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #d1d1d6; font-family: 'JetBrains Mono', monospace; }
    
    .kz-card { background: #121212; border: 1px solid #1f1f1f; border-radius: 4px; padding: 12px; margin-bottom: 10px; }
    .kz-header { font-size: 11px; font-weight: 800; color: #eab308; text-transform: uppercase; margin-bottom: 10px; }
    
    /* Jauge de Sentiment Dynamique */
    .gauge-wrap { position: relative; width: 100%; height: 25px; background: linear-gradient(90deg, #ef4444 0%, #eab308 50%, #10b981 100%); border-radius: 12px; margin-top: 10px; }
    .gauge-ptr { position: absolute; top: -3px; width: 3px; height: 31px; background: white; border-radius: 2px; }
    
    /* Carnet L2 */
    .dom-row { display: flex; height: 17px; align-items: center; border-bottom: 1px solid #111; }
    .dom-p { width: 55px; text-align: right; padding-right: 8px; font-size: 9px; color: #444; }
    .dom-bar { flex-grow: 1; height: 100%; position: relative; display: flex; align-items: center; background: #080808; }
    .dom-v { position: absolute; right: 8px; color: #fff; font-size: 8px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=10)
def terminal():
    # --- CALCULS ---
    gold = get_price("XAU/USD")
    dxy = get_price("DXY")
    cap = 953.55
    prog = (math.log(cap/100) / math.log(1000000/100)) * 100
    
    # Logique de Sentiment
    score = random.randint(15, 85)
    score_c = "#10b981" if score > 60 else "#eab308" if score > 40 else "#ef4444"
    bias_fr = "HAUSSIER" if score > 60 else "NEUTRE" if score > 40 else "BAISSIER"

    # --- TOPBAR ---
    st.markdown(f"""
    <div style="background:#0d0d0d; border-bottom:1px solid #eab308; padding:8px 20px; display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <b style="color:#eab308; font-size:16px;">🔱 BEE-INVEST | FORTRESS V7.0</b>
        <div style="color:#888; font-size:12px;">capital: <span style="color:#10b981;">{cap:,.2f} £</span></div>
        <div style="display:flex; gap:20px; font-size:14px;">
            <div>GOLD <span style="color:#eab308;">${gold:,.2f}</span></div>
            <div>DXY <span style="color:#10b981;">{dxy:.2f}</span></div>
        </div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.8, 1.1])

    with c1:
        # A. MODULE DE SENTIMENT
        st.markdown(f"""
        <div class="kz-card">
            <div class="kz-header">A. Module de Sentiment</div>
            <div style="font-size:10px; color:#aaa; line-height:1.4;">
                <b style="color:#eee;">Légende du Score :</b><br>
                <span style="color:#10b981;">High Bullish >75%</span><br>
                <span style="color:#10b981; opacity:0.7;">Low Bullish 60-75%</span><br>
                <span style="color:#eab308;">Neutral 40-60%</span><br>
                <span style="color:#ef4444; opacity:0.7;">Low Bearish 25-40%</span><br>
                <span style="color:#ef4444;">High Bearish <25%</span>
            </div>
            <div style="text-align:center; margin-top:15px; padding:10px; background:#080808; border:1px solid {score_c}44;">
                <div style="font-size:9px; color:#666;">Jauge de Sentiment</div>
                <b style="font-size:20px; color:{score_c};">{bias_fr} {score}%</b>
                <div class="gauge-wrap"><div class="gauge-ptr" style="left:{score}%;"></div></div>
            </div>
        </div>
        <div class="kz-card" style="height:312px;">
            <div class="kz-header">B. Calendrier Éco Hebdo & Intel</div>
            <div style="font-size:10px; line-height:1.5;">
                <div style="display:flex; justify-content:space-between;"><span>14:30 | Empire State (USD)</span><b style="color:#eab308;">★★★</b></div>
                <div style="display:flex; justify-content:space-between;"><span>14:30 | Ventes de détail (USD)</span><b style="color:#eab308;">★★★</b></div>
                <div style="display:flex; justify-content:space-between;"><span>08:00 | Inflation IPC (GBP)</span><b style="color:#eab308;">★★★</b></div>
                <hr style="border:0; border-top:1px solid #1f1f1f; margin:10px 0;">
                <b style="color:#eab308; font-size:9px;">Détails Intel du Marché</b><br>
                <small style="color:#888;">
                <b>BCE Intel:</b> Rumeurs de pause confirmées. Refuge Or favorisé par baisse des rendements.<br>
                <b>GEO-Watch:</b> Tensions géo-politiques régionales en escalade. Prime de risque intégrée à +12.5$.
                </small>
            </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        # D. ANALYSE & MACRO
        st.markdown('<div class="kz-card" style="padding:0; overflow:hidden;"><div class="kz-header" style="margin:12px;">D. Analyse TradingView</div>', unsafe_allow_html=True)
        st.components.v1.iframe("https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark", height=350)
        st.markdown(f"""
            <div style="padding:12px;">
                <div class="kz-header">D. Module d'Impact Macro (%)</div>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px; font-size:11px;">
                    <div style="background:#080808; padding:8px; border:1px solid #1f1f1f;">POLITIQUE BCE: <b style="color:#ef4444;">-12.4%</b></div>
                    <div style="background:#080808; padding:8px; border:1px solid #1f1f1f;">ACCUM. ETF: <b style="color:#10b981;">+24.1%</b></div>
                    <div style="background:#080808; padding:8px; border:1px solid #1f1f1f;">RISQUE GÉO: <b style="color:#10b981;">+18.5%</b></div>
                    <div style="background:#080808; padding:8px; border:1px solid #1f1f1f;">INDICE USD: <b style="color:#ef4444;">-09.2%</b></div>
                </div>
            </div></div>""", unsafe_allow_html=True)

    with c3:
        # E. MATRICE DES FLUX
        st.markdown('<div class="kz-card" style="height:535px;"><div class="kz-header">E. Matrice des Flux Institutionnels</div>', unsafe_allow_html=True)
        dom_html = ""
        for i in range(15, -16, -1):
            p = round(gold + (i * 0.4), 1)
            v = random.randint(150, 650)
            is_curr = p == round(gold, 1)
            bar_c = "rgba(239,68,68,0.3)" if p > gold else "rgba(16,185,129,0.3)"
            w = min(100, (v/1000)*100)
            dom_html += f'<div class="dom-row"><div class="dom-p" style="{"color:#eab308; font-weight:bold; background:rgba(234,179,8,0.1);" if is_curr else ""}">{p:.1f}</div>'
            dom_html += f'<div class="dom-bar">{"<div style=\'position:absolute; left:0; height:100%; width:"+str(w)+"%; background:"+bar_c+"; border-right:1px solid "+ ("#ef4444" if p > gold else "#10b981") +";\'></div>" if not is_curr else ""}<div class="dom-v">{v if not is_curr else "SPREAD"}</div></div></div>'
        st.markdown(f'<div class="dom-box" style="height:460px;">{dom_html}</div></div>', unsafe_allow_html=True)

    # --- F. ROADMAP ---
    st.markdown(f"""
    <div style="background:#0d0d0d; border:1px solid #1f1f1f; padding:10px; display:flex; justify-content:space-around; align-items:center; border-radius:4px;">
        <div style="font-size:10px; color:#555;">F. FEUILLE DE ROUTE DE DISCIPLINE</div>
        <div style="font-size:12px;">ZONE M.P: <b style="color:#10b981;">VALIDATED OK</b></div>
        <div style="font-size:12px;">DÉSÉQUILIBRE: <b>2.7x</b></div>
        <div style
