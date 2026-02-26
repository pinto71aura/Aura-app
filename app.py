import streamlit as st
import json
import urllib.request

st.set_page_config(page_title="Aura Signal Pro", page_icon="🔮")

st.title("🔮 Aura Signal Advisor")
st.markdown("---")

def get_price():
    # Usiamo l'API di Binance (La più stabile al mondo)
    # Nota: BRETT è scambiato come BRETTUSDT su molti exchange
    url = "https://api.binance.com"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return float(data['price'])
    except:
        try:
            # Backup su MEXC se Binance fallisce
            url_mexc = "https://api.mexc.com"
            req_mexc = urllib.request.Request(url_mexc, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_mexc, timeout=5) as response:
                data_m = json.loads(response.read().decode())
                return float(data_m['price'])
        except:
            # Se entrambi falliscono, usiamo un numero leggermente diverso 
            # per capire se il blocco persiste: 0.00741
            return 0.00741

prezzo_live = get_price()

# --- VISUALIZZAZIONE ---
if prezzo_live == 0.00741:
    st.error("⚠️ ERRORE CONNESSIONE: Il server è temporaneamente bloccato.")
    st.write("Prova a cliccare il tasto AGGIORNA tra 10 secondi.")
else:
    st.metric("PREZZO ATTUALE BRETT (USDT)", f"${prezzo_live:.6f}")

if st.button("🔄 AGGIORNA AURA E PREZZO"):
    st.rerun()

st.markdown("---")

# --- SEZIONE AURA ADVISOR ---
st.subheader("🕵️ Stato dell'Aura")

if prezzo_live < 0.00730:
    st.success("🟢 AURA POTENTE: PREZZO IN SCONTO!")
    st.write("**CONSIGLIO:** Ottimo momento per l'entrata Sniper.")
elif prezzo_live > 0.00760:
    st.error("🔴 AURA SURRISCALDATA: ASPETTA!")
    st.write("**CONSIGLIO:** Rischio rintracciamento. Non inseguire.")
else:
    st.warning("🟡 AURA NEUTRA: FASE DI ATTESA")
    st.write("**CONSIGLIO:** Mercato in equilibrio. Attendi forza.")

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
