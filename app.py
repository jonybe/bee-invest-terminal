import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# 1. Config Pro / Wide Mode
st.set_page_config(page_title="BEE-INVEST | TERMINAL", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=30000, key="datarefresh") # 30s refresh

def get_terminal_data():
    try:
        # Finance Data
        gold = yf.Ticker("GC=F").history(period="1d")
        btc = yf.Ticker("BTC-USD").history(period="1d")
        dxy = yf.Ticker("DX-Y.NYB").history(period="1d")
        yields = yf.Ticker("^TNX").history(period="1d")
        
        # Real-time News via RSS (Finviz - Plus robuste que Yahoo/Google)
        feed = feedparser.parse("https://www.google.com/search?q=gold+market+news&tbm=nws&output=rss")
        news = feed.entries[:8]
        
        return {
            "p_gold": gold['Close'].iloc[-1],
            "p_btc": btc['Close'].iloc[-1],
            "v_dxy": dxy['Close'].iloc[-1],
            "v_yields": yields['Close'].iloc[-1] / 10,
            "news": news,
            "time": datetime.now().strftime("%H:%M:%S")
        }
    except Exception as e:
        return None

d = get_terminal_data()

# --- CSS ARCHITECTURE PROFESSIONNELLE ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;600&display=swap');
    
    .stApp {{ background-color: #050505; }}
    html, body, [data-testid="stAppViewContainer"] {{ background-color: #050505; color: #e0e0e0; font-family: 'Inter', sans-serif; }}
    
    /* Header Style */
    .kz-header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #222; padding: 10px 0; margin-bottom: 25px; }}
    .gold-glow {{ border: 1px solid #00ff88; color: #00ff88; padding: 8px 20px; font-weight: bold; font-family: 'JetBrains Mono'; border-radius: 4px; background: rgba(0,255,136,0.05); font-size: 22px; }}
    
    /* Grid & Cards */
    .kz-card {{ background: #0d0d0d; border: 1px solid #1a1a1a; padding: 25px; border-radius: 4px; height: 100%; }}
    .section-label {{ color: #555; font-size: 10px; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 20px; font-weight: 700; }}
    
    /* Metrics */
    .val-large {{ font-family: 'JetBrains Mono'; font-size: 32px; font-weight: 700; color: #00ff88; margin-bottom: 5px; }}
    .val-sub {{ font-family: 'JetBrains Mono'; font-size: 11px; color: #444; }}
    
    /* News Feed Style */
    .news-line {{ border-left: 2px solid #ffb000; padding: 12px 15px; margin-bottom: 12px; background: rgba(255,176,0,0.02); transition: 0.3s; }}
    .news-line:hover {{ background: rgba(255,176,0,0.05); }}
    .news-time {{ font-size: 10px; color: #444; font-family: 'JetBrains Mono'; }}
    .news-txt {{ font-size: 13px; color: #ccc; line-height: 1.4; }}
    
    /* Verdict Footer */
    .footer {{ background: #00ff88; color: #000; text-align: center; padding: 20px; font-weight: 900; font-size: 22px; text-transform: uppercase; border-radius: 4px; margin-top: 30px; letter-spacing: 1px; }}
</style>
""", unsafe_allow_html=True)

if d:
    # HEADER
    st.markdown(f"""
    <div class="kz-header">
        <div><b style="color:#ffb000; font-size:24px; letter-spacing:-1px;">BEE-INVEST</b> <span style="color:#333; margin-left:10px; font-size:12px;">GOLD INTELLIGENCE UNIT</span></div>
        <div class="gold-glow">XAU / USD : {d['p_gold']:,.2f} $</div>
        <div style="text-align:right; line-height:1.2;">
            <span style="color:#666; font-size:10px;">LIVE : {d['time']} GMT+1</span><br>
            <span style="color:#00ff88; font-size:10px;">● CONNECTED</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([2.5, 1])

    with c1:
        # NEWS SECTION
        news_html = "".join([
            f"<div class='news-line'><div class='news-time'>{n.published[:25] if 'published' in n else 'LIVE'}</div><div class='news-txt'>{n.title}</div></div>" 
            for n in d['news']
        ])
        st.markdown(f"""
        <div class="kz-card">
            <div class="section-label">● LIVE MARKET NARRATIVE</div>
            <div style="margin-top:10px;">{news_html if news_html else "SYNCHRONISATION DU FLUX..."}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        # MACRO SECTION
        st.markdown(f"""
        <div class="kz-card">
            <div class="section-label">● SYNCHRONISATION ZONE</div>
            
            <div style="margin-bottom:35px;">
                <small style="color:#444;">INDICE DOLLAR (DXY)</small><br>
                <div class="val-large">{d['v_dxy']:.2f}</div>
            </div>
            
            <div style="margin-bottom:35px;">
                <small style="color:#444;">TAUX US 10Y</small><br>
                <div class="val-large" style="color:#eee;">{d['v_yields']:.2f}%</div>
            </div>
            
            <div style="margin-bottom:35px;">
                <small style="color:#444;">BITCOIN (BTC)</small><br>
                <div class="val-large" style="color:#58a6ff;">{d['p_btc']:,.0f} $</div>
            </div>

            <div style="border-top:1px solid #1a1a1a; padding-top:25px; text-align:center;">
                <div style="color:#ffb000; font-weight:bold; font-size:16px;">BIAIS : NEUTRE</div>
                <div style="background:#111; padding:20px; border-radius:4px; margin-top:15px; border:1px solid #222;">
                    <small style="color:#444; font-size:10px;">RISQUE CALCULÉ</small><br>
                    <div style="font-size:28px; font-weight:700; color:#00ff88; font-family:'JetBrains Mono';">LOT 0.00</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""<div class="footer">Confluence Analysée - Attente Signal Technique</div>""", unsafe_allow_html=True)
else:
    st.error("RÉTABLISSEMENT DU FLUX DE DONNÉES...")
