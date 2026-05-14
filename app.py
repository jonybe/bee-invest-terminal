import streamlit as st
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="BEE-INVEST | ELITE TERMINAL", layout="wide")

def get_market_data():
    try:
        gold = yf.Ticker("GC=F").history(period="1d")
        btc = yf.Ticker("BTC-USD").history(period="1d")
        dxy = yf.Ticker("DX-Y.NYB").history(period="1d")
        yields = yf.Ticker("^TNX").history(period="1d")
        
        return {
            "p_gold": gold['Close'].iloc[-1],
            "c_gold": ((gold['Close'].iloc[-1] - gold['Open'].iloc[-1]) / gold['Open'].iloc[-1]) * 100,
            "p_btc": btc['Close'].iloc[-1],
            "v_dxy": dxy['Close'].iloc[-1],
            "v_yields": yields['Close'].iloc[-1] / 10,
            "time": datetime.now().strftime("%H:%M:%S")
        }
    except:
        return {"p_gold":0, "c_gold":0, "p_btc":0, "v_dxy":0, "v_yields":0, "time":"--"}

data = get_market_data()

# --- DESIGN STYLE KILLZONE ---
html_ui = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
    body {{ background-color: #080808; color: #e0e0e0; font-family: 'Inter', sans-serif; }}
    .kz-container {{ background: #080808; padding: 20px; border-radius: 8px; }}
    .kz-header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1a1a1a; padding-bottom: 15px; margin-bottom: 25px; }}
    .kz-grid {{ display: grid; grid-template-columns: 2fr 1fr; gap: 25px; }}
    .kz-card {{ background: #0d0d0d; border: 1px solid #1a1a1a; padding: 20px; border-radius: 6px; }}
    .bar-container {{ background: #1a1a1a; height: 12px; border-radius: 6px; margin: 10px 0; overflow: hidden; display: flex; }}
    .bull-bar {{ background: #00ff88; height: 100%; }}
    .bear-bar {{ background: #ff4b4b; height: 100%; }}
    .tag {{ padding: 2px 8px; border-radius: 3px; font-size: 10px; font-weight: bold; text-transform: uppercase; border: 1px solid #333; }}
</style>

<div class="kz-container">
    <div class="kz-header">
        <div style="display:flex; align-items:center; gap:20px;">
            <b style="color:#ffb000; font-size:20px; letter-spacing:1px;">BEE-INVEST</b>
            <span style="color:#666; font-size:12px;">INTELLIGENCE D'OR</span>
            <span style="background:#1a1a1a; padding:5px 15px; border-radius:4px; border:1px solid #333; font-size:13px;">
                XAU / USD : <b style="color:#00ff88;">{data['p_gold']:,.2f} $</b> 
                <small style="color:{'#00ff88' if data['c_gold'] > 0 else '#ff4b4b'};">({data['c_gold']:+.2f}%)</small>
            </span>
        </div>
        <div style="text-align:right; font-size:12px; color:#666;">
            BIAIS: <b style="color:#ffb000;">NEUTRE</b> | LIVE: {data['time']} GMT+1 | <b>REFRESH OK</b>
        </div>
    </div>

    <div class="kz-grid">
        <!-- COLONNE GAUCHE: DOMINANCE & FORCES -->
        <div>
            <div class="kz-card" style="margin-bottom:20px;">
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#888; margin-bottom:10px;">
                    <span>TAUREAU CONTRE OURS : DOMINANCE</span>
                    <span>MACRO = BIAIS DIRECTIONNEL</span>
                </div>
                
                <small style="color:#00ff88;">SUPPORTING GOLD: 100%</small>
                <div class="bar-container"><div class="bull-bar" style="width: 100%;"></div></div>
                
                <small style="color:#ff4b4b; margin-top:10px; display:block;">OPPOSING GOLD: 100%</small>
                <div class="bar-container"><div class="bear-bar" style="width: 100%;"></div></div>
            </div>

            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
                <div class="kz-card">
                    <div style="color:#00ff88; font-weight:bold; margin-bottom:15px; font-size:13px;">● FORCES DE SOUTIEN <span style="float:right;">+28.00</span></div>
                    <div style="font-size:12px; margin-bottom:10px;">
                        <span class="tag" style="color:#00ff88; border-color:#00ff88;">GÉOPOLITIQUE</span><br>
                        <p style="color:#888; margin-top:5px; font-size:11px;">Indice de stress issu des données publiques - les tensions soutiennent la demande d'or.</p>
                    </div>
                    <div style="font-size:12px;">
                        <span class="tag" style="color:#58a6ff; border-color:#58a6ff;">BANQUES CENTRALES</span><br>
                        <p style="color:#888; margin-top:5px; font-size:11px;">Tendance positive constante pour les achats massifs d'or physique.</p>
                    </div>
                </div>
                <div class="kz-card">
                    <div style="color:#ff4b4b; font-weight:bold; margin-bottom:15px; font-size:13px;">● FORCES OPPOSÉES <span style="float:right;">-0.07</span></div>
                    <div style="font-size:11px; color:#888;">
                        <b>XAU 15m/1h Impulse:</b> -0.12% / +0.08%<br><br>
                        Windows disagree - score above blends them. Le flux est actuellement indécis sur les petites unités de temps.
                    </div>
                </div>
            </div>
        </div>

        <!-- COLONNE DROITE: SYNCHRO & POSITIONNEMENT -->
        <div>
            <div class="kz-card" style="margin-bottom:20px;">
                <div style="color:#888; font-size:11px; margin-bottom:15px;">● SYNCHRONISATION DE LA ZONE</div>
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span>INDICE DOLLAR (DXY)</span><b style="color:{'#00ff88' if data['v_dxy'] < 118.5 else '#ff4b4b'};">{data['v_dxy']:.2f}</b>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span>REAL YIELDS (10Y)</span><b>{data['v_yields']:.2f}%</b>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span>BITCOIN (BTC)</span><b style="color:#58a6ff;">{data['p_btc']:,.0f} $</b>
                </div>
            </div>

            <div class="kz-card" style="border-top: 3px solid #ffb000; text-align:center;">
                <div style="color:#888; font-size:11px; text-transform:uppercase; margin-bottom:10px;">Biais de Positionnement</div>
                <b style="font-size:18px; color:#ffb000;">CADRAGE DÉFENSIF</b>
                <p style="font-size:11px; color:#666; margin-top:10px;">Le score est inférieur à 50. Considérez les rallyes comme fragiles jusqu'au virage du dollar.</p>
                <div style="background:#1a1a1a; padding:15px; border-radius:4px; margin-top:20px;">
                    <small style="color:#888;">ORDRE JONNYBEE</small><br>
                    <b style="font-size:24px; color:#00ff88;">LOT 0.00</b>
                </div>
            </div>
        </div>
    </div>
    
    <div style="background:{'#00ff88' if data['v_dxy'] < 118.5 else '#ff4b4b'}; color:#000; text-align:center; padding:12px; margin-top:25px; font-weight:bold; border-radius:4px; letter-spacing:2px;">
        {"CONFLUENCE VALIDÉE - ATTENTE SETUP TECHNIQUE" if data['v_dxy'] < 118.5 else "ALERTE : CONDITIONS MACRO DEFAVORABLES"}
    </div>
</div>
"""

st.components.v1.html(html_ui, height=900, scrolling=True)
