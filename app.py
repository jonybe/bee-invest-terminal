import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import random

# ==========================================
# 1. Configuration & Design System (KILLZONE V2 - ORDER FLOW)
# ==========================================
st.set_page_config(page_title="KILLZONE | Order Flow Engine", layout="wide", initial_sidebar_state="collapsed")

if 'last_m5_ts' not in st.session_state:
    st.session_state.last_m5_ts = None

st.markdown("""
<style>
    * { --st-fragment-fade-opacity: 1 !important; --st-fragment-fade-duration: 0ms !important; }
    div[data-testid="stAppViewBlockContainer"], div[data-testid="stVerticalBlock"],
    div[data-fragment-component-id], [data-testid="stFragment"], [data-testid="stFragment"] > div {
        opacity: 1 !important; transition: none !important; animation: none !important; filter: blur(0px) !important;
    }
    html, body, [data-testid="stAppViewContainer"] { background-color: #0b0b0b !important; color: #a1a1aa; font-family: 'Inter', -apple-system, sans-serif; font-size: 11px; }
    .block-container { padding-top: 2rem !important; padding-bottom: 0rem !important; max-width: 1600px; }
    
    /* Composants KILLZONE Base */
    .kz-panel { background: #111111; border: 1px solid #222222; border-radius: 6px; padding: 16px; margin-bottom: 16px; }
    .kz-header { font-size: 10px; font-weight: 800; color: #a1a1aa; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 16px; display: flex; align-items: center; }
    .kz-header::before { content: '●'; color: #eab308; margin-right: 8px; font-size: 12px; }
    .kz-topbar { display: flex; justify-content: space-between; align-items: center; background: #111; padding: 12px 24px; border-bottom: 1px solid #222; border-radius: 6px; margin-bottom: 20px; }
    .kz-topbar-item { display: flex; flex-direction: column; }
    .kz-label { font-size: 8px; color: #71717a; text-transform: uppercase; font-weight: bold; margin-bottom: 2px; }
    .kz-val { font-size: 14px; color: #e4e4e7; font-weight: bold; font-family: 'JetBrains Mono', monospace; }
    
    /* Layouts & Utilitaires */
    .flow-container { margin-bottom: 24px; }
    .flow-meta { display: flex; justify-content: space-between; margin-bottom: 6px; font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: bold; }
    .flow-bar-wrapper { display: flex; height: 12px; border-radius: 2px; overflow: hidden; background: #ef4444; }
    .flow-bar-green { height: 100%; background: #10b981; transition: width 0.5s ease-in-out; }
    .badge-center { text-align: center; background: #18181b; border: 1px solid #27272a; padding: 4px 16px; border-radius: 4px; display: inline-block; transform: translateY(-10px); }
    .text-green { color: #10b981 !important; }
    .text-red { color: #ef4444 !important; }
    .text-gold { color: #eab308 !important; }

    /* ORDER FLOW SPECIFIC STYLES */
    .dom-heatmap { background: #0f0f11; border: 1px solid #222; border-radius: 6px; padding: 12px; }
    .dom-row { display: flex; align-items: center; font-family: 'JetBrains Mono'; font-size: 11px; margin-bottom: 2px; }
    .dom-price { width: 60px; text-align: right; margin-right: 12px; color: #71717a; }
    .dom-price.current { color: #eab308; font-weight: 900; font-size: 13px; }
    .dom-bar-container { flex: 1; height: 16px; background: #18181b; position: relative; border-radius: 2px; overflow: hidden; }
    .dom-bar-ask { position: absolute; left: 0; top: 0; height: 100%; background: rgba(239, 68, 68, 0.6); border-right: 2px solid #ef4444; }
    .dom-bar-bid { position: absolute; left: 0; top: 0; height: 100%; background: rgba(16, 185, 129, 0.6); border-right: 2px solid #10b981; }
    .dom-vol { position: absolute; right: 8px; top: 1px; color: #fff; font-size: 9px; font-weight: bold; text-shadow: 1px 1px 0 #000; }
    
    .setup-alert { background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; border-left: 4px solid #10b981; padding: 12px; border-radius: 4px; margin-top: 16px; animation: pulse 2s infinite; }
    .setup-alert.bear { background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; border-left: 4px solid #ef4444; }
    @keyframes pulse { 0% { opacity: 0.8; } 50% { opacity: 1; } 100% { opacity: 0.8; } }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LE MOTEUR (Logique & Données)
# ==========================================
@st.fragment(run_every=2)
def order_flow_engine():
    try:
        # A. Fetch Real Basic Data (Carburant gratuit)
        t = yf.Ticker("GC=F")
        gold = t.fast_info['last_price']
        prev_close = t.fast_info['previous_close']
        daily_change = ((gold - prev_close) / prev_close) * 100
        
        dxy = yf.Ticker("DX-Y.NYB").fast_info['last_price']
        # Simulation du filtre DXY (Vrai : Neutre/Baisse = Bon pour l'Or | Faux : Hausse forte = Danger)
        dxy_is_safe = True if dxy < 105.5 else False 

        # B. Simulation Level 2 (Carnet d'Ordres Institutionnel)
        # On génère des "murs" réalistes autour du vrai prix de l'or
        base_vol = random.randint(50, 150)
        
        # Scénario : On simule qu'un gros acteur veut acheter (Bid Wall)
        big_bid_price = round(gold - 1.5, 1) # Mur juste en dessous
        big_ask_price = round(gold + 4.0, 1) # Mur vendeur lointain
        
        dom_data = []
        total_ask_vol = 0
        total_bid_vol = 0
        
        # Création de 11 niveaux de prix (5 au-dessus, le prix actuel, 5 en dessous)
        for i in range(5, -6, -1):
            p = round(gold + (i * 0.5), 1)
            is_ask = p > gold
            is_current = p == round(gold, 1)
            
            # Injection de volume
            if p == big_ask_price: vol = random.randint(800, 1200)
            elif p == big_bid_price: vol = random.randint(1500, 2500) # LE GROS MUR ACHETEUR
            else: vol = base_vol + random.randint(-20, 80)
            
            if is_current: vol = 0
            
            # Calcul de l'Imbalance
            if is_ask: total_ask_vol += vol
            elif not is_current: total_bid_vol += vol
                
            dom_data.append({"price": p, "vol": vol, "type": "ask" if is_ask else ("current" if is_current else "bid")})

        # C. L'Algorithme de Détection (Ratio 2.7 + DXY)
        # Règle 1: L'imbalance doit être de 2.7x
        # Règle 2: Le filtre DXY doit être validé
        dom_ratio = (total_bid_vol / max(1, total_ask_vol)) if total_bid_vol > total_ask_vol else (total_ask_vol / max(1, total_bid_vol))
        is_bull_imbalance = total_bid_vol > (total_ask_vol * 2.7)
        is_bear_imbalance = total_ask_vol > (total_bid_vol * 2.7)

        setup_triggered = False
        setup_type = ""
        setup_msg = ""
        
        if is_bull_imbalance and dxy_is_safe:
            setup_triggered = True
            setup_type = "bull"
            setup_msg = f"ABSORPTION BULLISH DETECTED | RATIO {dom_ratio:.1f}x | DXY SAFE"
        elif is_bear_imbalance:
            # Pour le short de l'or, on veut que le DXY soit fort (on ignore le dxy_safe ici)
            setup_triggered = True
            setup_type = "bear"
            setup_msg = f"ABSORPTION BEARISH DETECTED | RATIO {dom_ratio:.1f}x"

        # D. Simulation Volume Profile (Value Area)
        poc = round(gold - 1.2, 1) # Le POC est proche du gros mur acheteur
        vah = poc + 6.0
        val = poc - 4.0

        # ==========================================
        # 3. L'INTERFACE VISUELLE (Le Cockpit)
        # ==========================================
        now = datetime.utcnow() + timedelta(hours=2)
        time_str = now.strftime("%H:%M:%S")
        
        pct_color = "text-green" if daily_change > 0 else "text-red"
        pct_sign = "+" if daily_change > 0 else ""

        # TOP BAR
        topbar_html = f"""
        <div class="kz-topbar">
            <div style="display:flex; align-items:center; gap:16px;">
                <div style="background:#eab308; color:#000; font-weight:900; padding:6px 10px; border-radius:4px; font-size:14px;">K</div>
                <div><div style="color:#e4e4e7; font-weight:800; font-size:14px; letter-spacing:1px;">KILLZONE <span style="color:#71717a; font-weight:normal;">| V2 ORDER FLOW</span></div></div>
            </div>
            <div class="kz-topbar-item"><span class="kz-label">ASSET</span><span class="kz-val" style="color:#eab308;">XAU / USD</span></div>
            <div class="kz-topbar-item"><span class="kz-label">SPOT PRICE</span><span class="kz-val" style="color:#e4e4e7;">${gold:,.2f} <small class="{pct_color}">{pct_sign}{daily_change:.2f}%</small></span></div>
            <div class="kz-topbar-item"><span class="kz-label">DXY FILTER</span><span class="kz-val {'text-green' if dxy_is_safe else 'text-red'}">{dxy:.2f} ({'SAFE' if dxy_is_safe else 'DANGER'})</span></div>
            <div class="kz-topbar-item"><span class="kz-label">LOCAL TIME</span><span class="kz-val">{time_str}</span></div>
        </div>
        """
        st.markdown(topbar_html, unsafe_allow_html=True)

        c1, c2 = st.columns([1.2, 1.8], gap="large")
        
        with c1:
            # MODULE 1: VOLUME PROFILE MAPPING
            st.markdown("""<div class="kz-panel"><div class="kz-header">INSTITUTIONAL ZONES (VOLUME PROFILE)</div>""", unsafe_allow_html=True)
            vp_html = f"""
            <div style="display:flex; flex-direction:column; gap:12px;">
                <div style="display:flex; justify-content:space-between; border-bottom:1px solid #222; padding-bottom:8px;">
                    <div><span style="font-size:9px; color:#71717a;">VAH (Value Area High)</span><br><span style="font-family:'JetBrains Mono'; font-weight:bold; color:#e4e4e7;">{vah:.1f}</span></div>
                    <div style="text-align:right;"><span style="font-size:9px; color:#ef4444;">RESISTANCE</span><br><span style="font-size:10px; color:#71717a;">70% Vol Boundary</span></div>
                </div>
                <div style="display:flex; justify-content:space-between; border-bottom:1px solid #222; padding-bottom:8px;">
                    <div><span style="font-size:9px; color:#eab308; font-weight:bold;">POC (Point of Control)</span><br><span style="font-family:'JetBrains Mono'; font-weight:900; color:#eab308; font-size:14px;">{poc:.1f}</span></div>
                    <div style="text-align:right;"><span style="font-size:9px; color:#eab308;">MAGNET</span><br><span style="font-size:10px; color:#71717a;">Max Volume Node</span></div>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <div><span style="font-size:9px; color:#71717a;">VAL (Value Area Low)</span><br><span style="font-family:'JetBrains Mono'; font-weight:bold; color:#e4e4e7;">{val:.1f}</span></div>
                    <div style="text-align:right;"><span style="font-size:9px; color:#10b981;">SUPPORT</span><br><span style="font-size:10px; color:#71717a;">70% Vol Boundary</span></div>
                </div>
            </div>
            </div>
            """
            st.markdown(vp_html, unsafe_allow_html=True)

            # MODULE 2: ALGORITHM METRICS
            st.markdown("""<div class="kz-panel"><div class="kz-header">ENGINE TELEMETRY (PARAMS)</div>""", unsafe_allow_html=True)
            metrics_html = f"""
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                <div style="background:#18181b; padding:10px; border-radius:4px; border:1px solid #27272a;">
                    <div style="color:#71717a; font-size:8px; font-weight:bold; margin-bottom:4px;">REQUIRED RATIO</div>
                    <div style="color:#e4e4e7; font-size:14px; font-family:'JetBrains Mono'; font-weight:bold;">2.7x</div>
                </div>
                <div style="background:#18181b; padding:10px; border-radius:4px; border:1px solid #27272a;">
                    <div style="color:#71717a; font-size:8px; font-weight:bold; margin-bottom:4px;">CURRENT IMBALANCE</div>
                    <div style="color:{'#10b981' if dom_ratio >= 2.7 else '#eab308'}; font-size:14px; font-family:'JetBrains Mono'; font-weight:bold;">{dom_ratio:.2f}x</div>
                </div>
                <div style="background:#18181b; padding:10px; border-radius:4px; border:1px solid #27272a;">
                    <div style="color:#71717a; font-size:8px; font-weight:bold; margin-bottom:4px;">BID LIQUIDITY (BUYERS)</div>
                    <div style="color:#10b981; font-size:12px; font-family:'JetBrains Mono';">{total_bid_vol} Lots</div>
                </div>
                <div style="background:#18181b; padding:10px; border-radius:4px; border:1px solid #27272a;">
                    <div style="color:#71717a; font-size:8px; font-weight:bold; margin-bottom:4px;">ASK LIQUIDITY (SELLERS)</div>
                    <div style="color:#ef4444; font-size:12px; font-family:'JetBrains Mono';">{total_ask_vol} Lots</div>
                </div>
            </div>
            </div>
            """
            st.markdown(metrics_html, unsafe_allow_html=True)

        with c2:
            # MODULE 3: THE HEATMAP (LEVEL 2 DOM)
            st.markdown("""<div class="kz-panel"><div class="kz-header">L2 HEATMAP / DEPTH OF MARKET</div>""", unsafe_allow_html=True)
            
            # Rendu du carnet d'ordres
            dom_html = "<div class='dom-heatmap'>"
            max_vol = max(total_bid_vol, total_ask_vol) if max(total_bid_vol, total_ask_vol) > 0 else 1
            
            for row in dom_data:
                p = f"{row['price']:.1f}"
                vol = row['vol']
                # On accentue visuellement les murs (plus de 500 lots)
                width_pct = min(100, (vol / 2500) * 100) if vol > 0 else 0 
                
                if row['type'] == "ask":
                    dom_html += f"""
                    <div class='dom-row'>
                        <div class='dom-price'>{p}</div>
                        <div class='dom-bar-container'><div class='dom-bar-ask' style='width:{width_pct}%;'></div><div class='dom-vol'>{vol if vol>0 else ''}</div></div>
                    </div>"""
                elif row['type'] == "current":
                    dom_html += f"""
                    <div class='dom-row' style='margin: 8px 0; background: rgba(234, 179, 8, 0.1); border-top: 1px solid #eab308; border-bottom: 1px solid #eab308;'>
                        <div class='dom-price current'>{p}</div>
                        <div class='dom-bar-container' style='background:transparent;'><div style='padding-left:8px; color:#eab308; font-size:9px; font-weight:bold; line-height:16px;'>SPOT PRICE (SPREAD)</div></div>
                    </div>"""
                else: # bid
                    dom_html += f"""
                    <div class='dom-row'>
                        <div class='dom-price'>{p}</div>
                        <div class='dom-bar-container'><div class='dom-bar-bid' style='width:{width_pct}%;'></div><div class='dom-vol'>{vol if vol>0 else ''}</div></div>
                    </div>"""
            
            dom_html += "</div>"
            st.markdown(dom_html, unsafe_allow_html=True)

            # ALERT TRIGGER
            if setup_triggered:
                cls = "setup-alert" if setup_type == "bull" else "setup-alert bear"
                st.markdown(f"""
                <div class="{cls}">
                    <div style="font-weight:900; font-size:12px; margin-bottom:4px;">{setup_msg}</div>
                    <div style="font-size:10px; color:#a1a1aa;">L'algorithme a détecté un mur massif absorbant la pression adverse. Zone de liquidité confirmée.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background:#0f0f11; border:1px dashed #27272a; padding:12px; border-radius:4px; margin-top:16px; text-align:center;">
                    <div style="color:#71717a; font-size:10px; font-weight:bold;">SCANNING LIQUIDITY...</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Engine Offline: {e}")

order_flow_engine()
