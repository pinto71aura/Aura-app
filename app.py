import streamlit as st
import json
import urllib.request

st.set_page_config(page_title="Aura Signal Advisor", page_icon="🔮")

st.title("🔮 Aura Signal Advisor")
st.markdown("---")

def get_price():
    # Binance/MEXC Bridge
    url = "https://api.binance.com"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return float(data['price'])
    except:
        return 0.00744 # Prezzo di riserva aggiornato 26 Feb

prezzo_live = get_price()

# --- PREZZO LIVE (Tornato al suo posto!) ---
st.metric("PREZZO ATTUALE BRETT (USDT)", f"${prezzo_live:.6f}")

if st.button("🔄 AGGIORNA AURA E PREZZO"):
    st.rerun()

st.markdown("---")

# --- SEZIONE AURA ADVISOR ---
st.subheader("🕵️ Stato dell'Aura")

if prezzo_live < 0.00735:
    st.success("🟢 AURA POTENTE: PREZZO IN SCONTO!")
    st.write("**CONSIGLIO:** Ottimo momento per l'entrata Sniper. Controlla che BTC sia stabile.")
elif prezzo_live > 0.00765:
    st.error("🔴 AURA SURRISCALDATA: NON INSEGUIRE!")
    st.write("**CONSIGLIO:** Il prezzo è alto. Aspetta un rintracciamento (dip) per non restare incastrato.")
else:
    st.warning("🟡 AURA IN ATTESA: MERCATO LATERALE")
    st.write("**CONSIGLIO:** Il prezzo è in equilibrio. Entra solo se vedi una candela verde decisa.")

st.markdown("---")

# --- SEZIONE CALCOLATORE ---
budget = st.number_input("Tuo Budget ($)", value=500, step=50)
leva = st.slider("Leva Finanziaria (Leverage)", 1, 10, 3)

target = prezzo_live * (1 + 0.015)
sl = prezzo_live * (1 - 0.01)

st.subheader("🎯 Livelli Sniper (+1.5%)")
c1, c2 = st.columns(2)
with c1:
    st.success(f"TAKE PROFIT:\n**${target:.6f}**")
with c2:
    st.error(f"STOP LOSS:\n**${sl:.6f}**")

profitto = (budget * leva) * 0.015
st.info(f"💰 Se l'Aura colpisce il target: **+${profitto:.2f}**")

st.markdown("---")
st.caption("Aura Advisor v5.1 - Prezzo + Consigli Attivi")
