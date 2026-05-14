import streamlit as st
import yfinance as yf
import feedparser
import re
from datetime import datetime

st.set_page_config(page_title="BEE-INVEST | QUANT UNIT", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    .kz-card { background: #0d0d0d; border: 1px solid #1a1a1a; padding: 20px; border-radius: 4px; margin-bottom: 15px; }
    .label { color: #555; font-size: 10px; text-transform: uppercase; font-weight: bold; letter-spacing: 1.5px; margin-bottom: 10px; }
    .val-quant { font-family: 'JetBrains Mono', monospace; font-size: 22px; font-weight: bold; }
    .bar-bg { background: #1a1a1a; height: 8px; border-radius: 4px; margin: 8px 0; overflow: hidden; }
    .bar-bull { background: #00ff88; height: 100%; transition: width 1s; }
    .force-box { border-left: 2px solid #333; padding-left: 15px; margin-bottom: 15px; background: rgba(255,255,255,0.01); padding: 10px; }
</style>
""", unsafe_allow_html=True)

def analyze_sentiment_scores(news_entries):
    # Initialisation des scores de base (tes références)
    geo_score = 28.0
    cb_score = 18.0
    etf_score = 9.0
    
    # Analyse de texte simple pour ajuster les scores en temps réel
    text_blob = " ".join([n.title.lower() for n in news_entries])
    
    # Géopolitique (Guerre, Tensions, Middle East, Ukraine)
    if any(word in text_blob for word in ['guerre', 'conflit', 'tension', 'frappe', 'missile', 'iran', 'russie']):
        geo_score += 4.5
    
    # Banques Centrales (Fed, BCE, Taux, Inflation)
    if any(word in text_blob for word in ['fed', 'bce', 'inflation', 'taux', 'powell', 'lagarde']):
        cb_score += 2.2
        
    return geo_score, cb_score, etf_score

def get_market_data():
    try:
        gold = yf.Ticker("GC=F").fast_info['last_price']
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        btc = yf.Ticker("BTC-USD").fast_info['last_price']
        
        feed = feedparser.parse("https://news.google.com/rss/search?q=or+bourse+forex+geopolitique&hl=fr&gl=FR&ceid=FR:fr")
        news = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)[:10]
        
        geo, cb, etf = analyze_sentiment_scores(news)
        return gold, dxy, yields, btc, news, geo, cb, etf
    except: return None

data = get_market_data()
if data:
    gold, dxy, yields, btc, news, geo, cb, etf = data
    
    # Calcul Dominance
    total_bull_force = geo + cb + etf
    # Ajustement par rapport aux vents contraires (DXY/Yields)
    market_drag = (dxy - 100) + (yields * 10)
    final_bull_dominance = min(max(total_bull_force - market_drag, 10), 100)
    
    # --- INTERFACE ---
    st.markdown(f"<div style='display:flex; justify-content:space-between; align-items:center;'><div><h2 style='color:#ffb000; margin:0;'>🔱 BEE-INVEST QUANT</h2></div><div class='val-quant' style='color:#00ff88;'>XAU: {gold:,.2f} $</div></div>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns([1.2, 1.5, 0.8])

    with col1:
        st.markdown("<p class='label'>● ANALYSE DES FORCES RÉELLES</p>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="force-box">
            <small class="label" style="color:#00ff88;">GÉOPOLITIQUE</small><br>
            <span class="val-quant">+{geo:.2f}</span><br>
            <small style="color:#444;">Score basé sur l'indice de stress actuel</small>
        </div>
        <div class="force-box">
            <small class="label" style="color:#58a6ff;">BANQUES CENTRALES</small><br>
            <span class="val-quant">+{cb:.2f}</span><br>
            <small style="color:#444;">Pression monétaire et achats physiques</small>
        </div>
        <div class="force-box">
            <small class="label" style="color:#ffb000;">FLUX ETF / INSTITUTIONNEL</small><br>
            <span class="val-quant">+{etf:.2f}</span><br>
            <small style="color:#444;">Demande globale de sécurité</small>
        </div>
        """)

    with col2:
        st.markdown("<p class='label'>● DOMINANCE & EXÉCUTION</p>", unsafe_allow_html=True)
        st.markdown(f"<small style='color:#00ff88;'>BULL DOMINANCE : {final_bull_dominance:.1f}%</small><div class='bar-bg'><div class='bar-bull' style='width:{final_bull_dominance}%'></div></div>", unsafe_allow_html=True)
        
        can_trade = final_bull_dominance > 55 and yields < 2.00
        lot = (959.56 * 0.02) / 150 if can_trade else 0.0
        
        st.markdown(f"""<div class='kz-card' style='border-top: 3px solid #ffb000; text-align:center;'>
            <small class="label">SIGNAL DYNAMIQUE</small><br>
            <b style="font-size:24px; color:{'#00ff88' if can_trade else '#ffb000'};">{'ACHAT (BUY)' if can_trade else 'CADRAGE DÉFENSIF'}</b>
            <hr style='border-color:#222;'>
            <small class="label">TAILLE DE LOT</small><br>
            <span style="font-size:45px; font-weight:900; color:#00ff88;">{lot:.2f}</span>
            <div style="margin-top:10px; color:#444; font-size:11px;">Basé sur Capital 959.56 GBP | Risque 2%</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown("<p class='label'>● SYNCHRO MACRO</p>", unsafe_allow_html=True)
        st.metric("DXY BROAD", f"{dxy:.2f}")
        st.metric("REAL YIELDS", f"{yields:.2f}%")
        st.metric("BTC / USD", f"{btc:,.0f}")

    st.markdown("---")
    st.markdown("<p class='label'>● DERNIÈRES DÉPÊCHES ANALYSÉES</p>", unsafe_allow_html=True)
    for n in news[:5]:
        with st.expander(f"🕒 {n.published[5:16]} | {n.title}"):
            st.write(n.summary)
            st.markdown(f"[Lire la suite]({n.link})")

# Auto-refresh 5s (plus stable pour les calculs de sentiment)
import time
time.sleep(5)
st.rerun()
