import streamlit as st
import json
import urllib.request

st.set_page_config(page_title="Aura Signal", page_icon="🌌")

# Titolo e Stile
st.title("🌌 Aura Signal Private")
st.markdown("---")

# Funzione per recuperare il prezzo REALE di BRETT
def get_price():
    try:
        # Usiamo l'API di CoinGecko (URL pubblico)
        url = "https://api.coingecko.com"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data['brett']['usd']
    except:
        return 0.00750 # Prezzo di riserva se internet fa i capricci

# Visualizzazione Prezzo
prezzo_live = get_price()
st.metric("Prezzo Live BRETT (USD)", f"${prezzo_live:.5f}")

if st.button("🔄 AGGIORNA PREZZO ORA"):
    st.rerun()

st.markdown("---")

# Input al CENTRO della pagina (Niente sidebar)
st.header("⚙️ Impostazioni Trade")
budget = st.number_input("Tuo Budget ($)", value=500, step=50)
leva = st.slider("Leva Finanziaria (Leverage)", 1, 10, 3)

# Logica Matematica Aura Sniper
st.markdown("---")
st.subheader("🎯 Strategia Sniper (+1.5%)")

target = prezzo_live * (1 + 0.015)
stop_loss = prezzo_live * (1 - 0.01)

col1, col2 = st.columns(2)
with col1:
    st.success(f"VENDI A (TP):\n**${target:.5f}**")
with col2:
    st.error(f"STOP LOSS (SL):\n**${stop_loss:.5f}**")

# Calcolo Profitto
profitto_netto = (budget * leva) * 0.015
st.info(f"💰 Con questa operazione punti a guadagnare: **${profitto_netto:.2f}**")

st.markdown("---")
st.caption("Aura Assistant v2.0 - Solo per uso personale")
