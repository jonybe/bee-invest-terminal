import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import random
import math

# 1. Configuration & Design System (V2.2 - FULL ZONES & ROADMAP)
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
    .block-container { padding-top: 1.5rem !important; padding-bottom: 0rem !important; max-width: 1600px; }
    
    .kz-panel { background: #111111; border: 1px solid #222222; border-radius: 6px; padding: 16px; margin-bottom: 16px; }
    .kz-header { font-size: 10px; font-weight: 800; color: #a1a1aa; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 16px; display: flex; align-items: center; }
    .kz-header::before { content: '●'; color: #eab308; margin-right: 8px; font-size: 12px; }
    .kz-topbar { display: flex; justify-content: space-between; align-items: center; background: #111; padding: 12px 24px; border-bottom: 1px solid #222; border-radius: 6px; margin-bottom: 20px; }
    .kz-topbar-item { display: flex; flex-direction: column; }
    .kz-label { font-size: 8px; color: #71717a; text-transform: uppercase; font-weight: bold; margin-bottom: 2px; }
    .kz-val { font-size: 14px; color: #e4e4e7; font-weight: bold; font-family: 'JetBrains Mono', monospace; }
    
    .flow-bar-wrapper { display: flex; height: 12px; border-radius: 2px; overflow: hidden; background: #ef4444; }
    .flow-bar-green { height: 100%; background: #10b981; transition: width 0.5s ease-in-out; }
    .badge-center { text-align: center; background: #18181b; border: 1px solid #27272a; padding: 4px 16px; border-radius: 4px; display: inline-block; transform: translateY(-10px); }
    
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

    .roadmap-item { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 12px; padding: 8px; background: #0
