from IPython.display import HTML, display, clear_output
import yfinance as yf
import time
from datetime import datetime

def bee_invest_elite_v7():
    while True:
        try:
            # 1. RÉCUPÉRATION DES DONNÉES EN DIRECT (OR, BTC, DXY, 10Y)
            gold = yf.Ticker("GC=F").history(period="1d")
            btc = yf.Ticker("BTC-USD").history(period="1d")
            dxy = yf.Ticker("DX-Y.NYB").history(period="1d")
            yields = yf.Ticker("^TNX").history(period="1d")

            # Prix actuels
            p_gold = gold['Close'].iloc[-1]
            p_btc = btc['Close'].iloc[-1]
            v_dxy = dxy['Close'].iloc[-1]
            v_yields = yields['Close'].iloc[-1] / 10
            
            # 2. LOGIQUE DE SENTIMENT (Basée sur tes captures du jour)
            # Score de 45 Neutre / Low selon Capture 085920
            sentiment_score = 45 
            regime = "WEAK — LEAN"
            maintenant = datetime.now().strftime("%H:%M:%S")

            # 3. CONDITIONS D'INVALIDATION (Alertes Capture 085940)
            alert_yields = "NEAR" if v_yields >= 1.99 else "OK"
            alert_dxy = "NEAR" if v_dxy >= 118.0 else "OK"

            # 4. DESIGN INTERFACE "KILLZONE"
            html_ui = f"""
            <div style="background:#050505; color:#eee; font-family:'Inter',sans-serif; padding:25px; width:1200px; border:1px solid #222; margin:auto; border-radius:12px;">
                
                <div style="display:flex; justify-content:space-between; border-bottom:1px solid #ffb000; padding-bottom:15px; margin-bottom:20px;">
                    <div>
                        <b style="color:#ffb000; font-size:22px;">🔱 BEE-INVEST TERMINAL</b>
                        <span style="margin-left:20px; color:#666;">SESSION : <span style="color:#ffb000;">LONDRES OPEN</span></span>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-size:18px; font-weight:bold; color:#00ff88;">XAU: {p_gold:,.2f}$ | BTC: {p_btc:,.0f}$</span><br>
                        <small style="color:#444;">ACTU : {maintenant} | JONNYBEE_ELITE</small>
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:20px;">
                    <!-- COLONNE 1 : SYNCHRO MACRO -->
                    <div style="background:#0d0d0d; padding:20px; border:1px solid #222; border-radius:8px;">
                        <div style="color:#ffb000; font-size:11px; font-weight:bold; margin-bottom:20px;">● MARKET REGIME (BIAIS)</div>
                        <div style="text-align:center; padding:10px; background:#1a1a1a; border-radius:4px;">
                            <b style="font-size:20px; color:#ffb000;">{regime}</b><br>
                            <small style="color:#666;">SCORE : {sentiment_score} (NEUTRAL)</small>
                        </div>
                        <div style="margin-top:20px;">
                            <div style="display:flex; justify-content:space-between;"><small>REAL YIELDS</small><b style="color:{'#ff4b4b' if alert_yields == 'NEAR' else '#eee'}">{v_yields:.2f}%</b></div>
                            <div style="display:flex; justify-content:space-between;"><small>DXY BROAD</small><b style="color:{'#ff4b4b' if alert_dxy == 'NEAR' else '#eee'}">{v_dxy:.2f}</b></div>
                        </div>
                    </div>

                    <!-- COLONNE 2 : CHECK-LIST STRATÉGIQUE -->
                    <div style="background:#0d0d0d; padding:20px; border:1px solid #222; border-radius:8px;">
                        <div style="color:#ffb000; font-size:11px; font-weight:bold; margin-bottom:20px;">● PROTOCOLE D'EXÉCUTION</div>
                        <div style="font-size:12px; line-height:2;">
                            <span style="color:#ff4b4b;">[!] Attendre Score > 65 ou < 35</span><br>
                            [✓] Session Londres Active<br>
                            [✓] Liquidité de Tir Détectée<br>
                            [ ] Setup Technique Validé (M15)<br>
                            <div style="margin-top:15px; border-top:1px solid #222; padding-top:10px; color:#888;">
                                <b>CADRAGE :</b> Respecter les vents contraires.
                            </div>
                        </div>
                    </div>

                    <!-- COLONNE 3 : LIVE NEWS FLOW -->
                    <div style="background:#0d0d0d; padding:20px; border:1px solid #222; border-radius:8px;">
                        <div style="color:#ffb000; font-size:11px; font-weight:bold; margin-bottom:20px;">● LIVE NARRATIVE</div>
                        <div style="font-size:11px; color:#ccc;">
                            <b>DOLLAR TRACKER :</b> Le flux FX est équilibré. L'indécision domine. Ne pas forcer l'entrée avant un break de structure.
                        </div>
                        <div style="margin-top:25px; text-align:center;">
                             <small style="color:#666;">POSITION CONSEILLÉE</small><br>
                             <b style="font-size:24px; color:#ffb000;">LOT 0.00 (WAIT)</b>
                        </div>
                    </div>
                </div>

                <div style="background:#1a1a1a; color:#ffb000; text-align:center; padding:15px; margin-top:20px; font-weight:bold; font-size:18px; border: 1px solid #333;">
                    ⚠️ ATTENTION : RENDEMENTS À 1.99% - PROCHE DE L'INVALIDATION (2.00%)
                </div>
            </div>
            """
            clear_output(wait=True)
            display(HTML(html_ui))
            time.sleep(60)
            
        except Exception as e:
            time.sleep(5)
            continue

bee_invest_elite_v7()
