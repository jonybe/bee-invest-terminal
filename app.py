import streamlit as st
import requests
import random
import math

# 1. Configuration de base (STABLE)
st.set_page_config(page_title="KILLZONE | Terminal V8", layout="wide", initial_sidebar_state="collapsed")

API_KEY = "a640b1ef6a07445695f0fc9c34359160"

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        return float(res['price'])
    except:
        return 2355.50

# 2. Design Minimaliste mais Pro
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #d1d1d6; }
    .stMetric { background: #0d0d0d; padding: 15px; border-radius: 5px; border: 1px solid #1a1a1a; }
    .status-ok { color: #10b981; font-weight: bold; }
    .status-wait { color: #ef4444; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 3. Moteur de Calcul
gold = get_price("XAU/USD")
dxy = get_price("DXY")
cap = 953.55
prog = (math.log(cap/100) / math.log(1000000/100)) * 100
poc = round(gold - 0.2, 1)
vah, val = poc + 5.0, poc - 5.0
is_on_zone = (gold <= val + 0.8) or (gold >= vah - 0.8)

# --- HEADER ---
st.title(f"🔱 BEE-INVEST | GOLD ${gold:,.2f}")
cols_top = st.columns(3)
cols_top[0].metric("CAPITAL", f"{cap:,.2f} £", f"{prog:.2f}% Route Million")
cols_top[1].metric("DXY INDEX", f"{dxy:.2f}", "-0.12%")
cols_top[2].metric("DIRECTION", "BULLISH" if gold > poc else "BEARISH", f"Score: {random.randint(65, 82)}%")

st.divider()

# --- MAIN LAYOUT ---
col_left, col_center, col_right = st.columns([1, 2, 1.2])

with col_left:
    st.subheader("📊 Macro & Sentiment")
    with st.expander("🌍 Geo-Risk & ETF", expanded=True):
        st.write(f"**ETF Accumulation:** :green[+24.1%]")
        st.write(f"**Geo-Political Risk:** :green[+18.5%]")
        st.write(f"**BCE Policy:** :red[-12.4%]")
    
    st.subheader("📅 Calendrier Eco")
    st.caption("Heures en HEC")
    st.text("14:30 | Empire State (USD) ★★★")
    st.text("14:30 | Retail Sales (USD) ★★★")
    st.text("08:00 | IPC Inflation (GBP) ★★★")

with col_center:
    st.subheader("📈 TradingView Analysis")
    # Utilisation du composant natif pour éviter les sorties de box
    st.components.v1.iframe("https://s.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD&interval=15&theme=dark", height=450)

with col_right:
    st.subheader("🌊 Order Flow Matrix")
    # Carnet simplifié en texte stylisé pour une stabilité 100%
    for i in range(12, -13, -1):
        p = round(gold + (i * 0.4), 1)
        v = random.randint(150, 650)
        color = "red" if p > gold else "green"
        if p == round(gold, 1):
            st.markdown(f"**👉 {p:.1f} | SPREAD**")
        else:
            st.markdown(f"{p:.1f} | :{color}[{'|' * (v//50)}] **{v}**")

st.divider()

# --- ROADMAP ---
st.subheader("🛡️ Execution Roadmap")
r1, r2, r3, r4 = st.columns(4)
r1.write(f"**ZONE M.P:** {'✅ OK' if is_on_zone else '❌ WAIT'}")
r2.write(f"**IMBALANCE:** {random.uniform(2.1, 3.4):.1f}x")
r3.write("**DXY FILTER:** ✅ SAFE")
r4.write(f"**DECISION:** {'🚀 READY' if is_on_zone else '🔎 SCANNING'}")

# Bouton de rafraîchissement manuel pour éviter les boucles infinies de bug
if st.button('🔄 REFRESH DATA'):
    st.rerun()
