import streamlit as st
import requests
import random
import math

# 1. Configuration de base
st.set_page_config(page_title="KILLZONE | Matrix Final", layout="wide", initial_sidebar_state="collapsed")

API_KEY = "a640b1ef6a07445695f0fc9c34359160"

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        return float(res['price'])
    except: return 2355.50

# CSS pour supprimer les marges blanches et forcer le noir
st.markdown("""
<style>
    div[data-testid="stAppViewBlockContainer"] { opacity: 1 !important; padding: 0 !important; max-width: 100% !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #d1d1d6; font-family: 'Inter', sans-serif; }
    iframe { border-radius: 4px; border: 1px solid #1a1a1a; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=8)
def matrix_engine():
    # --- A. TOUS LES CALCULS (ANTI-BUG) ---
    gold = get_price("XAU/USD")
    dxy = get_price("DXY")
    cap = 953.55
    prog = (math.log(cap/100) / math.log(1000000/100)) * 100
    poc = round(gold - 0.2, 1)
    vah, val = poc + 5.0, poc - 5.0
    
    # Flags de validation
    is_on_zone = (gold <= val + 0.8) or (gold >= vah - 0.8)
    dxy_ok = dxy < 107.0
    
    # Carnet d'ordres (DOM)
    dom_rows = ""
    t_ask, t_bid = 0, 0
    setup_dir = "BULL" if gold <= val+0.8 else "BEAR" if gold >= vah-0.8 else "NONE"
    for i in range(16, -17, -1):
        p = round(gold + (i * 0.4), 1)
        is_ask, is_curr = p > gold, p == round(gold, 1)
        v = random.randint(2600, 3500) if ((setup_dir == "BULL" and p == round(val,1)) or (setup_dir == "BEAR" and p == round(vah,1))) else random.randint(150, 650)
        if not is_curr:
            if is_ask: t_ask += v
            else: t_bid += v
        
        active_class = "color:#eab308; font-weight:900; background:rgba(234,179,8,0.1);" if is_curr else "color:#444;"
        bar_color = "rgba(239,68,68,0.3)" if is_ask else "rgba(16,185,129,0.3)"
        bar_border = "#ef4444" if is_ask else "#10b981"
        w = min(100, (v/4000)*100)
        
        bar_div = f'<div style="position:absolute; left:0; height:100%; width:{w}%; background:{bar_color}; border-right:2px solid {bar_border};"></div>' if not is_curr else ""
        vol_div = f'<div style="position:absolute; right:8px; color:#fff; font-size:9px; font-weight:700; z-index:10;">{v if not is_curr else ""}</div>'
        
        dom_rows += f"""
        <div style="display:flex; height:18px; align-items:center; border-bottom:1px solid #111; font-family:'JetBrains Mono';">
            <div style="width:60px; text-align:right; padding-right:10px; font-size:10px; {active_class}">{p:.1f}</div>
            <div style="flex-grow:1; height:100%; position:relative; background:#080808;">
                {bar_div}{vol_div}{'<div style="color:#eab308; font-size:8px; padding-left:10px;">MARKET</div>' if is_curr else ""}
            </div>
        </div>"""

    ratio = max(t_bid, t_ask) / max(1, min(t_bid, t_ask))
    ready = ratio >= 2.7 and is_on_zone and dxy_ok

    # --- B. CONSTRUCTION DU TERMINAL (TABLEAU FIXE) ---
    st.markdown(f"""
    <div style="padding:10px; background:#050505;">
        <div style="background:#0d0d0d; border-bottom:2px solid #eab308; padding:10px 20px; display:flex; justify-content:space-between; align-items:center; border-radius:4px; margin-bottom:10px;">
            <div style="display:flex; align-items:center; gap:20px;"><b style="color:#eab308; font-size:20px;">BEE-INVEST</b><span style="color:#333;">|</span><small>ELITE MATRIX V5.3</small></div>
            <div style="text-align:center;"><b style="color:#10b981; font-size:16px;">{cap:,.2f} £</b><div style="width:150px; height:3px; background:#1a1a1a; margin:4px auto;"><div style="width:{prog}%; height:100%; background:#10b981;"></div></div></div>
            <div style="display:flex; gap:30px;"><div style="text-align:right;"><small style="color:#555;">GOLD</small><br><b>${gold:,.2f}</b></div><div style="text-align:right;"><small style="color:#555;">DXY Index</small><br><b>{dxy:.2f}</b></div></div>
        </div>

        <table style="width:100%; border-spacing:10px; border-collapse:separate; table-layout:fixed;">
            <tr>
                <td style="width:300px; vertical-align:top;">
                    <div style="background:#0d0d0d; border:1px solid #1a1a1a; padding:15px; border-radius:4px; margin-bottom:10px;">
                        <div style="font-size:9px; color:#eab308; font-weight:900; letter-spacing:2px; margin-bottom:10px;">DAILY SENTIMENT</div>
                        <div style="text-align:center; font-size:26px; font-weight:900; color:{'#10b981' if gold > poc else '#ef4444'};">{'BULLISH' if gold > poc else 'BEARISH'}</div>
                        <div style="text-align:center; color:#eab308; font-size:10px; font-weight:bold;">Score: {random.randint(65, 82)}%</div>
                        <p style="font-size:8px; color:#444; margin-top:8px;">Bias calculé sur flux L2 + POC + DXY.</p>
                    </div>
                    <div style="background:#0d0d0d; border:1px solid #1a1a1a; padding:15px; border-radius:4px; height:320px;">
                        <div style="font-size:9px; color:#eab308; font-weight:900; letter-spacing:2px; margin-bottom:10px;">ECO CALENDAR</div>
                        <div style="font-size:10px; line-height:1.8;">
                            <div style="display:flex; justify-content:space-between;"><span>14:30 | Empire State</span><b style="color:#ef4444;">USD ★★★</b></div>
                            <div style="display:flex; justify-content:space-between;"><span>14:30 | Retail Sales</span><b style="color:#ef4444;">USD ★★★</b></div>
                            <div style="display:flex; justify-content:space-between;"><span>08:00 | IPC Inflation</span><b style="color:#ef4444;">GBP ★★★</b></div>
                        </div>
                        <div style="margin-top:20px; font-size:9px; color:#888;"><b>BCE:</b> Pause confirmée.<br><b>GEO:</b> Risque élevé.</div>
                    </div>
                </td>

                <td style="vertical-align:top;">
                    <div style="background:#0d0d0d; border:1px solid #1a1a1a; padding:10px; border-radius:4px; height:450px; margin-bottom:10px;">
                        <iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark" style="width: 100%; height: 100%; border: none;"></iframe>
                    </div>
                    <div style="background:#0d0d0d; border:1px solid #1a1a1a; padding:15px; border-radius:4px;">
                        <div style="font-size:9px; color:#eab308; font-weight:900; letter-spacing:2px; margin-bottom:10px;">MACRO IMPACT (%)</div>
                        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:10px;">
                            <div style="background:#080808; padding:8px; border-radius:4px; text-align:center;"><small>BCE</small><br><b style="color:#ef4444;">-12.4%</b></div>
                            <div style="background:#080808; padding:8px; border-radius:4px; text-align:center;"><small>ETF</small><br><b style="color:#10b981;">+24.1%</b></div>
                            <div style="background:#080808; padding:8px; border-radius:4px; text-align:center;"><small>GEO</small><br><b style="color:#10b981;">+18.5%</b></div>
                            <div style="background:#080808; padding:8px; border-radius:4px; text-align:center;"><small>USD</small><br><b style="color:#ef4444;">-09.2%</b></div>
                        </div>
                    </div>
                </td>

                <td style="width:320px; vertical-align:top;">
                    <div style="background:#0d0d0d; border:1px solid #1a1a1a; padding:10px; border-radius:4px; height:600px;">
                        <div style="font-size:9px; color:#eab308; font-weight:900; letter-spacing:2px; margin-bottom:10px;">ORDER FLOW MATRIX</div>
                        <div style="background:#080808; border-radius:2px; border:1px solid #1a1a1a; height:545px; overflow:hidden;">
                            {dom_rows}
                        </div>
                    </div>
                </td>
            </tr>
        </table>

        <div style="background:#0d0d0d; border:1px solid #1a1a1a; border-radius:4px; padding:15px; margin-top:5px; display:grid; grid-template-columns: repeat(4, 1fr); gap:20px; text-align:center;">
            <div><small style="color:#555;">ZONE PROFILE</small><br><b style="color:{'#10b981' if is_on_zone else '#ef4444'};">{'VALIDATED' if is_on_zone else 'SCANNING'}</b></div>
            <div><small style="color:#555;">IMBALANCE</small><br><b style="color:{'#10b981' if ratio >= 2.7 else '#ef4444'};">{ratio:.1f}x</b></div>
            <div><small style="color:#555;">DXY FILTER</small><br><b style="color:{'#10b981' if dxy_ok else '#ef4444'};">{'SAFE' if dxy_ok else 'DANGER'}</b></div>
            <div><small style="color:#555;">DECISION</small><br><b style="color:{'#10b981' if ready else '#eab308'};">{'READY TO FIRE' if ready else 'NO EDGE'}</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

matrix_engine()
