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
    if st.session_state.winner: # Si ya hay un ganador, no hacer nada
        return

    # Condiciones de victoria por puntos o penalizaciones
    if st.session_state.aka_score >= 8:
        st.session_state.winner = 'AKA'
    elif st.session_state.ao_score >= 8:
        st.session_state.winner = 'AO'
    elif get_penalty_label(st.session_state.ao_cat1) == 'H' or get_penalty_label(st.session_state.ao_cat2) == 'H':
        st.session_state.winner = 'AKA'
    elif get_penalty_label(st.session_state.aka_cat1) == 'H' or get_penalty_label(st.session_state.aka_cat2) == 'H':
        st.session_state.winner = 'AO'
    
    # Condición de victoria al final del tiempo
    elif st.session_state.timer == 0:
        if st.session_state.aka_score > st.session_state.ao_score:
            st.session_state.winner = 'AKA'
        elif st.session_state.ao_score > st.session_state.aka_score:
            st.session_state.winner = 'AO'
        elif st.session_state.senshu:
            st.session_state.winner = st.session_state.senshu
        else: # Empate sin senshu
            st.session_state.winner = "HIKIWAKE (EMPATE)"

    if st.session_state.winner:
        st.session_state.timer_running = False


def handle_scoring(competitor, points):
    """Maneja la lógica de puntuación y senshu."""
    if st.session_state.winner: return
    
    if competitor == 'AKA':
        st.session_state.aka_score += points
    else:
        st.session_state.ao_score += points
    
    if st.session_state.senshu is None:
        st.session_state.senshu = competitor
    
    check_for_winner()

def handle_penalty(competitor, category):
    """Maneja la lógica de penalizaciones."""
    if st.session_state.winner: return

    if competitor == 'AKA':
        if category == 1:
            st.session_state.aka_cat1 += 1
        else:
            st.session_state.aka_cat2 += 1
    else: # AO
        if category == 1:
            st.session_state.ao_cat1 += 1
        else:
            st.session_state.ao_cat2 += 1
    check_for_winner()

def reset_match():
    """Reinicia todo el estado de la sesión."""
    keys_to_keep = [] # Lista de claves a no borrar, si las hubiera
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]
    initialize_state() # Reinicializa el estado a sus valores por defecto
    st.rerun()

# --- Inicialización del Estado ---
initialize_state()

# --- Atajos de Teclado (Hotkeys) ---
hotkeys_dict = {
    "Y": "AKA Yuko", "U": "AKA Waza-ari", "I": "AKA Ippon",
    "G": "AO Yuko", "H": "AO Waza-ari", "J": "AO Ippon",
    "1": "AKA C1", "2": "AKA C2", 
    "8": "AO C1", "9": "AO C2",
    " ": "Start/Stop Timer", "R": "Reset Match"
}
# La función st_hotkeys debe estar fuera de cualquier callback o if
selected_hotkey = st_hotkeys(hotkeys_dict, return_type='TEXT')

if selected_hotkey:
    if selected_hotkey == "AKA Yuko": handle_scoring('AKA', 1)
    elif selected_hotkey == "AKA Waza-ari": handle_scoring('AKA', 2)
    elif selected_hotkey == "AKA Ippon": handle_scoring('AKA', 3)
    elif selected_hotkey == "AO Yuko": handle_scoring('AO', 1)
    elif selected_hotkey == "AO Waza-ari": handle_scoring('AO', 2)
    elif selected_hotkey == "AO Ippon": handle_scoring('AO', 3)
    elif selected_hotkey == "AKA C1": handle_penalty('AKA', 1)
    elif selected_hotkey == "AKA C2": handle_penalty('AKA', 2)
    elif selected_hotkey == "AO C1": handle_penalty('AO', 1)
    elif selected_hotkey == "AO C2": handle_penalty('AO', 2)
    elif selected_hotkey == "Start/Stop Timer":
        if not st.session_state.winner:
            st.session_state.timer_running = not st.session_state.timer_running
    elif selected_hotkey == "Reset Match":
        reset_match()


# --- Interfaz de Usuario (UI) ---
st.title("🥋 Marcador de Karate Kumite WKF")

col1, col2, col3 = st.columns([3, 1.5, 3])

# --- Columna AKA (Roja) ---
with col1:
    st.markdown("<h1 style='text-align: center; color: red;'>AKA (赤)</h1>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; font-size: 150px; color: red;'>{st.session_state.aka_score}</h1>", unsafe_allow_html=True)

    if st.session_state.senshu == 'AKA':
        st.markdown("<p style='text-align: center; font-size: 24px; color: red;'>SENSHU</p>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    if c1.button("Yuko (+1)", key="aka_yuko", use_container_width=True): handle_scoring('AKA', 1)
    if c2.button("Waza-ari (+2)", key="aka_wazaari", use_container_width=True): handle_scoring('AKA', 2)
    if c3.button("Ippon (+3)", key="aka_ippon", use_container_width=True): handle_scoring('AKA', 3)

    st.markdown("---")
    st.subheader("Penalizaciones AKA")
    p1, p2 = st.columns(2)
    p1.metric("Categoría 1", get_penalty_label(st.session_state.aka_cat1))
    p2.metric("Categoría 2", get_penalty_label(st.session_state.aka_cat2))
    if p1.button("Falta C1", key="aka_c1", use_container_width=True): handle_penalty('AKA', 1)
    if p2.button("Falta C2", key="aka_c2", use_container_width=True): handle_penalty('AKA', 2)

# --- Columna AO (Azul) ---
with col3:
    st.markdown("<h1 style='text-align: center; color: blue;'>AO (青)</h1>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; font-size: 150px; color: blue;'>{st.session_state.ao_score}</h1>", unsafe_allow_html=True)

    if st.session_state.senshu == 'AO':
        st.markdown("<p style='text-align: center; font-size: 24px; color: blue;'>SENSHU</p>", unsafe_allow_html=True)

    c4, c5, c6 = st.columns(3)
    if c4.button("Yuko (+1)", key="ao_yuko", use_container_width=True): handle_scoring('AO', 1)
    if c5.button("Waza-ari (+2)", key="ao_wazaari", use_container_width=True): handle_scoring('AO', 2)
    if c6.button("Ippon (+3)", key="ao_ippon", use_container_width=True): handle_scoring('AO', 3)

    st.markdown("---")
    st.subheader("Penalizaciones AO")
    p3, p4 = st.columns(2)
    p3.metric("Categoría 1", get_penalty_label(st.session_state.ao_cat1))
    p4.metric("Categoría 2", get_penalty_label(st.session_state.ao_cat2))
    if p3.button("Falta C1", key="ao_c1", use_container_width=True): handle_penalty('AO', 1)
    if p4.button("Falta C2", key="ao_c2", use_container_width=True): handle_penalty('AO', 2)

# --- Columna Central (Tiempo y Controles) ---
with col2:
    st.markdown("<h2 style='text-align: center;'>Tiempo</h2>", unsafe_allow_html=True)
    timer_placeholder = st.empty()
    minutes, seconds = divmod(st.session_state.timer, 60)
    timer_placeholder.markdown(f"<h1 style='text-align: center; font-size: 70px;'>{minutes:02d}:{seconds:02d}</h1>", unsafe_allow_html=True)

    t1, t2 = st.columns(2)
    if t1.button("▶️ / ⏸️", key="start_stop_timer", use_container_width=True):
        if not st.session_state.winner:
            st.session_state.timer_running = not st.session_state.timer_running
    
    if t2.button("🔄", key="reset_timer", use_container_width=True):
        st.session_state.timer = 180
        st.session_state.timer_running = False
        st.rerun()

st.markdown("---")
if st.session_state.winner:
    st.success(f"## ¡El ganador es {st.session_state.winner}! 🏆")

if st.button("Reiniciar Combate Completo", use_container_width=True):
    reset_match()

# --- Lógica del Temporizador (al final para que la UI se dibuje primero) ---
if st.session_state.timer_running and st.session_state.timer > 0:
    time.sleep(1)
    st.session_state.timer -= 1
    if st.session_state.timer == 0:
        check_for_winner()
    st.rerun()

