import streamlit as st
import yfinance as yf
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from GoogleNews import GoogleNews

# 1. Config Pro
st.set_page_config(page_title="BEE-INVEST | ELITE TERMINAL", layout="wide")
st_autorefresh(interval=60000, key="datarefresh") # Refresh 60s pour éviter les ban IP

def get_market_intelligence():
    try:
        # Data TradingView Style
        gold = yf.Ticker("GC=F").history(period="1d")
        btc = yf.Ticker("BTC-USD").history(period="1d")
        dxy = yf.Ticker("DX-Y.NYB").history(period="1d")
        yields = yf.Ticker("^TNX").history(period="1d")
        
        # News Fallback
        googlenews = GoogleNews(lang='fr', period='1d')
        googlenews.search('Gold Gold price')
        news_list = googlenews.results()[:6]
        
        p_gold = gold['Close'].iloc[-1]
        c_gold = ((p_gold - gold['Open'].iloc[-1]) / gold['Open'].iloc[-1]) * 100
        
        return {
            "p_gold": p_gold, "c_gold": c_gold,
            "p_btc": btc['Close'].iloc[-1],
            "v_dxy": dxy['Close'].iloc[-1],
            "v_yields": yields['Close'].iloc[-1] / 10,
            "news": news_list,
            "time": datetime.now().strftime("%H:%M:%S")
        }
    except:
        return None

data = get_market_intelligence()

if data:
    # --- CSS SUR MESURE KILLZONE ---
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500&display=swap');
        .stApp {{ background-color: #050505; }}
        .main-container {{ color: #e0e0e0; font-family: 'Inter', sans-serif; }}
        .header-box {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #222; padding: 10px 0; margin-bottom: 30px; }}
        .gold-price {{ color: #00ff88; font-size: 24px; font-weight: bold; border: 1px solid #00ff88; padding: 5px 15px; border-radius: 4px; background: rgba(0,255,136,0.05); }}
        .card {{ background: #0d0d0d; border: 1px solid #1a1a1a; padding: 25px; border-radius: 4px; height: 100%; }}
        .section-title {{ color: #666; font-size: 11px; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 20px; font-weight: bold; }}
        .metric-value {{ font-family: 'JetBrains Mono', monospace; font-size: 28px; font-weight: 500; }}
        .news-box {{ border-left: 2px solid #ffb000; padding-left: 15px; margin-bottom: 15px; }}
        .news-title {{ font-size: 13px; color: #eee; text-decoration: none; }}
        .footer-bar {{ background: #00ff88; color: #000; text-align: center; padding: 15px; font-weight: bold; font-size: 20px; text-transform: uppercase; margin-top: 30px; }}
    </style>
    """, unsafe_allow_html=True)

    # --- LAYOUT ---
    st.markdown(f"""
    <div class="main-container">
        <div class="header-box">
            <div><span style="color:#ffb000; font-weight:bold; font-size:20px;">BEE-INVEST</span> <span style="color:#444; margin-left:10px;">INTELLIGENCE D'OR</span></div>
            <div class="gold-price">XAU / USD : {data['p_gold']:,.2f} $</div>
            <div style="text-align:right; font-size:11px; color:#555;">LIVE : {data['time']} GMT+1<br>REFRESH : OK</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="section-title">● LIVE MARKET NARRATIVE</div>
            <div style="margin-bottom:30px;">
                <div style="color:#ffb000; font-size:16px; margin-bottom:10px;"><b>ACTUALITÉ RÉELLE DU MARCHÉ</b></div>
                {"".join([f"<div class='news-box'><div style='color:#666; font-size:10px;'>{n.get('date')}</div><div class='news-title'>{n.get('title')}</div></div>" for n in data['news']])}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="section-title">● SYNCHRONISATION ZONE</div>
            <div style="margin-bottom:20px;">
                <small style="color:#555;">INDICE DOLLAR (DXY)</small><br>
                <span class="metric-value" style="color:#00ff88;">{data['v_dxy']:.2f}</span>
            </div>
            <div style="margin-bottom:20px;">
                <small style="color:#555;">TAUX US 10Y</small><br>
                <span class="metric-value">{data['v_yields']:.2f}%</span>
            </div>
            <div style="margin-bottom:20px;">
                <small style="color:#555;">BITCOIN (BTC)</small><br>
                <span class="metric-value" style="color:#58a6ff;">{data['p_btc']:,.0f} $</span>
            </div>
            <hr style="border:0; border-top:1px solid #222; margin:30px 0;">
            <div style="text-align:center;">
                <div style="color:#ffb000; font-size:14px; font-weight:bold;">BIAIS : NEUTRE</div>
                <div style="background:#1a1a1a; padding:15px; margin-top:10px;">
                    <small style="color:#444;">LOTS CONSEILLÉS</small><br>
                    <span style="font-size:22px; font-weight:bold; color:#ffb000;">LOT 0.00</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""<div class="footer-bar">Confluence Analysée - Attente Signal Technique</div>""", unsafe_allow_html=True)
