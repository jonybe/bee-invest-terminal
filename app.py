import streamlit as st
import requests
import random
import math

# 1. Configuration & Global Style
st.set_page_config(page_title="KILLZONE | Institutional Dashboard", layout="wide", initial_sidebar_state="collapsed")

API_KEY = "a640b1ef6a07445695f0fc9c34359160"

# CSS ANTI-FLICKER & DESIGN PRO
st.markdown("""
<style>
    /* Force l'affichage permanent sans fondu au noir */
    div[data-testid="stAppViewBlockContainer"] { opacity: 1 !important; }
    [data-testid="stVerticalBlock"] > div { animation: none !important; }
    [data-testid="stElementContainer"] { opacity: 1 !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #050505 !important; 
        color: #d1d1d6; 
        font-family: 'Inter', sans-serif; 
    }

    .kz-panel { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 18px; margin-bottom: 15px; }
    .kz-header { font-size: 10px; font-weight: 800; color: #555; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 15px; display: flex; align-items: center; }
    .kz-header::before { content: ''; width: 3px; height: 12px; background: #eab308; margin-right: 10px; }
    
    .kz-topbar { display: flex; justify-content: space-between; align-items: center; background: #0d0d0d; padding: 12px 25px; border-bottom: 2px solid #eab308; margin-bottom: 20px; }
    
    /* DOM MATRIX PRO */
    .dom-container { background: #080808; border: 1px solid #1a1a1a; border-radius: 4px; height: 460px; overflow: hidden; }
    .dom-row { display: flex; height: 19px; align-items: center; font-family: 'JetBrains Mono', monospace; border-bottom: 1px solid #111; }
    .dom-price { width: 65px; color: #444; font-size: 10px; text-align: right; padding-right: 12px; }
    .dom-price.active { color: #eab308; font-weight: 900; background: rgba(234, 179, 8, 0.1); }
    .dom-bar-wrapper { flex-grow: 1; height: 100%; position: relative; display: flex; align-items: center; }
    .bid-bar { background: linear-gradient(90deg, rgba(16, 185, 129, 0.05) 0%, rgba(16, 185, 129, 0.4) 100%); border-right: 2px solid #10b981; position: absolute; left: 0; height: 100%; }
    .ask-bar { background: linear-gradient(90deg, rgba(239, 68, 68, 0.05) 0%, rgba(239, 68, 68, 0.4) 100%); border-right: 2px solid #ef4444; position: absolute; left: 0; height: 100%; }
    .dom-vol { position: absolute; right: 10px; color: #fff; font-size: 9px; font-weight: 700; z-index: 10; }

    /* ROADMAP STYLING PRO */
    .roadmap-section { margin-top: 25px; padding-top: 10px; }
    .roadmap-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }
    .roadmap-card { 
        background: linear-gradient(145deg, #111111, #0a0a0a); 
        border: 1px solid #222; 
        padding: 15px; 
        border-radius: 6px; 
        display: flex; 
        flex-direction: column;
        gap: 8px;
        position: relative;
        overflow: hidden;
    }
    .roadmap-label { font-size: 9px; font-weight: 800; color: #555; text-transform: uppercase; letter-spacing: 1px; }
    .roadmap-status { font-size: 11px; font-weight: 900; display: flex; align-items: center; gap: 8px; }
    .status-dot { width: 8px; height: 8px; border-radius: 50%; }
    
    .ok-text { color: #10b981; }
    .ok-dot { background: #10b981; box-shadow: 0 0 10px #10b981; }
    .wait-text { color: #ef4444; }
    .wait-dot { background: #ef4444; box-shadow: 0 0 10px #ef4444; }
</style>
""", unsafe_allow_html=True)

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/
