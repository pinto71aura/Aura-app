import streamlit as st
import json
import urllib.request

st.set_page_config(page_title="Aura Signal", page_icon="🌌")

st.title("🌌 Aura Signal Private")
st.markdown("---")

# FUNZIONE BLINDATA PER IL PREZZO
def get_price():
    # Proviamo l'identificativo corretto di CoinGecko per BRETT su BASE
    url = "https://api.coingecko.com"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            # Se il dato esiste, lo restituisce
            if 'brett-2' in data:
                return data['brett-2']['usd']
            else:
                st.warning("Dato non trovato nel database. Uso valore test.")
                return 0.00751 # Valore test diverso per capire se è cambiato
    except Exception as e:
        st.error(f"Errore di connessione: {e}")
        return 0.00752 # Valore test diverso

prezzo_live = get_price()

# Se vedi 0.00751 o 0.00752, sapremo esattamente dove sta il problema!
st.metric("Prezzo Live BRETT (USD)", f"${prezzo_live:.5f}")

if st.button("🔄 FORZA AGGIORNAMENTO"):
    st.rerun()

st.markdown("---")
st.header("⚙️ Impostazioni Trade")
budget = st.number_input("Tuo Budget ($)", value=500, step=50)
leva = st.slider("Leva Finanziaria", 1, 10, 3)

st.markdown("---")
st.subheader("🎯 Strategia Sniper (+1.5%)")

target = prezzo_live * (1 + 0.015)
stop_loss = prezzo_live * (1 - 0.01)

col1, col2 = st.columns(2)
with col1:
    st.success(f"VENDI A:\n**${target:.5f}**")
with col2:
    st.error(f"STOP LOSS:\n**${stop_loss:.5f}**")

profitto_netto = (budget * leva) * 0.015
st.info(f"💰 Profitto stimato: **${profitto_netto:.2f}**")
