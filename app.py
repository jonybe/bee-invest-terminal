import streamlit as st
import yfinance as yf
from datetime import datetime

# Configuration de la page Streamlit
st.set_page_config(page_title="BeeInvest Terminal", layout="wide")

def bee_invest_elite_v7():
    try:
        # 1. RÉCUPÉRATION DES DONNÉES
        gold = yf.Ticker("GC=F").history(period="1d")
        btc = yf.Ticker("BTC-USD").history(period="1d")
        dxy = yf.Ticker("DX-Y.NYB").history(period="1d")
        yields = yf.Ticker("^TNX").history(period="1d")

        p_gold = gold['Close'].iloc[-1] if not gold.empty else 0
        p_btc = btc['Close'].iloc[-1] if not btc.empty else 0
        v_dxy = dxy['Close'].iloc[-1] if not dxy.empty else 0
        v_yields = (yields['Close'].iloc[-1] / 10) if not yields.empty else 0
        
        sentiment_score = 45 
        regime = "WEAK — LEAN"
        maintenant = datetime.now().strftime("%H:%M:%S")

        # 2. DESIGN INTERFACE
        html_ui = f"""
        <div style="background:#050505; color:#eee; font-family:sans-serif; padding:25px; border:1px solid #222; border-radius:12px;">
            <div style="display:flex; justify-content:space-between; border-bottom:1px solid #ffb000; padding-bottom:15px; margin-bottom:20px;">
                <div><b style="color:#ffb000; font-size:22px;">🔱 BEE-INVEST TERMINAL</b></div>
                <div style="text-align:right;">
                    <span style="font-size:18px; font-weight:bold; color:#00ff88;">XAU: {p_gold:,.2f}$ | BTC: {p_btc:,.0f}$</span><br>
                    <small style="color:#444;">LIVE : {maintenant} | JONNYBEE_ELITE</small>
                </div>
            </div>
            <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:20px;">
                <div style="background:#0d0d0d; padding:20px; border:1px solid #222; border-radius:8px;">
                    <div style="color:#ffb000; font-size:11px; font-weight:bold; margin-bottom:20px;">● MARKET REGIME</div>
                    <div style="text-align:center; padding:10px; background:#1a1a1a; border-radius:4px;">
                        <b style="font-size:20px; color:#ffb000;">{regime}</b><br>
                        <small style="color:#666;">SCORE : {sentiment_score}</small>
                    </div>
                    <div style="margin-top:20px;">
                        <div style="display:flex; justify-content:space-between;"><small>REAL YIELDS</small><b>{v_yields:.2f}%</b></div>
                        <div style="display:flex; justify-content:space-between;"><small>DXY BROAD</small><b>{v_dxy:.2f}</b></div>
                    </div>
                </div>
                <div style="background:#0d0d0d; padding:20px; border:1px solid #222; border-radius:8px;">
                    <div style="color:#ffb000; font-size:11px; font-weight:bold; margin-bottom:20px;">● PROTOCOLE</div>
                    <div style="font-size:12px; line-height:2;">
                        <span style="color:#ff4b4b;">[!] Attendre Score > 65</span><br>
                        [✓] Session Londres Active<br>
                        [ ] Setup Technique Validé<br>
                    </div>
                </div>
                <div style="background:#0d0d0d; padding:20px; border:1px solid #222; border-radius:8px;">
                    <div style="color:#ffb000; font-size:11px; font-weight:bold; margin-bottom:20px;">● NARRATIVE</div>
                    <div style="font-size:11px; color:#ccc;">Flux FX équilibré. Indécision.</div>
                    <div style="margin-top:25px; text-align:center;">
                         <small style="color:#666;">POSITION</small><br>
                         <b style="font-size:24px; color:#ffb000;">LOT 0.00</b>
                    </div>
                </div>
            </div>
            <div style="background:#1a1a1a; color:#ffb000; text-align:center; padding:15px; margin-top:20px; font-weight:bold; border: 1px solid #333;">
                ⚠️ RENDEMENTS À {v_yields:.2f}% - PROCHE DE 2.00%
            </div>
        </div>
        """
        return html_ui
    except Exception as e:
        return f"<div style='color:white;'>Erreur de chargement des données : {e}</div>"

# Lancement de l'affichage
ui = bee_invest_elite_v7()
st.components.v1.html(ui, height=600)
