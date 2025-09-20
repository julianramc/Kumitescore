import streamlit as st
import time
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Karate Scoreboard WKF",
    page_icon="🥋",
    layout="wide",
    initial_sidebar_state="auto" # La barra lateral estará abierta al inicio
)

# --- CSS MEJORADO PARA EL NUEVO LAYOUT ---
st.markdown("""
<style>
    /* Ocultar el menú de Streamlit y el footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Contenedor principal para centrar contenido */
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .main-header {
        text-align: center;
        color: #1f4e79;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem; /* Margen reducido */
    }

    /* Estilo de tarjeta para cada competidor */
    .competitor-card {
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        border: 3px solid;
        height: 100%; /* Para que todas las tarjetas tengan la misma altura */
    }

    .card-aka {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        border-color: #c82333;
    }

    .card-ao {
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        border-color: #0056b3;
    }
    
    /* Estilo para el componente st.metric */
    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    [data-testid="stMetric"] > label {
        font-size: 1.5rem; /* Tamaño del nombre del competidor */
        font-weight: bold;
        color: white;
    }
    [data-testid="stMetric"] p {
        font-size: 5rem !important; /* Tamaño del número de puntos */
        font-weight: bold;
        color: white;
    }

    .timer-display {
        font-size: 6rem; /* Tiempo más grande */
        font-weight: bold;
        font-family: 'Courier New', monospace;
        color: #28a745;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem 0;
        margin-bottom: 1rem;
    }
    
    .senshu-indicator {
        background: #ffc107;
        color: #212529;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-top: 1rem;
    }

    .penalty-display {
        font-size: 1.1rem;
        font-weight: bold;
        margin-top: 1rem;
        background-color: rgba(0, 0, 0, 0.2);
        padding: 0.5rem;
        border-radius: 8px;
    }
    
    .stButton > button {
        width: 100%;
        font-weight: bold;
    }

    .victory-banner {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #333;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# --- JAVASCRIPTS (sin cambios en su lógica) ---
keyboard_js = """
<script>
document.addEventListener('keydown', function(event) {
    const key = event.key.toLowerCase();
    const keyMap = {
        'q': 1, 'w': 2, 'e': 3, 'a': 4, 's': 5, 'd': 6, 'z': 7,
        'u': 8, 'i': 9, 'o': 10, 'j': 11, 'k': 12, 'l': 13, 'm': 14,
        ' ': 15, 'r': 16
    };
    if (keyMap[key]) {
        event.preventDefault();
        const button = document.querySelector(`[data-testid="stButton"]:nth-of-type(${keyMap[key]}) button`);
        if (button) button.click();
    }
});
</script>
"""
auto_refresh_js = "<script>setInterval(() => {window.parent.dispatchEvent(new Event('resize'));}, 150);</script>"

# --- INICIALIZACIÓN Y FUNCIONES (sin cambios en su lógica) ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.aka_score = 0
    st.session_state.ao_score = 0
    st.session_state.aka_penalties = {'chukoku': 0, 'keikoku': 0, 'hansoku_chui': 0, 'hansoku': False}
    st.session_state.ao_penalties = {'chukoku': 0, 'keikoku': 0, 'hansoku_chui': 0, 'hansoku': False}
    st.session_state.senshu = None
    st.session_state.timer_running = False
    st.session_state.start_time = None
    st.session_state.elapsed_time = 0
    st.session_state.match_duration = 180
    st.session_state.winner = None
    st.session_state.victory_reason = None

# (Las funciones format_time, check_victory, add_score, add_penalty, reset_competitor son las mismas)
def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def check_victory():
    if st.session_state.winner: return True
    reason = None
    winner = None
    if st.session_state.aka_penalties['hansoku']: winner, reason = 'AO', 'Hansoku del oponente'
    elif st.session_state.ao_penalties['hansoku']: winner, reason = 'AKA', 'Hansoku del oponente'
    elif abs(st.session_state.aka_score - st.session_state.ao_score) >= 8:
        winner = 'AKA' if st.session_state.aka_score > st.session_state.ao_score else 'AO'
        reason = 'Diferencia de 8 puntos'
    
    if winner:
        st.session_state.winner = winner
        st.session_state.victory_reason = reason
        st.session_state.timer_running = False
        return True
    return False

def add_score(competitor, points):
    if st.session_state.winner: return
    is_aka = competitor == 'aka'
    if is_aka: st.session_state.aka_score += points
    else: st.session_state.ao_score += points
    if st.session_state.senshu is None and points > 0: st.session_state.senshu = competitor
    check_victory()

def add_penalty(competitor, penalty_type):
    if st.session_state.winner: return
    penalties = st.session_state.aka_penalties if competitor == 'aka' else st.session_state.ao_penalties
    opponent = 'ao' if competitor == 'aka' else 'aka'
    if penalty_type == 'chukoku': penalties['chukoku'] += 1
    elif penalty_type == 'keikoku': penalties['keikoku'] += 1; add_score(opponent, 1)
    elif penalty_type == 'hansoku_chui': penalties['hansoku_chui'] += 1; add_score(opponent, 2)
    elif penalty_type == 'hansoku': penalties['hansoku'] = True; check_victory()

def reset_competitor(competitor):
    is_aka = competitor == 'aka'
    if is_aka:
        st.session_state.aka_score = 0
        st.session_state.aka_penalties = {'chukoku': 0, 'keikoku': 0, 'hansoku_chui': 0, 'hansoku': False}
    else:
        st.session_state.ao_score = 0
        st.session_state.ao_penalties = {'chukoku': 0, 'keikoku': 0, 'hansoku_chui': 0, 'hansoku': False}
    if st.session_state.senshu == competitor: st.session_state.senshu = None
    st.session_state.winner = None
    st.session_state.victory_reason = None

def reset_all():
    st.session_state.aka_score = 0
    st.session_state.ao_score = 0
    st.session_state.aka_penalties = {'chukoku': 0, 'keikoku': 0, 'hansoku_chui': 0, 'hansoku': False}
    st.session_state.ao_penalties = {'chukoku': 0, 'keikoku': 0, 'hansoku_chui': 0, 'hansoku': False}
    st.session_state.senshu = None
    st.session_state.timer_running = False
    st.session_state.start_time = None
    st.session_state.elapsed_time = 0
    st.session_state.winner = None
    st.session_state.victory_reason = None
    
# --- BARRA LATERAL (SIDEBAR) PARA CONFIGURACIÓN Y AYUDA ---
with st.sidebar:
    st.title("⚙️ Configuración")
    aka_name = st.text_input("Nombre AKA (Rojo)", value="AKA", key="aka_name")
    ao_name = st.text_input("Nombre AO (Azul)", value="AO", key="ao_name")
    
    duration_minutes = st.selectbox("Duración (minutos)", [1, 2, 3, 4, 5], index=2)
    if st.button("Aplicar Duración y Resetear", use_container_width=True):
        st.session_state.match_duration = duration_minutes * 60
        reset_all() # Resetear todo al cambiar la duración para evitar inconsistencias
        
    with st.expander("⌨️ Controles de Teclado", expanded=False):
        st.markdown("""
        **AKA (Izquierda):** `Q` `W` `E` (Puntos), `A` `S` `D` (Penas)
        **AO (Derecha):** `U` `I` `O` (Puntos), `J` `K` `L` (Penas)
        **Tiempo:** `Espacio` (Play/Pausa), `R` (Reset)
        """)
    
# --- LAYOUT PRINCIPAL DE LA APLICACIÓN ---
st.markdown('<h1 class="main-header">🥋 KARATE SCOREBOARD WKF</h1>', unsafe_allow_html=True)

# Banner de victoria
if st.session_state.winner:
    winner_name = aka_name if st.session_state.winner == 'AKA' else ao_name
    st.markdown(f'<div class="victory-banner">🏆 VICTORIA: {winner_name} ({st.session_state.winner})<br><small>{st.session_state.victory_reason}</small></div>', unsafe_allow_html=True)

# --- NUEVO LAYOUT DE 3 COLUMNAS ---
col_aka, col_timer, col_ao = st.columns([3, 2, 3]) # AKA | TIMER | AO

# --- COLUMNA AKA (IZQUIERDA) ---
with col_aka:
    st.markdown('<div class="competitor-card card-aka">', unsafe_allow_html=True)
    
    # Marcador con st.metric
    st.metric(label=f"🔴 {aka_name} (AKA)", value=st.session_state.aka_score)

    # Indicador Senshu y Penalizaciones
    if st.session_state.senshu == 'aka':
        st.markdown('<div class="senshu-indicator">⭐ SENSHU</div>', unsafe_allow_html=True)
    
    penalties = st.session_state.aka_penalties
    penalty_text = f"C: {penalties['chukoku']} | K: {penalties['keikoku']} | HC: {penalties['hansoku_chui']}"
    st.markdown(f'<div class="penalty-display">{penalty_text}</div>', unsafe_allow_html=True)
    if penalties['hansoku']: st.error("**HANSOKU**")
    
    st.markdown("---")
    # Botones de puntuación
    btn_cols = st.columns(3)
    if btn_cols[0].button("Yuko (1)", key="aka_yuko", disabled=bool(st.session_state.winner), use_container_width=True): add_score('aka', 1)
    if btn_cols[1].button("Waza-ari (2)", key="aka_waza", disabled=bool(st.session_state.winner), use_container_width=True): add_score('aka', 2)
    if btn_cols[2].button("Ippon (3)", key="aka_ippon", disabled=bool(st.session_state.winner), use_container_width=True): add_score('aka', 3)
    
    # Botones de penalización
    penalty_cols = st.columns(3)
    if penalty_cols[0].button("Chukoku", key="aka_chukoku", disabled=bool(st.session_state.winner), use_container_width=True): add_penalty('aka', 'chukoku')
    if penalty_cols[1].button("Keikoku", key="aka_keikoku", disabled=bool(st.session_state.winner), use_container_width=True): add_penalty('aka', 'keikoku')
    if penalty_cols[2].button("Hansoku-chui", key="aka_hansoku_chui", disabled=bool(st.session_state.winner), use_container_width=True): add_penalty('aka', 'hansoku_chui')
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- COLUMNA CENTRAL (TIMER Y CONTROLES GLOBALES) ---
with col_timer:
    # Lógica del tiempo
    current_time = st.session_state.elapsed_time
    if st.session_state.timer_running:
        current_time = st.session_state.elapsed_time + (time.time() - st.session_state.start_time)
    remaining_time = max(0, st.session_state.match_duration - current_time)
    
    # Muestra del tiempo
    st.markdown(f'<div class="timer-display">{format_time(remaining_time)}</div>', unsafe_allow_html=True)

    # Controles del tiempo
    timer_cols = st.columns(2)
    if timer_cols[0].button("▶️ Start" if not st.session_state.timer_running else "⏸️ Pause", key="timer_control", use_container_width=True):
        if not st.session_state.winner:
            st.session_state.timer_running = not st.session_state.timer_running
            if st.session_state.timer_running:
                st.session_state.start_time = time.time()
            else:
                st.session_state.elapsed_time += time.time() - st.session_state.start_time

    if timer_cols[1].button("🔄 Reset Timer", key="timer_reset", use_container_width=True):
        st.session_state.timer_running = False
        st.session_state.start_time = None
        st.session_state.elapsed_time = 0

    st.markdown("---")
    
    # Controles globales
    st.button("🔄 RESETEAR COMBATE", key="reset_all", on_click=reset_all, use_container_width=True, type="primary")
    hansoku_cols = st.columns(2)
    if hansoku_cols[0].button("⚡ Hansoku AKA", key="hansoku_aka", use_container_width=True): add_penalty('aka', 'hansoku')
    if hansoku_cols[1].button("⚡ Hansoku AO", key="hansoku_ao", use_container_width=True): add_penalty('ao', 'hansoku')

# --- COLUMNA AO (DERECHA) ---
with col_ao:
    st.markdown('<div class="competitor-card card-ao">', unsafe_allow_html=True)
    
    # Marcador con st.metric
    st.metric(label=f"🔵 {ao_name} (AO)", value=st.session_state.ao_score)
    
    # Indicador Senshu y Penalizaciones
    if st.session_state.senshu == 'ao':
        st.markdown('<div class="senshu-indicator">⭐ SENSHU</div>', unsafe_allow_html=True)

    penalties = st.session_state.ao_penalties
    penalty_text = f"C: {penalties['chukoku']} | K: {penalties['keikoku']} | HC: {penalties['hansoku_chui']}"
    st.markdown(f'<div class="penalty-display">{penalty_text}</div>', unsafe_allow_html=True)
    if penalties['hansoku']: st.error("**HANSOKU**")
    
    st.markdown("---")
    # Botones de puntuación
    btn_cols = st.columns(3)
    if btn_cols[0].button("Yuko (1)", key="ao_yuko", disabled=bool(st.session_state.winner), use_container_width=True): add_score('ao', 1)
    if btn_cols[1].button("Waza-ari (2)", key="ao_waza", disabled=bool(st.session_state.winner), use_container_width=True): add_score('ao', 2)
    if btn_cols[2].button("Ippon (3)", key="ao_ippon", disabled=bool(st.session_state.winner), use_container_width=True): add_score('ao', 3)
    
    # Botones de penalización
    penalty_cols = st.columns(3)
    if penalty_cols[0].button("Chukoku", key="ao_chukoku", disabled=bool(st.session_state.winner), use_container_width=True): add_penalty('ao', 'chukoku')
    if penalty_cols[1].button("Keikoku", key="ao_keikoku", disabled=bool(st.session_state.winner), use_container_width=True): add_penalty('ao', 'keikoku')
    if penalty_cols[2].button("Hansoku-chui", key="ao_hansoku_chui", disabled=bool(st.session_state.winner), use_container_width=True): add_penalty('ao', 'hansoku_chui')
    
    st.markdown("</div>", unsafe_allow_html=True)


# --- Lógica de fin de combate por tiempo ---
if remaining_time <= 0 and not st.session_state.winner:
    st.session_state.timer_running = False
    if st.session_state.aka_score > st.session_state.ao_score: winner, reason = 'AKA', 'Puntos'
    elif st.session_state.ao_score > st.session_state.aka_score: winner, reason = 'AO', 'Puntos'
    elif st.session_state.senshu: winner, reason = st.session_state.senshu.upper(), 'Senshu'
    else: winner, reason = 'EMPATE', 'Combate empatado'
    st.session_state.winner = winner
    st.session_state.victory_reason = reason
    st.rerun() # Forzar rerun para mostrar el banner de victoria inmediatamente

# --- Insertar JS ---
components.html(keyboard_js, height=0)
if st.session_state.timer_running:
    components.html(auto_refresh_js, height=0)

