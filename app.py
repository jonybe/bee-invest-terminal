import streamlit as st
import yfinance as yf
import feedparser
from datetime import datetime, timedelta

# 1. Configuration & Design System (KILLZONE THEME V1.3 - UI FIX)
st.set_page_config(page_title="KILLZONE | Gold Intelligence", layout="wide", initial_sidebar_state="collapsed")

if 'last_m5_ts' not in st.session_state:
    st.session_state.last_m5_ts = None

# CSS "KILLZONE" - Dark Mode Institutionnel
st.markdown("""
<style>
    * { --st-fragment-fade-opacity: 1 !important; --st-fragment-fade-duration: 0ms !important; }
    div[data-testid="stAppViewBlockContainer"], div[data-testid="stVerticalBlock"],
    div[data-fragment-component-id], [data-testid="stFragment"], [data-testid="stFragment"] > div {
        opacity: 1 !important; transition: none !important; animation: none !important; filter: blur(0px) !important;
    }
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #0b0b0b !important; 
        color: #a1a1aa; 
        font-family: 'Inter', -apple-system, sans-serif; 
        font-size: 11px; 
    }
    .block-container { padding-top: 2rem !important; padding-bottom: 0rem !important; max-width: 1600px; }
    
    .kz-panel { background: #111111; border: 1px solid #222222; border-radius: 6px; padding: 16px; margin-bottom: 16px; }
    .kz-header { font-size: 10px; font-weight: 800; color: #a1a1aa; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 16px; display: flex; align-items: center; }
    .kz-header::before { content: '●'; color: #eab308; margin-right: 8px; font-size: 12px; }
    
    .kz-topbar { display: flex; justify-content: space-between; align-items: center; background: #111; padding: 12px 24px; border-bottom: 1px solid #222; border-radius: 6px; margin-bottom: 20px; }
    .kz-topbar-item { display: flex; flex-direction: column; }
    .kz-label { font-size: 8px; color: #71717a; text-transform: uppercase; font-weight: bold; margin-bottom: 2px; }
    .kz-val { font-size: 14px; color: #e4e4e7; font-weight: bold; font-family: 'JetBrains Mono', monospace; }
    
    .flow-container { margin-bottom: 24px; }
    .flow-meta { display: flex; justify-content: space-between; margin-bottom: 6px; font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: bold; }
    .flow-bar-wrapper { display: flex; height: 12px; border-radius: 2px; overflow: hidden; background: #ef4444; }
    .flow-bar-green { height: 100%; background: #10b981; transition: width 0.5s ease-in-out; }
    
    .badge-center { text-align: center; background: #18181b; border: 1px solid #27272a; padding: 4px 16px; border-radius: 4px; display: inline-block; transform: translateY(-10px); }
    
    .session-box { border: 1px solid #222; border-radius: 6px; padding: 12px; margin-bottom: 8px; background: #0f0f11; }
    .session-active { border: 1px solid #eab308; background: rgba(234, 179, 8, 0.05); }
    .session-title { font-size: 11px; font-weight: bold; color: #e4e4e7; display: flex; justify-content: space-between; margin-bottom: 4px; }
    .session-active .session-title { color: #eab308; }
    .session-desc { font-size: 10px; color: #71717a; line-height: 1.4; }
    
    .text-green { color: #10b981 !important; }
    .text-red { color: #ef4444 !important; }
    .text-gold { color: #eab308 !important; }
</style>
""", unsafe_allow_html=True)

@st.fragment(run_every=3)
def sync_terminal():
    try:
        # 1. FETCH DATA (Yahoo Finance - Free Data)
        t = yf.Ticker("GC=F")
        gold = t.fast_info['last_price']
        prev_close = t.fast_info['previous_close']
        daily_change = ((gold - prev_close) / prev_close) * 100
        
        pct_color = "text-green" if daily_change > 0 else "text-red"
        pct_sign = "+" if daily_change > 0 else ""
        
        df_m15 = t.history(period="2d", interval="15m").dropna()
        m15_imp = ((gold - df_m15['Close'].iloc[-2]) / df_m15['Close'].iloc[-2]) * 100
        
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        yields = yf.Ticker("^TNX").fast_info['last_price'] / 10
        vix = yf.Ticker("^VIX").fast_info['last_price']
        
        # 2. ALGORITHME DE SCORING (Approximation par défaut)
        h4_s = min(max(50 + (daily_change * 50), 10), 90)
        h2_s = min(max(50 + (m15_imp * 200), 10), 90)
        m15_s = min(max(50 + (m15_imp * 400), 0), 100)
        
        drag = (dxy - 100) + (yields * 5) + (vix * 0.5)
        bull_score = min(max(65.0 - drag + (m15_imp * 35), 10), 100)
        
        bias_label = "BULLISH" if bull_score > 55 else "BEARISH" if bull_score < 45 else "NEUTRAL"
        bias_col = "#10b981" if bias_label == "BULLISH" else "#ef4444" if bias_label == "BEARISH" else "#eab308"
        
        regime = "RANGE" if 45 < bull_score < 55 and vix < 20 else "TRENDING" if bull_score >= 55 or bull_score <= 45 else "VOL EXPANSION"
        
        # 3. TIMING & SESSIONS
        now = datetime.utcnow() + timedelta(hours=2)
        time_str = now.strftime("%H:%M:%S")
        hour = now.hour
        
        asia_active = 2 <= hour < 10
        london_active = 9 <= hour < 17
        ny_active = 14 <= hour < 22
        
        asia_cls = "session-active" if asia_active else ""
        lon_cls = "session-active" if london_active else ""
        ny_cls = "session-active" if ny_active else ""
        
        asia_stat = "LIVE" if asia_active else "CLOSED"
        lon_stat = "LIVE" if london_active else "CLOSED"
        ny_stat = "LIVE" if ny_active else "CLOSED"
        
        # --- RENDER TOP BAR ---
        topbar_html = f"""
        <div class="kz-topbar">
            <div style="display:flex; align-items:center; gap:16px;">
                <div style="background:#eab308; color:#000; font-weight:900; padding:6px 10px; border-radius:4px; font-size:14px;">K</div>
                <div><div style="color:#e4e4e7; font-weight:800; font-size:14px; letter-spacing:1px;">KILLZONE <span style="color:#71717a; font-weight:normal;">| BEE-INVEST INTEL</span></div></div>
            </div>
            <div class="kz-topbar-item"><span class="kz-label">ASSET</span><span class="kz-val" style="color:#eab308;">XAU / USD</span></div>
            <div class="kz-topbar-item"><span class="kz-label">PRICE</span><span class="kz-val" style="color:#e4e4e7;">${gold:,.2f} <small class="{pct_color}">{pct_sign}{daily_change:.2f}%</small></span></div>
            <div class="kz-topbar-item"><span class="kz-label">SCORE</span><span class="kz-val text-gold">{int(bull_score)} {bias_label}</span></div>
            <div class="kz-topbar-item"><span class="kz-label">LOCAL TIME</span><span class="kz-val">{time_str}</span></div>
        </div>
        """
        st.markdown(topbar_html, unsafe_allow_html=True)

        c1, c2 = st.columns([1.8, 1.2], gap="large")
        
        with c1:
            st.markdown("""<div class="kz-panel"><div class="kz-header">BULL VS BEAR · DOMINANCE</div>""", unsafe_allow_html=True)
            for tf, val, label in [("INTRADAY FLOW (4H)", h4_s, "MACRO TREND"), ("INTRADAY FLOW (2H)", h2_s, "CONFIRMATION"), ("FAST FLOW (15M)", m15_s, "EXECUTION")]:
                lean = "LEANING BULLISH" if val > 50 else "LEANING BEARISH"
                l_col = "#10b981" if val > 50 else "#ef4444"
                flow_html = f"""
                <div class="flow-container">
                    <div style="font-size:9px; color:#71717a; margin-bottom:8px; text-transform:uppercase;">{tf}</div>
                    <div class="flow-meta"><span class="text-green">{val:.1f}%</span><span class="text-red">{100-val:.1f}%</span></div>
                    <div class="flow-bar-wrapper"><div class="flow-bar-green" style="width:{val}%;"></div></div>
                    <div style="text-align:center;"><div class="badge-center"><div style="font-size:7px; color:#71717a; text-transform:uppercase;">{label}</div><div style="font-size:9px; font-weight:900; color:{l_col};">{lean}</div></div></div>
                </div>
                """
                st.markdown(flow_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # --- CORRECTION DU BUG VISUEL ICI ---
            supp_val = max(0, m15_imp*15)
            opp_val = min(0, m15_imp*15)
            forces_html = f"""
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:16px;">
                <div style="background:#0f0f11; border:1px solid #222; border-radius:6px; padding:16px; border-top:2px solid #10b981;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                        <div class="kz-header" style="margin:0;">SUPPORTING FORCES</div>
                        <div class="text-green" style="font-family:'JetBrains Mono'; font-size:16px; font-weight:bold;">+{supp_val:.2f}</div>
                    </div>
                    <div style="font-size:10px; color:#71717a; border-bottom:1px solid #222; padding-bottom:6px; margin-bottom:6px;">
                        <span style="background:#18181b; padding:2px 6px; border-radius:2px; color:#10b981;">XAU Momentum</span>
                    </div>
                    <div style="font-size:9px; color:#a1a1aa; line-height:1.5;">Near-term leg showing strength. Tape indicates aggressive bidding on dips. Score above neutral blends implies continuation.</div>
                </div>
                
                <div style="background:#0f0f11; border:1px solid #222; border-radius:6px; padding:16px; border-top:2px solid #ef4444;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                        <div class="kz-header" style="margin:0;">OPPOSING FORCES</div>
                        <div class="text-red" style="font-family:'JetBrains Mono'; font-size:16px; font-weight:bold;">{opp_val:.2f}</div>
                    </div>
                    <div style="font-size:10px; color:#71717a; border-bottom:1px solid #222; padding-bottom:6px; margin-bottom:6px;">
                        <span style="background:#18181b; padding:2px 6px; border-radius:2px; color:#ef4444;">Risk Pulse / USD</span>
                    </div>
                    <div style="font-size:9px; color:#a1a1aa; line-height:1.5;">VIX currently at {vix:.1f}. Higher real yields increase carry pressure on non-yielding gold and weaken safe-haven score.</div>
                </div>
            </div>
            """
            st.markdown(forces_html, unsafe_allow_html=True)

            inval_html = """
            <div class="kz-panel">
                <div class="kz-header" style="justify-content:space-between;"><span>INVALIDATION CONDITIONS</span><span style="font-size:8px; font-weight:normal; color:#71717a;">WHAT WOULD BREAK THIS NARRATIVE</span></div>
                <div style="display:flex; align-items:center; border-bottom:1px solid #222; padding:10px 0;">
                    <div style="width:30px; font-family:'JetBrains Mono'; color:#71717a; font-size:10px;">01</div>
                    <div style="flex:1;"><div style="color:#e4e4e7; font-size:11px; font-weight:bold;">Real yields rise above <span class="text-gold">2.00%</span></div><div style="color:#71717a; font-size:10px;">Higher real yields increase carry pressure on non-yielding gold.</div></div>
                    <div style="background:#ef444422; color:#ef4444; border:1px solid #ef444455; padding:2px 8px; border-radius:4px; font-size:8px; font-weight:bold;">NEAR</div>
                </div>
                <div style="display:flex; align-items:center; padding:10px 0;">
                    <div style="width:30px; font-family:'JetBrains Mono'; color:#71717a; font-size:10px;">02</div>
                    <div style="flex:1;"><div style="color:#e4e4e7; font-size:11px; font-weight:bold;">USD broad index pushes above <span class="text-gold">106.50</span></div><div style="color:#71717a; font-size:10px;">Dollar strength typically tightens financial conditions and caps upside.</div></div>
                    <div style="background:#ef444422; color:#ef4444; border:1px solid #ef444455; padding:2px 8px; border-radius:4px; font-size:8px; font-weight:bold;">NEAR</div>
                </div>
            </div>
            """
            st.markdown(inval_html, unsafe_allow_html=True)

        with c2:
            timing_html = f"""
            <div class="kz-panel">
                <div class="kz-header">KILLZONE TIMING (UTC+2)</div>
                <div class="session-box {asia_cls}">
                    <div class="session-title"><span>● ASIA <span style="color:#71717a; font-size:9px; font-weight:normal; margin-left:8px;">02:00 - 10:00</span></span><span style="font-size:9px;">{asia_stat}</span></div>
                    <div class="session-desc">Typically range-bound. Liquidity thin ex-China — positioning into London open matters more than price.</div>
                </div>
                <div class="session-box {lon_cls}">
                    <div class="session-title"><span>● LONDON <span style="color:#71717a; font-size:9px; font-weight:normal; margin-left:8px;">09:00 - 17:00</span></span><span style="font-size:9px;">{lon_stat}</span></div>
                    <div class="session-desc">Highest edge for breakout execution. Expect sharp directional moves if narrative pressure is unresolved.</div>
                </div>
                <div class="session-box {ny_cls}">
                    <div class="session-title"><span>● NEW YORK <span style="color:#71717a; font-size:9px; font-weight:normal; margin-left:8px;">15:00 - 23:00</span></span><span style="font-size:9px;">{ny_stat}</span></div>
                    <div class="session-desc">Overlap hour drives two-way flow. DXY-correlated — watch cross-market reactions around U.S. data.</div>
                </div>
            </div>
            """
            st.markdown(timing_html, unsafe_allow_html=True)

            bias_html = f"""
            <div class="kz-panel">
                <div class="kz-header">POSITIONING BIAS</div>
                <div style="display:flex; align-items:center; margin-bottom:16px;">
                    <div style="width:60px; height:60px; border-radius:50%; border:2px solid {bias_col}; display:flex; flex-direction:column; align-items:center; justify-content:center; margin-right:16px;">
                        <span style="font-size:8px; color:#71717a;">BIAS</span><span style="font-size:10px; font-weight:bold; color:{bias_col};">{bias_label}</span>
                    </div>
                    <div>
                        <div style="color:#e4e4e7; font-size:12px; font-weight:bold; margin-bottom:4px;">Defensive framing — respect the flow.</div>
                        <div style="color:#71717a; font-size:10px;">The score is {int(bull_score)}. Treat counter-trend moves as fragile until yields or the dollar turn.</div>
                    </div>
                </div>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                    <div style="background:#18181b; padding:10px; border-radius:4px; border:1px solid #27272a;"><div style="color:#e4e4e7; font-size:9px; font-weight:bold; margin-bottom:4px;">⏱ PATIENCE</div><div style="color:#71717a; font-size:9px;">Wait for clear 15m momentum alignment.</div></div>
                    <div style="background:#18181b; padding:10px; border-radius:4px; border:1px solid #27272a;"><div style="color:#e4e4e7; font-size:9px; font-weight:bold; margin-bottom:4px;">⚖️ ASYMMETRY</div><div style="color:#71717a; font-size:9px;">Deploy only when invalidation is tight.</div></div>
                </div>
            </div>
            """
            st.markdown(bias_html, unsafe_allow_html=True)

            rg_bd = '#eab308' if regime == 'RANGE' else '#222'
            rg_bg = 'rgba(234, 179, 8, 0.05)' if regime == 'RANGE' else '#0f0f11'
            rg_co = '#eab308' if regime == 'RANGE' else '#71717a'
            tr_bd = '#eab308' if regime == 'TRENDING' else '#222'
            tr_bg = 'rgba(234, 179, 8, 0.05)' if regime == 'TRENDING' else '#0f0f11'
            tr_co = '#eab308' if regime == 'TRENDING' else '#71717a'
            vl_bd = '#eab308' if regime == 'VOL EXPANSION' else '#222'
            vl_bg = 'rgba(234, 179, 8, 0.05)' if regime == 'VOL EXPANSION' else '#0f0f11'
            vl_co = '#eab308' if regime == 'VOL EXPANSION' else '#71717a'

            regime_html = f"""
            <div class="kz-panel">
                <div class="kz-header">MARKET REGIME</div>
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; margin-bottom:16px;">
                    <div style="border:1px solid {rg_bd}; text-align:center; padding:12px 0; border-radius:4px; background:{rg_bg}; color:{rg_co};">⟷<br><span style="font-size:9px; font-weight:bold;">RANGE</span></div>
                    <div style="border:1px solid {tr_bd}; text-align:center; padding:12px 0; border-radius:4px; background:{tr_bg}; color:{tr_co};">↗<br><span style="font-size:9px; font-weight:bold;">TRENDING</span></div>
                    <div style="border:1px solid {vl_bd}; text-align:center; padding:12px 0; border-radius:4px; background:{vl_bg}; color:{vl_co};">~<br><span style="font-size:9px; font-weight:bold;">VOLATILITY</span></div>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; border-top:1px solid #222; padding-top:12px;">
                    <div><div style="font-size:8px; color:#71717a; text-transform:uppercase;">REAL YIELD</div><div style="font-family:'JetBrains Mono'; font-size:14px; font-weight:bold; color:#e4e4e7;">{yields:.2f}%</div></div>
                    <div><div style="font-size:8px; color:#71717a; text-transform:uppercase;">VIX</div><div style="font-family:'JetBrains Mono'; font-size:14px; font-weight:bold; color:#e4e4e7;">{vix:.1f}</div></div>
                    <div><div style="font-size:8px; color:#71717a; text-transform:uppercase;">USD BROAD</div><div style="font-family:'JetBrains Mono'; font-size:14px; font-weight:bold; color:#e4e4e7;">{dxy:.1f}</div></div>
                </div>
            </div>
            """
            st.markdown(regime_html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Sync issue: {e}")

sync_terminal()
