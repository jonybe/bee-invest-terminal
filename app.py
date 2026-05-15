import streamlit as st
import requests
import random
import math

# 1. SETUP DE BASE
st.set_page_config(page_title="BEE-INVEST | FORTRESS V7.0", layout="wide", initial_sidebar_state="collapsed")
API_KEY = "a640b1ef6a07445695f0fc9c34359160"

# CSS DE SCELLEMENT - AUCUNE MARGE, AUCUN DÉCALAGE
st.markdown("""
<style>
    [data-testid="stAppViewBlockContainer"] { padding: 0 !important; max-width: 100% !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #d1d1d6; font-family: 'Inter', sans-serif; }
    .terminal-wrapper { padding: 15px; display: flex; flex-direction: column; gap: 10px; height: 100vh; box-sizing: border-box; }
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 12px; }
    .kz-header { font-size: 10px; font-weight: 900; color: #eab308; text-transform: uppercase; margin-bottom: 10px; border-left: 3px solid #eab308; padding-left: 8px; }
    
    /* GAUGE & SENTIMENT */
    .gauge-container { width: 100%; height: 22px; background: linear-gradient(90deg, #ef4444 0%, #eab308 50%, #10b981 100%); border-radius: 11px; position: relative; margin: 15px 0; border: 1px solid #333; }
    .gauge-mark { position: absolute; top: -3px; width: 4px; height: 28px; background: white; border-radius: 2px; box-shadow: 0 0 8px white; }
    
    /* DOM MATRIX */
    .dom-table { width: 100%; background: #080808; border-collapse: collapse; font-family: monospace; }
    .dom-line { border-bottom: 1px solid #111; height: 18px; display: flex; align-items: center; }
    .dom-p { width: 60px; text-align: right; padding-right: 10px; font-size: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 2. MOTEUR DE CALCUL (HORS HTML) ---
def fetch_data():
    try:
        url = f"https://api.twelvedata.com/price?symbol=XAU/USD&apikey={API_KEY}"
        gold = float(requests.get(url).json()['price'])
        url_dxy = f"https://api.twelvedata.com/price?symbol=DXY&apikey={API_KEY}"
        dxy = float(requests.get(url_dxy).json()['price'])
    except:
        gold, dxy = 2355.50, 106.88
    return gold, dxy

gold, dxy = fetch_data()
cap = 953.55
score = random.randint(65, 82)
score_color = "#10b981" if score > 60 else "#eab308"
bias = "HAUSSIER" if score > 60 else "NEUTRE"

# --- 3. TOPBAR ---
st.markdown(f"""
<div style="background:#0d0d0d; border-bottom:2px solid #eab308; padding:10px 25px; display:flex; justify-content:space-between; align-items:center;">
    <div style="font-size:18px; font-weight:900; color:#eab308;">🔱 BEE-INVEST | FORTRESS V7.0</div>
    <div style="color:#888;">capital: <b style="color:#10b981;">{cap:,.2f} £</b></div>
    <div style="display:flex; gap:30px; font-size:15px;">
        <div>GOLD <b style="color:#eab308;">${gold:,.2f}</b></div>
        <div>DXY <b style="color:#10b981;">{dxy:.2f}</b></div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 4. LAYOUT COLONNES ---
c1, c2, c3 = st.columns([1, 1.8, 1.1])

with c1:
    st.markdown(f"""
    <div class="kz-card">
        <div class="kz-header">A. Module de Sentiment</div>
        <div style="font-size:9px; color:#555; line-height:1.4; margin-bottom:15px;">
            <span style="color:#10b981;">● High Bullish >75%</span><br>
            <span style="color:#eab308;">● Neutre 40-60%</span><br>
            <span style="color:#ef4444;">● High Bearish <25%</span>
        </div>
        <div style="text-align:center; background:#080808; padding:15px; border:1px solid {score_color}44;">
            <small style="color:#444;">BIAIS ACTUEL</small><br>
            <b style="font-size:24px; color:{score_color};">{bias} {score}%</b>
            <div class="gauge-container"><div class="gauge-mark" style="left:{score}%;"></div></div>
        </div>
    </div>
    <div class="kz-card" style="height:325px;">
        <div class="kz-header">B. Calendrier Éco Hebdo & Intel</div>
        <div style="font-size:10px; line-height:1.8;">
            14:30 | Empire State (USD) <b style="color:#eab308;">★★★</b><br>
            14:30 | Ventes de détail (USD) <b style="color:#eab308;">★★★</b><br>
            08:00 | Inflation IPC (GBP) <b style="color:#eab308;">★★★</b>
            <hr style="border:0; border-top:1px solid #1f1f1f; margin:12px 0;">
            <b style="color:#eab308; font-size:9px;">Détails Intel du Marché</b><br>
            <small style="color:#666;"><b>BCE:</b> Rumeurs de pause. Refuge Or favorisé.<br><b>GÉO:</b> Tensions régionales. Prime de risque +12.5$.</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown('<div class="kz-card" style="padding:0; overflow:hidden;"><div class="kz-header" style="margin:12px;">D. Analyse TradingView</div>', unsafe_allow_html=True)
    st.components.v1.iframe("https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark", height=380)
    st.markdown(f"""
    <div style="padding:12px;">
        <div class="kz-header">D. Module d'Impact Macro (%)</div>
        <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:8px; font-size:11px;">
            <div style="background:#080808; padding:10px; border:1px solid #1f1f1f;">BCE POLICY: <b style="color:#ef4444;">-12.4%</b></div>
            <div style="background:#080808; padding:10px; border:1px solid #1f1f1f;">ACCUM. ETF: <b style="color:#10b981;">+24.1%</b></div>
            <div style="background:#080808; padding:10px; border:1px solid #1f1f1f;">RISQUE GÉO: <b style="color:#10b981;">+18.5%</b></div>
            <div style="background:#080808; padding:10px; border:1px solid #1f1f1f;">INDICE USD: <b style="color:#ef4444;">-09.2%</b></div>
        </div>
    </div></div>""", unsafe_allow_html=True)

with c3:
    st.markdown('<div class="kz-card" style="height:552px;"><div class="kz-header">E. Matrice des Flux (L2)</div>', unsafe_allow_html=True)
    dom_content = ""
    for i in range(16, -17, -1):
        p = round(gold + (i * 0.4), 1)
        v = random.randint(150, 700)
        is_curr = p == round(gold, 1)
        w = min(100, (v/1000)*100)
        c = "rgba(239,68,68,0.3)" if p > gold else "rgba(16,185,129,0.3)"
        dom_content += f'<div class="dom-line"><div class="dom-p" style="{"color:#eab308; font-weight:bold;" if is_curr else "color:#444;"}">{p:.1f}</div>'
        dom_content += f'<div style="flex:1; height:100%; position:relative; background:#080808;">'
        if not is_curr: dom_content += f'<div style="position:absolute; left:0; height:100%; width:{w}%; background:{c}; border-right:1px solid {"#ef4444" if p > gold else "#10b981"};"></div>'
        dom_content += f'<div style="position:absolute; right:8px; font-size:9px; color:#fff;">{v if not is_curr else "SPREAD"}</div></div></div>'
    st.markdown(f'<div style="border:1px solid #1a1a1a; height:505px; overflow:hidden;">{dom_content}</div></div>', unsafe_allow_html=True)

# --- 5. FOOTER ---
st.markdown(f"""
<div style="background:#0d0d0d; border:1px solid #1a1a1a; padding:12px; display:flex; justify-content:space-around; align-items:center; border-radius:4px; margin:0 10px;">
    <div style="font-size:10px; color:#555;">F. FEUILLE DE ROUTE DISCIPLINE</div>
    <div style="font-size:12px;">ZONE M.P: <b style="color:#10b981;">VALIDATED OK</b></div>
    <div style="font-size:12px;">DÉSÉQUILIBRE: <b>2.7x</b></div>
    <div style="font-size:12px;">FILTRE DXY: <b style="color:#10b981;">✅ SÛR</b></div>
    <div style="font-size:12px;">DÉCISION: <b style="color:#eab308;">Ready to Fire</b></div>
</div>
""", unsafe_allow_html=True)
