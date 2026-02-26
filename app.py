import streamlit as st
import json
import urllib.request
import pandas as pd

st.set_page_config(page_title="Aura AI Advisor", page_icon="🔮")
st.title("🔮 Aura Intelligence Advisor")

def get_data_and_rsi():
    # Peschiamo le ultime 100 candele da 15 minuti da Binance
    url = "https://api.binance.com"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'vol', 'close_time', 'q_vol', 'trades', 'buy_base', 'buy_quote', 'ignore'])
            df['close'] = df['close'].astype(float)
            
            # Calcolo RSI Matematico
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            return df['close'].iloc[-1], rsi.iloc[-1], df['vol'].iloc[-1]
    except:
        return None, None, None

price, rsi, vol = get_data_and_rsi()

if price and rsi:
    st.metric("PREZZO BRETT", f"${price:.6f}")
    st.metric("FORZA MERCATO (RSI)", f"{rsi:.2f}")

    st.markdown("---")
    st.subheader("🕵️ Verdetto dell'Aura")
    
    if rsi < 35:
        st.success("🟢 AURA POTENTE (OVERSOLD): Il mercato è scarico. MOMENTO OTTIMO PER ENTRARE.")
    elif rsi > 65:
        st.error("🔴 AURA SURRISCALDATA (OVERBOUGHT): Troppa euforia. ASPETTA IL CROLLO.")
    else:
        st.warning("🟡 AURA NEUTRA: Il trend è incerto. Entra solo se hai fegato.")
    
    if st.button("🔄 AGGIORNA ANALISI"):
        st.rerun()
else:
    st.error("⚠️ Connessione ai dati di mercato fallita. Riprova tra poco.")
    price = 0.00745 # Riserva

# --- CALCOLATORE SNIPER ---
st.markdown("---")
budget = st.number_input("Tuo Budget ($)", value=500)
leva = st.slider("Leva (Leverage)", 1, 10, 3)

target = price * (1 + 0.015)
sl = price * (1 - 0.01)

st.subheader("🎯 Target Sniper")
c1, c2 = st.columns(2)
c1.metric("TAKE PROFIT", f"${target:.6f}")
c2.metric("STOP LOSS", f"${sl:.6f}")
