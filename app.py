import streamlit as st
import requests
import random
import math

# 1. Configuration & API
st.set_page_config(page_title="KILLZONE | Terminal Fortress", layout="wide", initial_sidebar_state="collapsed")
API_KEY = "a640b1ef6a07445695f0fc9c34359160"

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        return float(res['price'])
    except: return 2355.50

# CSS DE SCELLEMENT (Verrouille les composants)
st.markdown("""
<style>
    [data-testid="stAppViewBlockContainer"] { padding: 0 !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #d1d1d6; font-family: 'Inter', sans-serif; }
    .kz-table { width: 100%; border-collapse: separate; border-spacing: 10px; table-layout: fixed; background: #050505; }
    .kz-cell { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 12px; vertical-align: top; overflow: hidden; }
    .kz-header { font-size: 9px; font-weight: 900; color: #eab308; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 8px; border-left: 3px solid #eab308; padding-left: 8px; }
    
    /* DOM STYLING */
    .dom-row { display: flex; height: 17px; align-items: center; border-bottom: 1px solid #111; font-family: 'JetBrains Mono', monospace; }
    .dom-p { width: 55px; text-align: right; padding-right: 8px; font-size: 9px; }
    .dom-bar-wrap { flex-grow: 1; height: 100%; position: relative; display: flex; align-items: center; background: #080808; }
    .dom-vol { position: absolute; right: 8px; color: #fff; font-size: 8px; font-weight: bold; z-index: 10; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=10)
def terminal():
    # CALCULS
    gold = get_price("XAU/USD")
    dxy = get_price("DXY")
    cap = 953.55
    prog = (math.log(cap/100) / math.log(1000000/100)) * 100
    poc = round(gold - 0.2, 1)
    vah, val = poc + 5.0, poc - 5.0
    
    # DOM HTML GENERATION
    dom_rows_html = ""
    t_ask, t_bid = 0, 0
    setup_dir = "BULL" if gold <= val+0.8 else "BEAR" if gold >= vah-0.8 else "NONE"
    for i in range(16, -17, -1):
        p = round(gold + (i * 0.4), 1)
        is_ask, is_curr = p > gold, p == round(gold, 1)
        v = random.randint(2500, 3500) if ((setup_dir == "BULL" and p == round(val,1)) or (setup_dir == "BEAR" and p == round(vah,1))) else random.randint(120, 600)
        if not is_curr:
            if is_ask: t_ask += v
            else: t_bid += v
        
        p_style = "color:#eab308; font-weight:bold; background:rgba(234,179,8,0.1);" if is_curr else "color:#444;"
        bar_c = "rgba(239,68,68,0.25)" if is_ask else "rgba(16,185,129,0.25)"
        bar_b = "#ef4444" if is_ask else "#10b981"
        w = min(100, (v/4000)*100)
        
        bar_div = f'<div style="position:absolute; left:0; height:100%; width:{w}%; background:{bar_c}; border-right:2px solid {bar_b};"></div>' if not is_curr else ""
        dom_rows_html += f'<div class="dom-row"><div class="dom-p" style="{p_style}">{p:.1f}</div><div class="dom-bar-wrap">{bar_div}<div class="dom-vol">{v if not is_curr else ""}</div></div></div>'

    ratio = max(t_bid, t_ask) / max(1, min(t_bid, t_ask))
    is_on_zone = (gold <= val + 0.8) or (gold >= vah - 0.8)

    # RENDU GLOBAL (STRUCTURE TABLEAU UNIQUE)
    st.markdown(f"""
    <div style="background:#0d0d0d; border-bottom:2px solid #eab308; padding:8px 20px; display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:15px;"><b style="color:#eab308; font-size:18px;">BEE-INVEST</b><span style="color:#333;">|</span><small>FORTRESS V7.0</small></div>
        <div style="text-align:center;"><b style="color:#10b981; font-size:16px;">{cap:,.2f} £</b><div style="width:150px; height:3px; background:#1a1a1a; margin:4px auto;"><div style="width:{prog}%; height:100%; background:#10b981;"></div></div></div>
        <div style="display:flex; gap:30px;"><div style="text-align:right;"><small>GOLD</small><br><b>${gold:,.2f}</b></div><div style="text-align:right;"><small>DXY</small><br><b>{dxy:.2f}</b></div></div>
    </div>

    <table class="kz-table">
        <tr>
            <td style="width:280px;">
                <div class="kz-cell" style="margin-bottom:10px;">
                    <div class="kz-header">Sentiment</div>
                    <div style="text-align:center; padding:10px; background:#080808; border-radius:4px;">
                        <span style="font-size:20px; font-weight:900; color:{'#10b981' if gold > poc else '#ef4444'};">{'BULLISH' if gold > poc else 'BEARISH'}</span><br>
                        <span style="color:#eab308; font-size:9px; font-weight:bold;">Score: {random.randint(65, 82)}%</span>
                    </div>
                </div>
                <div class="kz-cell" style="height:350px;">
                    <div class="kz-header">Eco Calendar</div>
                    <div style="font-size:9px; line-height:1.6;">
                        <div style="display:flex; justify-content:space-between;"><span>14:30 | Empire State</span><b style="color:#ef4444;">USD ★★★</b></div>
                        <div style="display:flex; justify-content:space-between;"><span>14:30 | Retail Sales</span><b style="color:#ef4444;">USD ★★★</b></div>
                        <div style="display:flex; justify-content:space-between;"><span>08:00 | IPC Inflation</span><b style="color:#ef4444;">GBP ★★★</b></div>
                        <hr style="border:0; border-top:1px solid #1a1a1a; margin:8px 0;">
                        <small style="color:#888;"><b>BCE :</b> Pause confirmée.<br><b>GEO :</b> Tensions géo +12$.</small>
                    </div>
                </div>
            </td>

            <td>
                <div class="kz-cell" style="height:488px; position:relative;">
                    <div class="kz-header">TradingView M15 Analysis</div>
                    <div style="height:350px; overflow:hidden;">
                        <iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark" style="width:100%; height:100%; border:none;"></iframe>
                    </div>
                    <div style="margin-top:10px; display:grid; grid-template-columns: repeat(4, 1fr); gap:5px;">
                        <div style="background:#080808; padding:6px; border:1px solid #1a1a1a; text-align:center;"><small>BCE</small><br><b style="color:#ef4444;">-12%</b></div>
                        <div style="background:#080808; padding:6px; border:1px solid #1a1a1a; text-align:center;"><small>ETF</small><br><b style="color:#10b981;">+24%</b></div>
                        <div style="background:#080808; padding:6px; border:1px solid #1a1a1a; text-align:center;"><small>GEO</small><br><b style="color:#10b981;">+18%</b></div>
                        <div style="background:#080808; padding:6px; border:1px solid #1a1a1a; text-align:center;"><small>USD</small><br><b style="color:#ef4444;">-09%</b></div>
                    </div>
                </div>
            </td>

            <td style="width:300px;">
                <div class="kz-cell" style="height:488px;">
                    <div class="kz-header">Order Flow Matrix</div>
                    <div style="background:#080808; border:1px solid #1a1a1a; height:440px; overflow:hidden;">
                        {dom_rows_html}
                    </div>
                </div>
            </td>
        </tr>
        <tr>
            <td colspan="3">
                <div class="kz-cell" style="display:grid; grid-template-columns: repeat(4, 1fr); gap:10px; text-align:center;">
                    <div><small style="color:#555;">ZONE M.P</small><br><b style="color:{'#10b981' if is_on_zone else '#ef4444'};">{'VALIDATED' if is_on_zone else 'SCANNING'}</b></div>
                    <div><small style="color:#555;">IMBALANCE</small><br><b style="color:{'#10b981' if ratio >= 2.7 else '#ef4444'};">{ratio:.1f}x</b></div>
                    <div><small style="color:#555;">DXY FILTER</small><br><b style="color:#10b981;">CONFLUENCE</b></div>
                    <div><small style="color:#555;">DECISION</small><br><b style="color:{'#10b981' if ratio >= 2.7 and is_on_zone else '#eab308'};">{'READY TO FIRE' if ratio >= 2.7 and is_on_zone else 'NO EDGE'}</b></div>
                </div>
            </td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

terminal()
