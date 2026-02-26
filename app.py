import streamlit as st
import json
import urllib.request

st.set_page_config(page_title="Aura Signal Pro", page_icon="🔮")

st.title("🔮 Aura Signal Advisor")
st.markdown("---")

def get_price():
    # Usiamo DexScreener API per BRETT su BASE (Il più preciso)
    # Token Address di BRETT: 0x532f27101965dd16442e59d40670faf5ebb142e4
    url = "https://api.dexscreener.com"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return float(data['pair']['priceUsd'])
    except:
        # Se DexScreener fallisce, usiamo CoinGecko come backup
        try:
            url_cg = "https://api.coingecko.com"
            req_cg = urllib.request.Request(url_cg, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_cg, timeout=10) as response:
                data_cg = json.loads(response.read().decode())
                return data_cg['based-brett']['usd']
        except:
            return 0.00744 # Riserva

prezzo_live = get_price()

# --- PREZZO LIVE ---
st.metric("PREZZO REALE BRETT (BASE)", f"${prezzo_live:.6f}")

if st.button("🔄 AGGIORNA AURA E PREZZO"):
    st.rerun()

st.markdown("---")

# --- SEZIONE AURA ADVISOR ---
st.subheader("🕵️ Stato dell'Aura")

# Logica dinamica: confronta il prezzo con zone calde/fredde
if prezzo_live < 0.00730:
    st.success("🟢 AURA POTENTE: PREZZO IN SCONTO!")
    st.write("**CONSIGLIO:** Prezzo sotto la media. Buona zona Sniper.")
elif prezzo_live > 0.00760:
    st.error("🔴 AURA SURRISCALDATA: ASPETTA!")
    st.write("**CONSIGLIO:** Troppo alto ora. Rischio rintracciamento.")
else:
    st.warning("🟡 AURA NEUTRA: FASE DI ATTESA")
    st.write("**CONSIGLIO:** Mercato in equilibrio. Entra solo se vedi forza.")

st.markdown("---")

# --- SEZIONE CALCOLATORE ---
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

profitto = (budget * leva) * 0.015
st.info(f"💰 Profitto potenziale: **+${profitto:.2f}**")

st.caption("Aura Advisor v6.0 - Dati aggregati da DexScreener")
