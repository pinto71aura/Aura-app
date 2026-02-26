import streamlit as st
import json
import urllib.request
import time

st.set_page_config(page_title="Aura Signal", page_icon="🌌")

st.title("🌌 Aura Signal Private")
st.markdown("---")

def get_price():
    # Nuovo Fornitore: Crypto.com API (Molto più veloce)
    url = "https://api.crypto.com"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            # Estraiamo il prezzo dell'ultima vendita (last_price)
            return float(data['result']['data'][0]['a']) 
    except:
        # Se fallisce, usiamo un valore diverso per capire: 0.00744
        return 0.00744

prezzo_live = get_price()

# Se vedi 0.00744, la connessione è ancora bloccata. 
# Se vedi un numero diverso (es. 0.0074782), l'app è FINALMENTE connessa!
st.metric("Prezzo Live BRETT (USD)", f"${prezzo_live:.5f}")

if st.button("🔄 AGGIORNA ORA"):
    st.rerun()

st.markdown("---")
st.header("⚙️ Impostazioni Trade")
budget = st.number_input("Tuo Budget ($)", value=500, step=50)
leva = st.slider("Leva Finanziaria", 1, 10, 3)

st.markdown("---")
st.subheader("🎯 Strategia Sniper (+1.5%)")

target = prezzo_live * (1 + 0.015)
sl = prezzo_live * (1 - 0.01)

c1, c2 = st.columns(2)
with c1:
    st.success(f"TAKE PROFIT (Vendi):\n**${target:.5f}**")
with c2:
    st.error(f"STOP LOSS:\n**${sl:.5f}**")

profitto = (budget * leva) * 0.015
st.info(f"💰 Profitto stimato: **${profitto:.2f}**")
