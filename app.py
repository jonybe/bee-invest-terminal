import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. Config & Auto-refresh (2 sec)
st.set_page_config(page_title="BEE-INVEST | MACRO INTELLIGENCE", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    .strat-card { background: #0d0d0d; border: 1px solid #ffb000; padding: 20px; border-radius: 4px; }
    .news-card { border-left: 3px solid #ffb000; padding: 10px; background: #0d0d0d; margin-bottom: 5px; font-size: 13px; }
    .price-val { font-family: 'JetBrains Mono', monospace; font-size: 28px; color: #00ff88; font-weight: bold; }
    .label { color: #555; font-size: 10px; text-transform: uppercase; font-weight: bold; letter-spacing: 1px; }
    .reason-box { background: #111; padding: 15px; border-radius: 4px; border-left: 2px solid #555; font-size: 13px; color: #aaa; margin-top: 10px; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

def get_market_data():
    try:
        gold = yf.Ticker("GC=F").fast_info['last_price']
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        btc = yf.Ticker("BTC-USD").fast_info['last_price']
        feed = feedparser.parse("https://news.google.com/rss/search?q=or+bourse+forex&hl=fr&gl=FR&ceid=FR:fr")
        sorted_news = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)
        return gold, dxy, yields, btc, sorted_news[:12]
    except: return None

gold, dxy, yields, btc, news = get_market_data()

# --- MOTEUR D'ANALYSE MACRO DYNAMIQUE ---
reasons = []
can_buy = True

# Analyse Dollar
if dxy < 118.05:
    reasons.append(f"✅ DXY ({dxy:.2f}) est sous la résistance critique de 118.05, libérant de la pression haussière sur l'Or.")
else:
    reasons.append(f"❌ DXY ({dxy:.2f}) est trop fort. Le dollar domine, rendant l'achat d'Or risqué.")
    can_buy = False

# Analyse Yields
if yields < 2.00:
    reasons.append(f"✅ Les Yields US 10Y ({yields:.2f}%) sont sous le seuil d'invalidation de 2.00%, favorisant les actifs non-rémunérés.")
else:
    reasons.append(f"❌ Les Yields ({yields:.2f}%) ont franchi les 2.00%. Pression vendeuse immédiate sur l'Or.")
    can_buy = False

# Analyse Gold Momentum (basé sur 4700 de référence)
if gold > 4700:
    reasons.append(f"📈 Momentum haussier confirmé au-dessus des 4700$.")
else:
    reasons.append(f"📉 L'Or stagne sous les 4700$. Manque de volume acheteur.")

# Verdict Final
signal = "ACHAT (BUY)" if can_buy else "NE PAS ENTRER"
entry, sl, tp = (gold, gold-15, gold+30) if can_buy else (0, 0, 0)

# --- AFFICHAGE ---
st.markdown(f"<h2 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST TACTICAL UNIT</h2>", unsafe_allow_html=True)
st.markdown("---")

col_news, col_strat, col_market = st.columns([1.2, 1.5, 0.8])

with col_news:
    st.markdown("<p class='label'>● DERNIÈRES DÉPÊCHES (FR)</p>", unsafe_allow_html=True)
    for n in news:
        st.markdown(f"<div class='news-card'><small style='color:#ffb000;'>{n.published[5:16]}</small><br>{n.title}</div>", unsafe_allow_html=True)

with col_strat:
    st.markdown("<p class='label'>● ANALYSE TACTIQUE DYNAMIQUE</p>", unsafe_allow_html=True)
    st.markdown(f"""<div class="strat-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="label">SIGNAL :</span> 
            <span style="color:{'#00ff88' if can_buy else '#ffb000'}; font-weight:bold; font-size:22px;">{signal}</span>
        </div>
        <hr style='border-color:#222;'>
        <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px; text-align:center;">
            <div><small class='label'>ENTRÉE</small><br><b>{entry if can_buy else '--'}</b></div>
            <div><small class='label'>STOP LOSS</small><br><b style='color:#ff4b4b;'>{sl if can_buy else '--'}</b></div>
            <div><small class='label'>TAKE PROFIT</small><br><b style='color:#00ff88;'>{tp if can_buy else '--'}</b></div>
        </div>
        <hr style='border-color:#222;'>
        <span class="label">DIAGNOSTIC MACRO TEMPS RÉEL :</span><br>
        <div class="reason-box">
            {"<br>".join(reasons)}
        </div>
    </div>""", unsafe_allow_html=True)

with col_market:
    st.markdown("<p class='label'>● PRIX EN DIRECT</p>", unsafe_allow_html=True)
    st.markdown(f"<div style='background:#0d0d0d; padding:15px; border-radius:4px; margin-bottom:10px; border:1px solid #1a1a1a; text-align:center;'><small class='label'>GOLD</small><br><span class='price-val'>{gold:,.2f}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background:#0d0d0d; padding:15px; border-radius:4px; margin-bottom:10px; border:1px solid #1a1a1a; text-align:center;'><small class='label'>DXY</small><br><span class='price-val' style='color:#eee;'>{dxy:.2f}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background:#0d0d0d; padding:15px; border-radius:4px; border:1px solid #1a1a1a; text-align:center;'><small class='label'>10Y YIELDS</small><br><span class='price-val' style='color:#58a6ff;'>{yields:.2f}%</span></div>", unsafe_allow_html=True)

# Footer Verdict
status_color = "#00ff88" if can_buy else "#ff4b4b"
st.markdown(f"<div style='background:{status_color}; color:black; text-align:center; padding:15px; font-weight:900; margin-top:20px;'>VERDICT : {'ACCORD EXÉCUTION' if can_buy else 'ALERTE : CONDITIONS DE FAVORABLES'}</div>", unsafe_allow_html=True)

# Auto-refresh 2s
import time
time.sleep(2)
st.rerun()
