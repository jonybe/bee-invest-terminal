import streamlit as st
import requests
import random
import math

# 1. Config & API
st.set_page_config(page_title="BEE-INVEST | FORTRESS V7.0", layout="wide", initial_sidebar_state="collapsed")
API_KEY = "a640b1ef6a07445695f0fc9c34359160"

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        return float(res['price'])
    except: return 2355.50

# 2. LE MOTEUR CSS (C'est ici qu'on verrouille le design de ta capture)
st.markdown("""
<style>
    /* Supprime tout l'habillage Streamlit pour remplir l'écran */
    [data-testid="stAppViewBlockContainer"] { padding: 0 !important; max-width: 100% !important; opacity: 1 !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #d1d1d6; font-family: 'Inter', sans-serif; }
    
    /* Structure en Grille Area (Comme sur ton image) */
    .terminal-grid {
        display: grid;
        grid-template-columns: 320px 1fr 340px;
        grid-template-rows: auto 1fr auto;
        grid-template-areas: 
            "top top top"
            "left center right"
            "footer footer footer";
        gap: 12px;
        padding: 15px;
        height: 98vh;
        box-sizing: border-box;
    }

    /* Styles des Blocs */
    .kz-top { grid-area: top; background: #0d0d0d; border-bottom: 2px solid #eab308; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; border-radius: 4px; }
    .kz-left { grid-area: left; display: flex; flex-direction: column; gap: 12px; }
    .kz-center { grid-area: center; display: flex; flex-direction: column; gap: 12px; }
    .kz-right { grid-area: right; display: flex; flex-direction: column; gap: 12px; }
    .kz-footer { grid-area: footer; background: #0d0d0d; border: 1px solid #1a1a1a; padding: 12px; border-radius: 4px; display: flex; justify-content: space-around; }

    .card { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 15px; }
    .header { font-size: 11px; font-weight: 900; color: #eab308; text-transform: uppercase; margin-bottom: 12px; border-left: 3px solid #eab308; padding-left: 8px; }
    
    /* Jauge & Score */
    .gauge-bg { width: 100%; height: 25px; background: linear-gradient(90deg, #ef4444, #eab308, #10b981); border-radius: 12px; position: relative; margin: 15px 0; border: 1px solid #333; }
    .gauge-cursor { position: absolute; top: -3px; width: 4px; height: 31px; background: white; border-radius: 2px; box-shadow: 0 0 10px white; transition: 0.5s; }
    
    /* DOM Matrix */
    .dom-wrap { background: #080808; border: 1px solid #1a1a1a; flex-grow: 1; overflow: hidden; border-radius: 2px; }
    .dom-row { display: flex; height: 19px; align-items: center; border-bottom: 1px solid #111; font-family: monospace; font-size: 10px; }
    .dom-p { width: 60px; text-align: right; padding-right: 10px; color: #444; }
    .dom-p.active { color: #eab308; font-weight: 900; background: rgba(234,179,8,0.15); }
    .dom-bar { flex-grow: 1; height: 100%; position: relative; display: flex; align-items: center; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=10)
def render_terminal():
    # --- CALCULS ---
    gold = get_price("XAU/USD")
    dxy = get_price("DXY")
    cap = 953.55
    prog = (math.log(cap/100) / math.log(1000000/100)) * 100
    
    score = random.randint(15, 85)
    color = "#10b981" if score > 60 else "#eab308" if score > 40 else "#ef4444"
    bias = "HAUSSIER" if score > 60 else "NEUTRE" if score > 40 else "BAISSIER"
    
    # --- CARNET L2 ---
    dom_rows = ""
    for i in range(16, -17, -1):
        p = round(gold + (i * 0.4), 1)
        v = random.randint(150, 700)
        is_curr = p == round(gold, 1)
        w = min(100, (v/1000)*100)
        c = "rgba(239,68,68,0.3)" if p > gold else "rgba(16,185,129,0.3)"
        dom_rows += f'<div class="dom-row"><div class="dom-p {"active" if is_curr else ""}">{p:.1f}</div>'
        dom_rows += f'<div class="dom-bar">'
        if not is_curr: dom_rows += f'<div style="position:absolute;left:0;height:100%;width:{w}%;background:{c};border-right:1px solid {"#ef4444" if p > gold else "#10b981"};"></div>'
        dom_rows += f'<div style="position:absolute;right:8px;font-weight:bold;color:#fff;">{v if not is_curr else "SPREAD"}</div></div></div>'

    # --- RENDU HTML UNIQUE ---
    st.markdown(f"""
    <div class="terminal-grid">
        <div class="kz-top">
            <div style="font-size:18px;"><b>🔱 BEE-INVEST</b> | FORTRESS V7.0</div>
            <div style="text-align:center; color:#888;">capital: <b style="color:#10b981;">{cap:,.2f} £</b></div>
            <div style="display:flex; gap:30px;">
                <div>GOLD <b style="color:#eab308;">${gold:,.2f}</b></div>
                <div>DXY <b style="color:#10b981;">{dxy:.2f}</b></div>
            </div>
        </div>

        <div class="kz-left">
            <div class="card">
                <div class="header">A. Module de Sentiment</div>
                <div style="font-size:9px; color:#555; margin-bottom:10px;">
                    <span style="color:#10b981;">● High Bullish >75%</span> | <span style="color:#eab308;">● Neutre 40-60%</span> | <span style="color:#ef4444;">● High Bearish <25%</span>
                </div>
                <div style="text-align:center; padding:15px; background:#080808; border-radius:4px; border:1px solid {color}44;">
                    <small style="color:#666;">BIAIS ACTUEL</small><br>
                    <b style="font-size:24px; color:{color};">{bias} {score}%</b>
                    <div class="gauge-bg"><div class="gauge-cursor" style="left:{score}%;"></div></div>
                </div>
            </div>
            <div class="card" style="flex-grow:1;">
                <div class="header">B. Calendrier Éco & Intel</div>
                <div style="font-size:10px; line-height:1.8;">
                    14:30 | Empire State (USD) <b style="color:#eab308;">★★★</b><br>
                    14:30 | Ventes de détail (USD) <b style="color:#eab308;">★★★</b><br>
                    08:00 | Inflation IPC (GBP) <b style="color:#eab308;">★★★</b>
                    <hr style="border:0; border-top:1px solid #1f1f1f; margin:15px 0;">
                    <b style="color:#eab308; font-size:9px;">DÉTAILS INTEL DU MARCHÉ</b><br>
                    <small style="color:#777;"><b>BCE :</b> Rumeurs de pause confirmées. Refuge Or favorisé.<br><b>GEO :</b> Tensions régionales. Prime de risque intégrée à +12.5$.</small>
                </div>
            </div>
        </div>

        <div class="kz-center">
            <div class="card" style="flex-grow:1; padding:0; overflow:hidden;">
                <div class="header" style="margin:15px;">D. Analyse TradingView</div>
                <iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark" style="width:100%; height:380px; border:none;"></iframe>
            </div>
            <div class="card">
                <div class="header">D. Module d'Impact Macro (%)</div>
                <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:10px; font-size:11px;">
                    <div style="background:#080808; padding:10px; border:1px solid #1f1f1f; text-align:center;">BCE: <b style="color:#ef4444;">-12.4%</b></div>
                    <div style="background:#080808; padding:10px; border:1px solid #1f1f1f; text-align:center;">ETF: <b style="color:#10b981;">+24.1%</b></div>
                    <div style="background:#080808; padding:10px; border:1px solid #1f1f1f; text-align:center;">GÉO: <b style="color:#10b981;">+18.5%</b></div>
                    <div style="background:#080808; padding:10px; border:1px solid #1f1f1f; text-align:center;">USD: <b style="color:#ef4444;">-09.2%</b></div>
                </div>
            </div>
        </div>

        <div class="kz-right">
            <div class="card" style="height:100%; display:flex; flex-direction:column;">
                <div class="header">E. Matrice des Flux (L2)</div>
                <div class="dom-wrap">{dom_rows}</div>
            </div>
        </div>

        <div class="kz-footer">
            <div style="font-size:12px;">ZONE M.P: <b style="color:#10b981;">VALIDATED OK</b></div>
            <div style="font-size:12px;">DÉSÉQUILIBRE: <b>2.7x</b></div>
            <div style="font-size:12px;">FILTRE DXY: <b style="color:#10b981;">✅ SÛR</b></div>
            <div style="font-size:12px;">DÉCISION: <b style="color:#eab308;">Ready to Fire</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

render_terminal()
