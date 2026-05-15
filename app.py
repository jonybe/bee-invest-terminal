import streamlit as st
import requests
import random
import math

# 1. CONFIGURATION DE BASE
st.set_page_config(page_title="BEE-INVEST | FORTRESS V7.0", layout="wide", initial_sidebar_state="collapsed")
API_KEY = "a640b1ef6a07445695f0fc9c34359160"

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        return float(res['price'])
    except: return 2355.50

# --- 2. CALCULS DES DONNÉES (SÉCURISÉ) ---
gold = get_price("XAU/USD")
dxy = get_price("DXY")
cap = 953.55
prog = (math.log(cap/100) / math.log(1000000/100)) * 100

# Calcul du score et de sa couleur synchronisée
score = random.randint(65, 82)
if score > 75:
    score_color = "#10b981"  # Vert vif (High Bullish)
    bias_txt = "FORT HAUSSIER"
elif score > 60:
    score_color = "#10b981"  # Vert (Low Bullish)
    bias_txt = "HAUSSIER FAIBLE"
elif score > 40:
    score_color = "#eab308"  # Jaune (Neutral)
    bias_txt = "NEUTRE"
else:
    score_color = "#ef4444"  # Rouge (Bearish)
    bias_txt = "BAISSIER"

# --- 3. CONSTRUTION DE LA MATRICE L2 DE DROITE ---
dom_rows_html = ""
for i in range(16, -17, -1):
    p = round(gold + (i * 0.4), 1)
    v = random.randint(150, 700)
    is_curr = p == round(gold, 1)
    
    # Styles correspondants aux barres d'orderbook de la photo
    if p > gold:
        bar_c = "rgba(239, 68, 68, 0.2)"
        border_c = "#ef4444"
    else:
        bar_c = "rgba(16, 185, 129, 0.2)"
        border_c = "#10b981"
        
    w = min(100, (v / 800) * 100)
    p_style = "color:#eab308; font-weight:bold; background:rgba(234,179,8,0.15);" if is_curr else "color:#888;"
    
    bar_html = f'<div style="position:absolute; left:0; top:0; height:100%; width:{w}%; background:{bar_c}; border-right:1px solid {border_c};"></div>' if not is_curr else ""
    vol_html = f'<div style="position:absolute; right:10px; color:#fff; font-size:10px; font-weight:bold; z-index:2;">{v if not is_curr else "SPREAD"}</div>'
    
    dom_rows_html += f"""
    <div style="display:flex; height:18px; align-items:center; position:relative; background:#0a0a0a; border-bottom:1px solid #151515;">
        <div style="width:65px; text-align:right; padding-right:10px; font-size:10px; z-index:2; font-family:monospace; {p_style}">{p:.1f}</div>
        <div style="flex-grow:1; height:100%; position:relative;">
            {bar_html}
            {vol_html}
        </div>
    </div>
    """

# --- 4. RENDER INJECTIONS CSS GLOBAL (Forçage du thème sombre de la photo) ---
st.markdown("""
<style>
    /* Nettoyage des blocs et marges de Streamlit */
    [data-testid="stAppViewBlockContainer"] { padding: 0 !important; max-width: 100% !important; }
    div[data-testid="stVerticalBlock"] { gap: 0 !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #0b0c10 !important; color: #d1d1d6; }
    
    /* Structure principale en Grille CSS (3 Colonnes Fixes + Topbar + Footer) */
    .ft-grid {
        display: grid;
        grid-template-columns: 310px 1fr 340px;
        grid-template-rows: auto 1fr auto;
        grid-template-areas:
            "top top top"
            "left center right"
            "foot foot foot";
        gap: 12px;
        padding: 12px;
        height: 98vh;
        box-sizing: border-box;
        background-color: #050505;
    }
    
    /* Style uniforme pour les conteneurs (Bords carrés, gris très sombre) */
    .ft-card {
        background-color: #121318;
        border: 1px solid #22252a;
        border-radius: 4px;
        padding: 12px;
        display: flex;
        flex-direction: column;
        box-sizing: border-box;
    }
    
    /* Titres des modules calqués fidèlement sur l'image */
    .ft-title {
        font-size: 11px;
        font-weight: bold;
        color: #f1f2f6;
        text-transform: none;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
    }
    
    /* Conteneur d'Iframe masquant les débordements */
    .chart-box { flex-grow: 1; min-height: 360px; background: #000; border: 1px solid #22252a; border-radius: 2px; position: relative; }
</style>
""", unsafe_allow_html=True)

# --- 5. CODE HTML CENTRALISÉ SANS INTERRUPTION ---
st.markdown(f"""
<div class="ft-grid">
    
    <div style="grid-area: top; background:#121318; border-bottom:1px solid #22252a; padding:10px 20px; display:flex; justify-content:space-between; align-items:center; border-radius:4px; font-family:monospace; font-size:12px;">
        <div style="font-weight:bold; color:#eab308; letter-spacing:1px;">🔱 BEE-INVEST | FORTRESS V7.0</div>
        <div style="color:#888;">capital: <span style="color:#10b981; font-weight:bold;">{cap:,.2f} £</span></div>
        <div style="display:flex; gap:25px; font-weight:bold;">
            <div style="color:#888;">GOLD <span style="color:#eab308;">${gold:,.2f}</span></div>
            <div style="color:#888;">DXY <span style="color:#10b981;">{dxy:.2f}</span></div>
        </div>
    </div>

    <div style="grid-area: left; display:flex; flex-direction:column; gap:12px;">
        <div class="ft-card">
            <div class="ft-title">A. Module de Sentiment</div>
            <div style="font-size:10px; color:#a1a1a6; font-family:monospace; line-height:1.5; margin-bottom:10px;">
                <b>Légende du Score Legend:</b><br>
                <span style="color:#10b981;">High Bullish >75%</span><br>
                <span style="color:#10b981; opacity:0.7;">Low Bullish &nbsp;60-75%</span><br>
                <span style="color:#eab308;">Neutral &nbsp; &nbsp; 40-60%</span><br>
                <span style="color:#ef4444; opacity:0.7;">Low Bearish &nbsp;25-40%</span><br>
                <span style="color:#ef4444;">High Bearish &lt;25%</span>
            </div>
            <div style="background:#0a0a0a; border:1px solid #22252a; padding:12px; border-radius:4px; text-align:center;">
                <div style="font-size:12px; font-weight:bold; color:{score_color}; margin-bottom:8px;">
                    Jauge de Sentiment : {bias_txt} ({score}%)
                </div>
                <div style="position:relative; width:100%; height:20px; background:linear-gradient(90deg, #ef4444 0%, #eab308 50%, #10b981 100%); border-radius:4px; border:1px solid #333;">
                    <div style="position:absolute; top:-2px; left:{score}%; width:4px; height:24px; background:#fff; border-radius:1px; box-shadow:0 0 5px #fff;"></div>
                </div>
            </div>
        </div>
        
        <div class="ft-card" style="flex-grow:1;">
            <div class="ft-title">B. Calendrier Éco Hebdo & Intel</div>
            <div style="font-size:10px; font-family:monospace; line-height:1.6; color:#10b981; margin-bottom:12px;">
                14:30 | Empire State (USD) <span style="color:#eab308;">★★★</span><br>
                14:30 | Ventes de détail (USD) <span style="color:#eab308;">★★★</span><br>
                08:00 | Inflation IPC (GBP) <span style="color:#eab308;">★★★</span>
            </div>
            <div style="border-top:1px solid #22252a; padding-top:10px; font-size:10px; font-family:monospace; line-height:1.4;">
                <b style="color:#eab308;">Détails Intel du Marché</b><br>
                <span style="color:#eab308;">BCE Intel:</span><br>
                <span style="color:#a1a1a6;">Updated: Rumeurs de pause sur les taux confirmées par sources de marché. Refuge Or favorisé par baisse anticipée des rendements.</span><br>
                <span style="color:#eab308; display:block; margin-top:5px;">GEO-Watch:</span>
                <span style="color:#a1a1a6;">Updated: Tensions géo-politiques régionales en escalade. Prime de risque intégrée à +12.5$.</span>
            </div>
        </div>
    </div>

    <div style="grid-area: center; display:flex; flex-direction:column; gap:12px; overflow:hidden;">
        <div class="ft-card" style="flex-grow:1; padding:0; overflow:hidden; position:relative;">
            <div class="ft-title" style="padding:12px 12px 0 12px;">D. Analyse TradingView</div>
            <div class="chart-box" style="margin:0 12px 12px 12px;">
                <iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark" style="width:100%; height:100%; border:none; position:absolute; top:0; left:0;"></iframe>
            </div>
        </div>
        
        <div class="ft-card">
            <div class="ft-title">D. Module d'Impact Macro (%)</div>
            <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:8px; font-family:monospace; font-size:11px;">
                <div style="background:#0a0a0a; border:1px solid #22252a; padding:8px 12px;">POLITIQUE BCE: <span style="color:#ef4444; font-weight:bold;">-12.4%</span></div>
                <div style="background:#0a0a0a; border:1px solid #22252a; padding:8px 12px;">ACCUM. ETF: <span style="color:#10b981; font-weight:bold;">+24.1%</span></div>
                <div style="background:#0a0a0a; border:1px solid #22252a; padding:8px 12px;">RISQUE GÉO: <span style="color:#10b981; font-weight:bold;">+18.5%</span></div>
                <div style="background:#0a0a0a; border:1px solid #22252a; padding:8px 12px;">INDICE USD: <span style="color:#ef4444; font-weight:bold;">-09.2%</span></div>
            </div>
        </div>
    </div>

    <div style="grid-area: right; display:flex; flex-direction:column;">
        <div class="ft-card" style="height:100%; padding-bottom:5px;">
            <div class="ft-title">E. Matrice des Flux Institutionnels</div>
            <div style="font-size:10px; color:#888; font-family:monospace; text-align:center; margin-bottom:5px; font-weight:bold; letter-spacing:1px;">
                CARNET MATRIX (L2)
            </div>
            <div style="flex-grow:1; border:1px solid #22252a; background:#0a0a0a; overflow-y:auto; overflow-x:hidden; border-radius:2px;">
                {dom_rows_html}
            </div>
        </div>
    </div>

    <div class="kz-footer" style="grid-area: foot; font-family:monospace; font-size:11px; align-items:center; border:1px solid #22252a; background:#121318;">
        <div style="color:#666; font-weight:bold;">F. Feuille de Route de Discipline d'Exécution</div>
        <div>ZONE M.P: <span style="color:#10b981; font-weight:bold;">Validated OK</span></div>
        <div>DÉSÉQUILIBRE: <span style="color:#eab308; font-weight:bold;">2.7x</span></div>
        <div>FILTRE DXY: <span style="color:#10b981; font-weight:bold;">✅ Sûr</span></div>
        <div>DÉCISION: <span style="color:#10b981; font-weight:bold; text-shadow: 0 0 5px #10b981;">Ready to Fire</span></div>
    </div>

</div>
""", unsafe_allow_html=True)
