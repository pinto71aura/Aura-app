import streamlit as st
import requests

st.set_page_config(page_title="Aura Signal", page_icon="🌌")
st.title("🌌 Aura Signal Private")

# Funzione per recuperare il prezzo VERO di BRETT
def get_price():
    try:
        url = "https://api.coingecko.com"
        response = requests.get(url).json()
        return response['brett']['usd']
    except:
        return 0.00750 # Prezzo di emergenza se l'API non risponde

prezzo_live = get_price()
st.metric("Prezzo Live BRETT (USD)", f"${prezzo_live:.5f}")

# I tuoi parametri
st.sidebar.header("Impostazioni Trade")
budget = st.sidebar.number_input("Tuo Budget ($)", value=500)
leva = st.sidebar.slider("Leva Finanziaria", 1, 10, 3)

# Logica Aura Sniper
st.subheader("🎯 Strategia Sniper")
target = prezzo_live * (1 + 0.015)
stop_loss = prezzo_live * (1 - 0.01)

col1, col2 = st.columns(2)
col1.success(f"VENDI A (TP): \n**${target:.5f}**")
col2.error(f"STOP LOSS (SL): \n**${stop_loss:.5f}**")

profitto = (budget * leva) * 0.015
st.info(f"💰 Se colpisce il target guadagni: **${profitto:.2f}**")

if st.button("Aggiorna Prezzo 🔄"):
    st.rerun()
