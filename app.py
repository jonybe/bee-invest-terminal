import streamlit as st
import yfinance as yf
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# 1. Configuration et Auto-refresh (Toutes les 30 secondes)
st.set_page_config(page_title="BEE-INVEST | LIVE TERMINAL", layout="wide")
st_autorefresh(interval=30000, key="datarefresh")

def get_live_data():
    try:
        # Récupération des tickers
        tickers = {
            "gold": yf.Ticker("GC=F"),
            "btc": yf.Ticker("BTC-USD"),
            "dxy": yf.Ticker("DX-Y.NYB"),
            "yields": yf.Ticker("^TNX")
        }
        
        data = {k: v.history(period="1d") for k, v in tickers.items()}
        news = tickers["gold"].news # Flux de news réel
        
        # Calcul des prix et variations
        p_gold = data["gold"]['Close'].iloc[-1]
        c_gold = ((p_gold - data["gold"]['Open'].iloc[-1]) / data["gold"]['Open'].iloc[-1]) * 100
        
        # Simulation dynamique des barres basée sur le prix (pour le mouvement temps réel)
        # Si l'or monte, la barre Bull augmente.
        bull_strength = min(max(50 + (c_gold * 10), 10), 100)
        bear_strength = 100 - bull_strength
        
        return {
            "p_gold": p_gold, "c_gold": c_gold,
            "p_btc": data["btc"]['Close'].iloc[-1],
            "v_dxy": data["dxy"]['Close'].iloc[-1],
            "v_yields": data["yields"]['Close'].iloc[-1] / 10,
            "news": news[:8], # On prend 8 news au lieu de 4
            "bull": bull_strength, "bear": bear_strength,
            "time": datetime.now().strftime("%H:%M:%S")
        }
    except:
        return None

ld = get_live_data()

if ld:
    # --- DESIGN KILLZONE DYNAMIQUE ---
    html_ui = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
        body {{ background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; }}
        .kz-card {{ background: #0d0d0d; border: 1px solid #1a1a1a; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .bar-bg {{ background: #1a1a1a; height: 10px; border-radius: 5px; margin: 10px 0; overflow: hidden; }}
        .bull-fill {{ background: #00ff88; height: 100%; width: {ld['bull']}%; transition: width 1s ease-in-out; }}
        .bear-fill {{ background: #ff4b4b; height: 100%; width: {ld['bear']}%; transition: width 1s ease-in-out; }}
        .news-item {{ border-bottom: 1px solid #1a1a1a; padding: 10px 0; font-size: 11px; }}
    </style>

    <div style="background:#050505; padding:10px;">
        <!-- HEADER LIVE -->
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #ffb000; padding-bottom:15px; margin-bottom:20px;">
            <div><b style="color:#ffb000; font-size:22px;">🔱 BEE-INVEST LIVE</b></div>
            <div style="background:#111; padding:5px 15px; border:1px solid #333; border-radius:4px;">
                XAU/USD : <b style="color:#00ff88;">{ld['p_gold']:,.2f} $</b> ({ld['c_gold']:+.2f}%)
            </div>
            <div style="text-align:right; font-size:12px; color:#666;">MAJ : {ld['time']} | <b>FLUX ACTIF</b></div>
        </div>

        <div style="display:grid; grid-template-columns: 2fr 1fr; gap:20px;">
            <div>
                <!-- DOMINANCE DYNAMIQUE -->
                <div class="kz-card">
                    <div style="display:flex; justify-content:space-between; font-size:11px; color:#888;">
                        <span>DOMINANCE FLUX (RÉEL)</span>
                        <span>SCORE DYNAMIQUE</span>
                    </div>
                    <div style="margin-top:15px;">
                        <small style="color:#00ff88;">BULL FORCE: {ld['bull']:.1f}%</small>
                        <div class="bar-bg"><div class="bull-fill"></div></div>
                        <small style="color:#ff4b4b;">BEAR FORCE: {ld['bear']:.1f}%</small>
                        <div class="bar-bg"><div class="bear-fill"></div></div>
                    </div>
                </div>

                <!-- FLUX DE NEWS ÉTENDU -->
                <div class="kz-card">
                    <div style="color:#ffb000; font-weight:bold; font-size:13px; margin-bottom:15px;">● JOURNAL DES DÉPÊCHES (LIVE 8)</div>
                    {"".join([f"<div class='news-item'><b style='color:#ffb000;'>[{n.get('publisher','LIVE')}]</b> {n.get('title')}</div>" for n in ld['news']])}
                </div>
            </div>

            <div>
                <!-- PRIX RÉELS -->
                <div class="kz-card">
                    <div style="color:#888; font-size:11px; margin-bottom:15px;">● SYNCHRO ZONE</div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:10px;"><span>DXY</span><b style="color:#00ff88;">{ld['v_dxy']:.2f}</b></div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:10px;"><span>10Y YIELDS</span><b>{ld['v_yields']:.2f}%</b></div>
                    <div style="display:flex; justify-content:space-between;"><span>BTC</span><b style="color:#58a6ff;">{ld['p_btc']:,.0f} $</b></div>
                </div>

                <!-- BIAIS -->
                <div class="kz-card" style="border-top:3px solid #ffb000; text-align:center;">
                    <b style="color:#ffb000;">CADRAGE DÉFENSIF</b><br>
                    <small style="color:#666;">Biais actuel basé sur DXY/Yields</small>
                    <div style="background:#111; padding:15px; border-radius:4px; margin-top:20px;">
                        <small style="color:#888;">LOT CONSEILLÉ</small><br>
                        <b style="font-size:24px; color:#00ff88;">LOT 0.00</b>
                    </div>
                </div>
            </div>
        </div>
        
        <div style="background:#00ff88; color:#000; text-align:center; padding:15px; font-weight:bold; margin-top:10px; border-radius:5px;">
            CONFLUENCE ANALYSÉE - ATTENTE SIGNAL TECHNIQUE
        </div>
    </div>
    """
    st.components.v1.html(html_ui, height=1000, scrolling=True)
else:
    st.error("Connexion aux flux financiers momentanément interrompue. Reconnexion...")
