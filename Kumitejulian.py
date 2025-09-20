import streamlit as st
import time
from streamlit_hotkeys import st_hotkeys

# --- Configuración Inicial de la Página ---
st.set_page_config(page_title="Karate Kumite Scoreboard", layout="wide")

# --- Funciones de Ayuda ---

def initialize_state():
    """Inicializa el estado de la sesión si no existe."""
    if 'aka_score' not in st.session_state:
        st.session_state.aka_score = 0
    if 'ao_score' not in st.session_state:
        st.session_state.ao_score = 0
    if 'aka_cat1' not in st.session_state:
        st.session_state.aka_cat1 = 0
    if 'ao_cat1' not in st.session_state:
        st.session_state.ao_cat1 = 0
    if 'aka_cat2' not in st.session_state:
        st.session_state.aka_cat2 = 0
    if 'ao_cat2' not in st.session_state:
        st.session_state.ao_cat2 = 0
    if 'senshu' not in st.session_state:
        st.session_state.senshu = None  # Puede ser 'AKA' o 'AO'
    if 'timer' not in st.session_state:
        st.session_state.timer = 180  # 3 minutos por defecto
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'winner' not in st.session_state:
        st.session_state.winner = None

def get_penalty_label(count):
    """Devuelve la etiqueta de la penalización según el conteo."""
    if count == 1:
        return "C"
    elif count == 2:
        return "K"
    elif count == 3:
        return "HC"
    elif count >= 4:
        return "H"
    return ""

def check_for_winner():
    """Verifica si hay un ganador."""
    if st.session_state.aka_score >= 8 and (st.session_state.aka_score - st.session_state.ao_score) >= 2:
        st.session_state.winner = 'AKA'
        st.session_state.timer_running = False
    elif st.session_state.ao_score >= 8 and (st.session_state.ao_score - st.session_state.aka_score) >= 2:
        st.session_state.winner = 'AO'
        st.session_state.timer_running = False
    elif get_penalty_label(st.session_state.ao_cat1) == 'H' or get_penalty_label(st.session_state.ao_cat2) == 'H':
        st.session_state.winner = 'AKA'
        st.session_state.timer_running = False
    elif get_penalty_label(st.session_state.aka_cat1) == 'H' or get_penalty_label(st.session_state.aka_cat2) == 'H':
        st.session_state.winner = 'AO'
        st.session_state.timer_running = False
    elif st.session_state.timer == 0:
        st.session_state.timer_running = False
        if st.session_state.aka_score > st.session_state.ao_score:
            st.session_state.winner = 'AKA'
        elif st.session_state.ao_score > st.session_state.aka_score:
            st.session_state.winner = 'AO'
        elif st.session_state.senshu:
            st.session_state.winner = st.session_state.senshu

# --- Inicialización del Estado ---
initialize_state()

# --- Atajos de Teclado ---
hotkeys = {
    "Y": "AKA Yuko", "U": "AKA Waza-ari", "I": "AKA Ippon",
    "G": "AO Yuko", "H": "AO Waza-ari", "J": "AO Ippon",
    "1": "AKA C1", "2": "AKA C2", "8": "AO C1", "9": "AO C2",
    "espacio": "Start/Stop Timer", "R": "Reset Match"
}
selected_hotkey = st_hotkeys(hotkeys)

if selected_hotkey:
    if selected_hotkey == "AKA Yuko": st.session_state.aka_score += 1
    if selected_hotkey == "AKA Waza-ari": st.session_state.aka_score += 2
    if selected_hotkey == "AKA Ippon": st.session_state.aka_score += 3
    if selected_hotkey == "AO Yuko": st.session_state.ao_score += 1
    if selected_hotkey == "AO Waza-ari": st.session_state.ao_score += 2
    if selected_hotkey == "AO Ippon": st.session_state.ao_score += 3
    if selected_hotkey == "AKA C1": st.session_state.aka_cat1 += 1
    if selected_hotkey == "AKA C2": st.session_state.aka_cat2 += 1
    if selected_hotkey == "AO C1": st.session_state.ao_cat1 += 1
    if selected_hotkey == "AO C2": st.session_state.ao_cat2 += 1
    if selected_hotkey == "Start/Stop Timer": st.session_state.timer_running = not st.session_state.timer_running
    if selected_hotkey == "Reset Match":
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

    # Lógica de Senshu
    if st.session_state.senshu is None and (st.session_state.aka_score > 0 or st.session_state.ao_score > 0):
        if st.session_state.aka_score > st.session_state.ao_score:
            st.session_state.senshu = 'AKA'
        elif st.session_state.ao_score > st.session_state.aka_score:
            st.session_state.senshu = 'AO'

    check_for_winner()

# --- Interfaz de Usuario ---
st.title("🥋 Marcador de Karate Kumite WKF")

col1, col2, col3 = st.columns([3, 1, 3])

with col1:
    st.markdown("<h1 style='text-align: center; color: red;'>AKA (赤)</h1>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; font-size: 150px; color: red;'>{st.session_state.aka_score}</h1>", unsafe_allow_html=True)

    if st.session_state.senshu == 'AKA':
        st.markdown("<p style='text-align: center; font-size: 24px; color: red;'>SENSHU</p>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    if c1.button("Yuko (+1)", key="aka_yuko"):
        st.session_state.aka_score += 1
        if st.session_state.senshu is None: st.session_state.senshu = 'AKA'
        check_for_winner()
    if c2.button("Waza-ari (+2)", key="aka_wazaari"):
        st.session_state.aka_score += 2
        if st.session_state.senshu is None: st.session_state.senshu = 'AKA'
        check_for_winner()
    if c3.button("Ippon (+3)", key="aka_ippon"):
        st.session_state.aka_score += 3
        if st.session_state.senshu is None: st.session_state.senshu = 'AKA'
        check_for_winner()

    st.markdown("---")
    st.subheader("Penalizaciones AKA")
    p1, p2 = st.columns(2)
    p1.metric("Categoría 1", get_penalty_label(st.session_state.aka_cat1))
    p2.metric("Categoría 2", get_penalty_label(st.session_state.aka_cat2))
    if p1.button("Falta C1", key="aka_c1"):
        st.session_state.aka_cat1 += 1
        check_for_winner()
    if p2.button("Falta C2", key="aka_c2"):
        st.session_state.aka_cat2 += 1
        check_for_winner()


with col3:
    st.markdown("<h1 style='text-align: center; color: blue;'>AO (青)</h1>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; font-size: 150px; color: blue;'>{st.session_state.ao_score}</h1>", unsafe_allow_html=True)

    if st.session_state.senshu == 'AO':
        st.markdown("<p style='text-align: center; font-size: 24px; color: blue;'>SENSHU</p>", unsafe_allow_html=True)

    c4, c5, c6 = st.columns(3)
    if c4.button("Yuko (+1)", key="ao_yuko"):
        st.session_state.ao_score += 1
        if st.session_state.senshu is None: st.session_state.senshu = 'AO'
        check_for_winner()
    if c5.button("Waza-ari (+2)", key="ao_wazaari"):
        st.session_state.ao_score += 2
        if st.session_state.senshu is None: st.session_state.senshu = 'AO'
        check_for_winner()
    if c6.button("Ippon (+3)", key="ao_ippon"):
        st.session_state.ao_score += 3
        if st.session_state.senshu is None: st.session_state.senshu = 'AO'
        check_for_winner()

    st.markdown("---")
    st.subheader("Penalizaciones AO")
    p3, p4 = st.columns(2)
    p3.metric("Categoría 1", get_penalty_label(st.session_state.ao_cat1))
    p4.metric("Categoría 2", get_penalty_label(st.session_state.ao_cat2))
    if p3.button("Falta C1", key="ao_c1"):
        st.session_state.ao_cat1 += 1
        check_for_winner()
    if p4.button("Falta C2", key="ao_c2"):
        st.session_state.ao_cat2 += 1
        check_for_winner()

with col2:
    st.markdown("<h2 style='text-align: center;'>Tiempo</h2>", unsafe_allow_html=True)
    timer_placeholder = st.empty()
    minutes, seconds = divmod(st.session_state.timer, 60)
    timer_placeholder.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{minutes:02d}:{seconds:02d}</h1>", unsafe_allow_html=True)

    t1, t2, t3 = st.columns(3)
    if t1.button("▶️", key="start_timer"):
        st.session_state.timer_running = True
    if t2.button("⏸️", key="stop_timer"):
        st.session_state.timer_running = False
    if t3.button("🔄", key="reset_timer"):
        st.session_state.timer = 180
        st.session_state.timer_running = False
        st.rerun()

st.markdown("---")
if st.session_state.winner:
    st.success(f"## ¡El ganador es {st.session_state.winner}! 🏆")

if st.button("Reiniciar Combate Completo"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

st.sidebar.title("Atajos de Teclado")
st.sidebar.markdown("""
- **Espacio**: Iniciar/Detener Tiempo
- **R**: Reiniciar Combate

**AKA (Rojo):**
- **Y**: Yuko (+1)
- **U**: Waza-ari (+2)
- **I**: Ippon (+3)
- **1**: Falta Categoría 1
- **2**: Falta Categoría 2

**AO (Azul):**
- **G**: Yuko (+1)
- **H**: Waza-ari (+2)
- **J**: Ippon (+3)
- **8**: Falta Categoría 1
- **9**: Falta Categoría 2
""")


# --- Lógica del Temporizador ---
if st.session_state.timer_running and st.session_state.timer > 0:
    time.sleep(1)
    st.session_state.timer -= 1
    if st.session_state.timer == 0:
        check_for_winner()
    st.rerun()

