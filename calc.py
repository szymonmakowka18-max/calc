import streamlit as st
import math

# 1. Konfiguracja strony
st.set_page_config(
    page_title="Kalkulator Inżynierski CNC",
    layout="wide",
    page_icon="🔧",
    initial_sidebar_state="expanded"
)

# 2. Stylizacja (Poprawa czytelności - czarna, gruba czcionka)
st.markdown("""
    <style>
    /* Stylizacja wartości metryk */
    [data-testid="stMetricValue"] {
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
    }
    /* Stylizacja etykiet metryk */
    [data-testid="stMetricLabel"] {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    /* Stylizacja kontenera metryki */
    [data-testid="stMetric"] {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #dee2e6;
    }
    /* Stylizacja zakładek */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stWidgetLabel"] {
        font-size: 1.2rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚙️ Zaawansowany Kalkulator Skrawania")

# 3. Panel boczny - Ustawienia globalne
st.sidebar.header("🔧 Ustawienia Systemowe")
system = st.sidebar.radio("Wybierz system:", ["Metryczny (mm, m/min)", "Imperialny (cale, ft/min)"])
is_metric = system == "Metryczny (mm, m/min)"
eta = st.sidebar.slider("Sprawność maszyny (η)", 0.1, 1.0, 0.8)

# Definicja jednostek
u_dist = "mm" if is_metric else "cale"
u_speed = "m/min" if is_metric else "ft/min"
u_feed_rev = "mm/obr" if is_metric else "cal/obr"
u_feed_min = "mm/min" if is_metric else "in/min"
u_pwr = "kW" if is_metric else "KM"
u_vol = "cm³/min" if is_metric else "in³/min"
u_torque = "Nm" if is_metric else "lbf ft"

# 4. Zakładki dla operacji
tab_turn, tab_mill, tab_bore = st.tabs(["🌀 TOCZENIE", "🌽 FREZOWANIE", "🕳️ WYTACZANIE"])

# --- TOCZENIE ---
with tab_turn:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.subheader("Dane wejściowe")
        dm = st.number_input(f"Średnica przedmiotu Dm [{u_dist}]", value=50.0, key="t_dm")
        vc = st.number_input(f"Prędkość skrawania vc [{u_speed}]", value=180.0, key="t_vc")
        fn = st.number_input(f"Posuw na obrót fn [{u_feed_rev}]", value=0.25, format="%.3f", key="t_fn")
        ap = st.number_input(f"Głębokość osiowa ap [{u_dist}]", value=2.0, key="t_ap")
        kc = st.number_input(f"Opór właściwy kc [N/mm²]", value=2100, key="t_kc")
        kapr = st.slider("Kąt przystawienia KAPR°", 0, 180, 45, key="t_kapr")

    with c2:
        st.subheader("Wyniki Obliczeń")
        mult = 1000 if is_metric else 12
        n = (vc * mult) / (math.pi * dm) if dm > 0 else 0
        vf = n * fn
        pc = (ap * fn * vc * kc) / (60000 * eta) if is_metric else (ap * fn * vc * kc) / (33000 * eta)
        q = (vc * ap * fn) if is_metric else (vc * 12 * ap * fn)
        hex_val = fn * math.sin(math.radians(kapr)) if kapr > 0 else fn
        
        res1, res2 = st.columns(2)
        res1.metric("Obroty n", f"{int(n)} obr/min")
        res1.metric("Posuw vf", f"{round(vf, 1)} {u_feed_min}")
        res1.metric("Moc netto Pc", f"{round(pc, 2)} {u_pwr}")
        
        res2.metric("Wydajność Q", f"{round(q, 1)} {u_vol}")
        res2.metric("Grubość wióra hex", f"{round(hex_val, 3)} {u_dist}")
        res2.metric("Moment M", f"{round((pc*9550/n if n>0 else 0), 1)} {u_torque}")

# --- FREZOWANIE ---
with tab_mill:
    m1, m2 = st.columns([1, 1.2])
    with m1:
        st.subheader("Geometria Freza")
        dc = st.number_input(f"Średnica skrawania DC [{u_dist}]", value=16.0, key="m_dc")
        zc = st.number_input("Liczba efektywnych ostrzy zc", value=3, min_value=1)
        fz = st.number_input(f"Posuw na ostrze fz [{u_dist}]", value=0.08, format="%.3f")
        ae = st.number_input(f"Szerokość skrawania ae [{u_dist}]", value=8.0)
        ap_m = st.number_input(f"Głębokość osiowa ap [{u_dist}]", value=4.0, key="m_ap")
        vc_m = st.number_input(f"Prędkość vc [{u_speed}]", value=220.0, key="m_vc")
        kc_m = st.number_input("Opór właściwy kc [N/mm²]", value=1800, key="m_kc")

    with m2:
        st.subheader("Wyniki Obliczeń")
        n_m = (vc_m * mult) / (math.pi * dc) if dc > 0 else 0
        vf_m = n_m * fz * zc
        fn_m = fz * zc
        q_m = (ap_m * ae * vf_m) / 1000 if is_metric else (ap_m * ae * vf_m)
        pc_m = (q_m * kc_m) / (60 * 1000 * eta) if is_metric else (q_m * kc_m) / 33000
        hm = fz * math.sqrt(ae/dc) if dc > 0 else 0
        
        rm1, rm2 = st.columns(2)
        rm1.metric("Obroty n", f"{int(n_m)} obr/min")
        rm1.metric("Posuw stołu vf", f"{round(vf_m, 1)} {u_feed_min}")
        rm1.metric("Moc netto Pc", f"{round(pc_m, 2)} {u_pwr}")
        
        rm2.metric("Posuw na obrót fn", f"{round(fn_m, 2)} {u_feed_rev}")
        rm2.metric("Średnia grubość hm", f"{round(hm, 3)} {u_dist}")
        rm2.metric("Wydajność Q", f"{round(q_m, 1)} {u_vol}")

# --- WYTACZANIE ---
with tab_bore:
    st.info("Parametry Wytaczania / Boring")
    w1, w2 = st.columns(2)
    with w1:
        bd = st.number_input(f"Średnica korpusu BD [{u_dist}]", value=20.0)
        lu = st.number_input(f"Długość użytkowa LU [{u_dist}]", value=60.0)
        dcap = st.number_input(f"Średnica rzeczywista DCap [{u_dist}]", value=25.0)
    with w2:
        ratio = lu/dcap if dcap > 0 else 0
        st.metric("Stosunek wysięgu L/D", f"{round(ratio, 1)}")
        if ratio > 4:
            st.warning("Uwaga: Wysoki stosunek L/D. Ryzyko drgań! Rozważ trzonek węglikowy.")
        else:
            st.success("Stosunek L/D w normie dla trzonków stalowych.")

st.markdown("---")
st.caption("Kalkulator Parametrów Skrawania v1.0 | 2026")
