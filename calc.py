import streamlit as st
import math

st.title("⚙️ Kalkulator Parametrów Skrawania")

# Wybór systemu jednostek
system = st.radio("Wybierz system jednostek:", ["Metryczne", "Imperialne"], horizontal=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Dane wejściowe")
    d = st.number_input("Średnica (d) [mm/cale]", min_value=0.1, value=20.0)
    vc = st.number_input("Prędkość skrawania (vc)", min_value=1.0, value=150.0)
    fn = st.number_input("Posuw na obrót (fn)", min_value=0.01, value=0.2)
    ap = st.number_input("Głębokość skrawania (ap)", min_value=0.1, value=2.0)
    L = st.number_input("Długość skrawania (L) [mm/cale]", min_value=1.0, value=100.0)

# LOGIKA OBLICZEŃ
if system == "Metryczne":
    # n = (vc * 1000) / (pi * d)
    n = (vc * 1000) / (math.pi * d)
    # vf = n * fn
    vf = n * fn
    # Tc = L / vf
    tc = L / vf if vf > 0 else 0
    # Q = vc * ap * fn (uproszczone dla cm3/min)
    q = (vc * ap * fn) 
else:
    # System Imperialny
    # n = (vc * 12) / (pi * d)
    n = (vc * 12) / (math.pi * d)
    vf = n * fn
    tc = L / vf if vf > 0 else 0
    q = (vc * 12 * ap * fn) # cale3/min

with col2:
    st.subheader("Wyniki")
    st.metric("Prędkość obrotowa (n)", f"{int(n)} obr./min")
    st.metric("Prędkość posuwu (vf)", f"{round(vf, 2)} mm/min" if system == "Metryczne" else f"{round(vf, 2)} cal/min")
    st.metric("Czas maszynowy (Tc)", f"{round(tc, 2)} min")
    
    unit_q = "cm³/min" if system == "Metryczne" else "in³/min"
    st.metric("Wydajność (Q)", f"{round(q, 2)} {unit_q}")

st.markdown("---")

# Sekcja Mocy i Momentu (Wymaga siły skrawania lub materiału)
st.subheader("⚡ Moc i Moment obrotowy")
kc = st.number_input("Opór właściwy materiału (kc) [N/mm2]", value=2000) # np. dla stali

# Pc = (ap * f * vc * kc) / (60 * 10^3)
pc = (ap * fn * vc * kc) / 60000
# Mc = (Pc * 9550) / n
mc = (pc * 9550) / n if n > 0 else 0

c1, c2 = st.columns(2)
c1.metric("Moc netto (Pc)", f"{round(pc, 2)} kW")
c2.metric("Moment obrotowy (Mc)", f"{round(mc, 2)} Nm")