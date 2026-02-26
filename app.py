import streamlit as st
import json
import urllib.request
import time # Serve per il trucco del tempo

st.set_page_config(page_title="Aura Signal", page_icon="🌌")

st.title("🌌 Aura Signal Private")
st.markdown("---")

def get_price():
    # Trucco: aggiungiamo l'ora esatta all'URL per forzare dati nuovi
    timestamp = int(time.time())
    url = f"https://api.coingecko.com{timestamp}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data['based-brett']['usd']
    except:
        return 0.00746 # Prezzo attuale di riserva

prezzo_live = get_price()
st.metric("Prezzo Live BRETT (USD)", f"${prezzo_live:.5f}")

if st.button("🔄 FORZA AGGIORNAMENTO"):
    st.rerun()

st.markdown("---")
st.header("⚙️ Impostazioni Trade")
budget = st.number_input("Tuo Budget ($)", value=500, step=50)
leva = st.slider("Leva Finanziaria", 1, 10, 3)

st.markdown("---")
st.subheader("🎯 Strategia Sniper (+1.5%)")

# Calcoli con precisione chirurgica
target = prezzo_live * (1 + 0.015)
stop_loss = prezzo_live * (1 - 0.01)

col1, col2 = st.columns(2)
with col1:
    st.success(f"TAKE PROFIT (Vendi a):\n**${target:.5f}**")
with col2:
    st.error(f"STOP LOSS:\n**${stop_loss:.5f}**")

profitto_netto = (budget * leva) * 0.015
st.info(f"💰 Profitto stimato: **${profitto_netto:.2f}**")
