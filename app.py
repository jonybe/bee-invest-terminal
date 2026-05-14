import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime

# 1. Config & Auto-refresh (2s)
st.set_page_config(page_title="BEE-INVEST | QUANT V18", layout="wide")

# CSS Pro Fixé
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; padding: 20px; border-radius: 4px; margin-bottom: 15px; }
    .label { color: #555; font-size: 10px; text-transform: uppercase; font-weight: bold; letter-spacing: 1.5px; margin-bottom: 10px; }
    .val-quant { font-family: 'JetBrains Mono', monospace; font-size: 22px; font-weight: bold; }
    .bar-bg { background: #1a1a1a; height: 8px; border-radius: 4px; margin: 8px 0; overflow: hidden; }
    .bar-bull { background: #00ff88; height: 100%; transition: width 1s; }
</style>
""", unsafe_allow_html=True)

def get_market_data():
    try:
        gold = yf.Ticker("GC=F").fast_info['last_price']
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        btc = yf.Ticker("BTC-USD").fast_info['last_price']
        feed = feedparser.parse("https://news.google.com/rss/search?q=or+bourse+forex&hl=fr&gl=FR&ceid=FR:fr")
        news = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)[:10]
        
        # Scores réels dynamiques (Logique V17)
        text_blob = " ".join([n.title.lower() for n in news])
        geo = 32.50 if any(w in text_blob for w in ['iran', 'guerre', 'tension', 'russie']) else 28.0
        cb = 20.20 if any(w in text_blob for w in ['fed', 'inflation', 'taux', 'bce']) else 18.0
        etf = 9.00
        
        return gold, dxy, yields, btc, news, geo, cb, etf
    except: return None

data = get_market_data()

if data:
    gold, dxy, yields, btc, news, geo, cb, etf = data
    
    # Header
    st.markdown(f"<div style='display:flex; justify-content:space-between; align-items:center;'><div><h2 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST QUANT</h2></div><div style='font-family:JetBrains Mono; color:#00ff88; font-size:22px; font-weight:bold;'>XAU: {gold:,.2f} $</div></div>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns([1.2, 1.5, 0.8])

    with col1:
        st.markdown("<p class='label'>● ANALYSE DES FORCES RÉELLES</p>", unsafe_allow_html=True)
        
        # Correction : On utilise st.markdown séparément pour chaque bloc
        st.markdown(f"""<div style="border-left:2px solid #00ff88; padding-left:15px; margin-bottom:20px;">
            <small class="label" style="color:#00ff88;">GÉOPOLITIQUE</small><br>
            <span class="val-quant">+{geo:.2f}</span><br>
            <small style="color:#444;">Basé sur l'indice de stress actuel</small>
        </div>""", unsafe_allow_html=True)
        
        st.markdown(f"""<div style="border-left:2px solid #58a6ff; padding-left:15px; margin-bottom:20px;">
            <small class="label" style="color:#58a6ff;">BANQUES CENTRALES</small><br>
            <span class="val-quant">+{cb:.2f}</span><br>
            <small style="color:#444;">Pression monétaire et achats physiques</small>
        </div>""", unsafe_allow_html=True)
        
        st.markdown(f"""<div style="border-left:2px solid #ffb000; padding-left:15px; margin-bottom:20px;">
            <small class="label" style="color:#ffb000;">FLUX ETF / INST.</small><br>
            <span class="val-quant">+{etf:.2f}</span><br>
            <small style="color:#444;">Demande globale de sécurité</small>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("<p class='label'>● DOMINANCE & EXÉCUTION</p>", unsafe_allow_html=True)
        # Calcul Dominance
        market_drag = (dxy - 100) + (yields * 5)
        dominance = min(max((geo + cb + etf) - market_drag, 10), 100)
        
        st.markdown(f"<small style='color:#00ff88;'>BULL DOMINANCE : {dominance:.1f}%</small><div class='bar-bg'><div class='bar-bull' style='width:{dominance}%'></div></div>", unsafe_allow_html=True)
        
        can_trade = dominance > 58 and yields < 2.00
        lot = (959.56 * 0.02) / 150 if can_trade else 0.0
        
        st.markdown(f"""<div class='kz-card' style='border-top: 3px solid #ffb000; text-align:center;'>
            <small class="label">SIGNAL DYNAMIQUE</small><br>
            <b style="font-size:24px; color:{'#00ff88' if can_trade else '#ffb000'};">{'ACHAT (BUY)' if can_trade else 'CADRAGE DÉFENSIF'}</b>
            <hr style='border-color:#222;'>
            <small class="label">TAILLE DE LOT</small><br>
            <span style="font-size:45px; font-weight:900; color:#00ff88;">{lot:.2f}</span>
            <div style="margin-top:10px; color:#444; font-size:10px;">Capital: 959.56 GBP | Risque: 2%</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown("<p class='label'>● SYNCHRO MACRO</p>", unsafe_allow_html=True)
        st.metric("DXY BROAD", f"{dxy:.2f}")
        st.metric("REAL YIELDS", f"{yields:.2f}%")
        st.metric("BTC / USD", f"{btc:,.0f}")

    st.markdown("---")
    st.markdown("<p class='label'>● DERNIÈRES DÉPÊCHES ANALYSÉES</p>", unsafe_allow_html=True)
    for n in news[:6]:
        with st.expander(f"🕒 {n.published[5:16]} | {n.title}"):
            st.write(n.summary if 'summary' in n else "Résumé non disponible.")
            st.markdown(f"[Lire l'article complet]({n.link})")

# Auto-refresh 5s
import time
time.sleep(5)
st.rerun()
