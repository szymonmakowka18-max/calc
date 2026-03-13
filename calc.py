import streamlit as st
import math

# Ustawienia strony
st.set_page_config(page_title="Inżynier Skrawania", layout="wide", page_icon="🔧")

# Stylizacja dla lepszej czytelności na telefonie
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 10px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🔧 Kalkulator Parametrów Obróbki")

# Panel boczny - Ustawienia globalne
st.sidebar.header("⚙️ Ustawienia Główne")
system = st.sidebar.radio("System jednostek:", ["Metryczny", "Imperialny"])
is_metric = system == "Metryczny"
eta = st.sidebar.slider("Sprawność maszyny (η)", 0.1, 1.0, 0.8)

# Zakładki dla różnych operacji
tab_turn, tab_mill, tab_bore = st.tabs(["🌀 Toczenie", "🌽 Frezowanie", "🕳️ Wytaczanie"])

# --- FUNKCJE POMOCNICZE ---
def format_unit(val, unit_m, unit_i):
    return f"{val:.2f} {unit_m if is_metric else unit_i}"

# --- TOCZENIE ---
with tab_turn:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Dane wejściowe")
        dm = st.number_input("Średnica przedmiotu Dm [mm/cal]", value=50.0, key="turn_dm")
        vc = st.number_input("Prędkość skrawania vc [m/min / ft/min]", value=150.0, key="turn_vc")
        fn = st.number_input("Posuw na obrót fn [mm/obr / cal/obr]", value=0.2, format="%.3f")
        ap = st.number_input("Głębokość skrawania ap [mm/cal]", value=2.0, key="turn_ap")
        kc = st.number_input("Opór właściwy kc [N/mm2]", value=2000, key="turn_kc")
        kapr = st.slider("Kąt przystawienia KAPR°", 0, 180, 45, key="turn_kapr")

    with c2:
        st.subheader("Wyniki")
        mult = 1000 if is_metric else 12
        n = (vc * mult) / (math.pi * dm) if dm > 0 else 0
        vf = n * fn
        pc = (ap * fn * vc * kc) / (60000 * eta) if is_metric else (ap * fn * vc * kc) / (33000 * eta)
        q = vc * ap * fn if is_metric else vc * 12 * ap * fn
        
        st.metric("Prędkość obrotowa n", f"{int(n)} obr/min")
        st.metric("Posuw stołu vf", format_unit(vf, "mm/min", "in/min"))
        st.metric("Moc netto Pc", format_unit(pc, "kW", "KM"))
        st.metric("Wydajność Q", format_unit(q, "cm³/min", "in³/min"))

# --- FREZOWANIE ---
with tab_mill:
    m1, m2 = st.columns(2)
    with m1:
        st.subheader("Geometria narzędzia")
        dc = st.number_input("Średnica skrawania DC [mm/cal]", value=20.0)
        zc = st.number_input("Liczba ostrzy zc", value=4, min_value=1)
        fz = st.number_input("Posuw na ostrze fz [mm / cal]", value=0.1, format="%.3f")
        ae = st.number_input("Szerokość skrawania ae [mm/cal]", value=10.0)
        ap_m = st.number_input("Głębokość osiowa ap [mm/cal]", value=3.0, key="mill_ap")
        vc_m = st.number_input("Prędkość skrawania vc [m/min]", value=200.0, key="mill_vc")
        kc_m = st.number_input("Opór właściwy kc [N/mm2]", value=1800, key="mill_kc")

    with m2:
        st.subheader("Wyniki")
        n_m = (vc_m * mult) / (math.pi * dc) if dc > 0 else 0
        fn_m = fz * zc
        vf_m = n_m * fn_m
        q_m = (ap_m * ae * vf_m) / 1000 if is_metric else (ap_m * ae * vf_m)
        pc_m = (q_m * kc_m) / (60 * 1000 * eta) if is_metric else (q_m * kc_m) / 33000
        
        # Średnia grubość wióra hm (uproszczona dla ae/dc)
        hm = fz * math.sqrt(ae/dc) if dc > 0 else 0
        
        st.metric("Prędkość obrotowa n", f"{int(n_m)} obr/min")
        st.metric("Posuw na obrót fn", format_unit(fn_m, "mm/obr", "in/obr"))
        st.metric("Posuw stołu vf", format_unit(vf_m, "mm/min", "in/min"))
        st.metric("Moc netto Pc", format_unit(pc_m, "kW", "KM"))
        st.metric("Średnia grubość wióra hm", format_unit(hm, "mm", "cal"))

# --- WYTACZANIE ---
with tab_bore:
    st.info("Parametry dla wytaczania (Boring)")
    w1, w2 = st.columns(2)
    with w1:
        dcap = st.number_input("Średnica rzeczywista DCap [mm/cal]", value=25.0)
        lu = st.number_input("Długość użytkowa LU [mm/cal]", value=50.0)
        bd = st.number_input("Średnica korpusu BD [mm/cal]", value=20.0)
    with w2:
        st.write("Wytaczanie wykorzystuje podobną logikę co toczenie wewnętrzne.")
        # Tutaj można dodać specyficzne obliczenia drgań lub ugięć dla LU/BD
        st.metric("Stosunek wysięgu (L/D)", f"{round(lu/dcap, 1) if dcap > 0 else 0}")

st.markdown("---")
st.caption("Opracowano na podstawie standardów ISO dla narzędzi skrawających.")
