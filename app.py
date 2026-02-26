import streamlit as st
import json
import urllib.request

st.set_page_config(page_title="Aura Signal Advisor", page_icon="🔮")

st.title("🔮 Aura Signal Advisor")
st.markdown("---")

def get_price():
    # USIAMO UN AGGREGATORE DIVERSO (DEXSCREENER CON LINK DIRETTO)
    # Questo è quasi impossibile da bloccare per il server
    url = "https://api.dexscreener.com"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            # Cerchiamo il prezzo nella prima coppia disponibile (solitamente BRETT/WETH)
            if data and 'pairs' in data and len(data['pairs']) > 0:
                return float(data['pairs'][0]['priceUsd'])
            else:
                return 0.007421 # Valore di test realistico
    except Exception as e:
        # Se fallisce ancora, proviamo un secondo ponte (CoinGecko Simple)
        try:
            url_cg = "https://api.coingecko.com"
            with urllib.request.urlopen(url_cg, timeout=10) as res_cg:
                data_cg = json.loads(res_cg.read().decode())
                return float(data_cg['based-brett']['usd'])
        except:
            return 0.007422 # Secondo valore di test

prezzo_live = get_price()

# --- CONTROLLO VISIVO ---
if prezzo_live == 0.007421 or prezzo_live == 0.007422:
    st.warning("⚠️ L'AURA È IN MODALITÀ MANUALE (Connessione lenta)")
    st.write("Inserisci il prezzo che vedi su LBank qui sotto per calcolare i livelli:")
    prezzo_live = st.number_input("Prezzo BRETT attuale", value=prezzo_live, format="%.6f")
else:
    st.metric("PREZZO REALE BRETT (BASE)", f"${prezzo_live:.6f}")
    if st.button("🔄 AGGIORNA AURA E PREZZO"):
        st.rerun()

st.markdown("---")

# --- SEZIONE AURA ADVISOR ---
st.subheader("🕵️ Stato dell'Aura")
if prezzo_live < 0.00730:
    st.success("🟢 AURA POTENTE: PREZZO IN SCONTO!")
elif prezzo_live > 0.00760:
    st.error("🔴 AURA SURRISCALDATA: ASPETTA!")
else:
    st.warning("🟡 AURA NEUTRA: FASE DI ATTESA")

st.markdown("---")

# --- CALCOLATORE ---
budget = st.number_input("Tuo Budget ($)", value=500, step=50)
leva = st.slider("Leva (Leverage)", 1, 10, 3)

target = prezzo_live * (1 + 0.015)
sl = prezzo_live * (1 - 0.01)

st.subheader("🎯 Livelli Sniper (+1.5%)")
c1, c2 = st.columns(2)
with c1:
    st.success(f"TAKE PROFIT:\n**${target:.6f}**")
with c2:
    st.error(f"STOP LOSS:\n**${sl:.6f}**")

st.info(f"💰 Profitto potenziale: **+${(budget * leva) * 0.015:.2f}**")
