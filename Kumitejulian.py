import streamlit as st
import time
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Karate Scoreboard WKF",
    page_icon="🥋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado para el scoreboard
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f4e79;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Separating AKA (red) and AO (blue) competitor sections */
    .competitor-section-aka {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(220,53,69,0.3);
        border: 3px solid #dc3545;
    }
    
    .competitor-section-ao {
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,123,255,0.3);
        border: 3px solid #007bff;
    }
    
    .competitor-name {
        font-size: 1.8rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .score-display {
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .timer-section {
        background: linear-gradient(135deg, #28a745 0%, #1e7e34 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .timer-display {
        font-size: 5rem;
        font-weight: bold;
        font-family: 'Courier New', monospace;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Different penalty section colors for AKA and AO */
    .penalty-section-aka {
        background: #f8d7da;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
        margin: 1rem 0;
        color: #721c24;
    }
    
    .penalty-section-ao {
        background: #d1ecf1;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        margin: 1rem 0;
        color: #0c5460;
    }
    
    .senshu-indicator {
        background: #ffc107;
        color: #212529;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem;
        box-shadow: 0 2px 8px rgba(255,193,7,0.4);
    }
    
    .victory-banner {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #333;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .control-section {
        background: #e9ecef;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# JavaScript para controles de teclado
keyboard_js = """
<script>
document.addEventListener('keydown', function(event) {
    const key = event.key.toLowerCase();
    
    // Prevenir comportamiento por defecto para nuestras teclas
    if (['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c', 'v', ' ', 'r'].includes(key)) {
        event.preventDefault();
    }
    
    // Simular clicks en botones basado en teclas presionadas
    switch(key) {
        // Competidor AKA (Izquierda)
        case 'q': // Yuko AKA
            document.querySelector('[data-testid="stButton"]:nth-of-type(1) button')?.click();
            break;
        case 'w': // Waza-ari AKA
            document.querySelector('[data-testid="stButton"]:nth-of-type(2) button')?.click();
            break;
        case 'e': // Ippon AKA
            document.querySelector('[data-testid="stButton"]:nth-of-type(3) button')?.click();
            break;
        case 'a': // Chukoku AKA
            document.querySelector('[data-testid="stButton"]:nth-of-type(4) button')?.click();
            break;
        case 's': // Keikoku AKA
            document.querySelector('[data-testid="stButton"]:nth-of-type(5) button')?.click();
            break;
        case 'd': // Hansoku-chui AKA
            document.querySelector('[data-testid="stButton"]:nth-of-type(6) button')?.click();
            break;
        case 'z': // Reset AKA
            document.querySelector('[data-testid="stButton"]:nth-of-type(7) button')?.click();
            break;
            
        // Competidor AO (Derecha)
        case 'u': // Yuko AO
            document.querySelector('[data-testid="stButton"]:nth-of-type(8) button')?.click();
            break;
        case 'i': // Waza-ari AO
            document.querySelector('[data-testid="stButton"]:nth-of-type(9) button')?.click();
            break;
        case 'o': // Ippon AO
            document.querySelector('[data-testid="stButton"]:nth-of-type(10) button')?.click();
            break;
        case 'j': // Chukoku AO
            document.querySelector('[data-testid="stButton"]:nth-of-type(11) button')?.click();
            break;
        case 'k': // Keikoku AO
            document.querySelector('[data-testid="stButton"]:nth-of-type(12) button')?.click();
            break;
        case 'l': // Hansoku-chui AO
            document.querySelector('[data-testid="stButton"]:nth-of-type(13) button')?.click();
            break;
        case 'm': // Reset AO
            document.querySelector('[data-testid="stButton"]:nth-of-type(14) button')?.click();
            break;
            
        // Controles de tiempo
        case ' ': // Espacio - Start/Stop
            document.querySelector('[data-testid="stButton"]:nth-of-type(15) button')?.click();
            break;
        case 'r': // Reset timer
            document.querySelector('[data-testid="stButton"]:nth-of-type(17) button')?.click();
            break;
    }
});
</script>
"""

# Inicializar estado de la sesión
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.aka_score = 0
    st.session_state.ao_score = 0
    st.session_state.aka_penalties = {'chukoku': 0, 'keikoku': 0, 'hansoku_chui': 0, 'hansoku': False}
    st.session_state.ao_penalties = {'chukoku': 0, 'keikoku': 0, 'hansoku_chui': 0, 'hansoku': False}
    st.session_state.senshu = None  # 'aka' o 'ao' o None
    st.session_state.timer_running = False
    st.session_state.start_time = None
    st.session_state.elapsed_time = 0
    st.session_state.match_duration = 180  # 3 minutos por defecto
    st.session_state.winner = None
    st.session_state.victory_reason = None

def format_time(seconds):
    """Formatear tiempo en MM:SS"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def check_victory():
    """Verificar condiciones de victoria según reglamento WKF"""
    # Victoria por Hansoku
    if st.session_state.aka_penalties['hansoku']:
        st.session_state.winner = 'AO'
        st.session_state.victory_reason = 'Victoria por Hansoku del oponente'
        return True
    if st.session_state.ao_penalties['hansoku']:
        st.session_state.winner = 'AKA'
        st.session_state.victory_reason = 'Victoria por Hansoku del oponente'
        return True
    
    # Victoria por diferencia de 8 puntos
    score_diff = abs(st.session_state.aka_score - st.session_state.ao_score)
    if score_diff >= 8:
        if st.session_state.aka_score > st.session_state.ao_score:
            st.session_state.winner = 'AKA'
        else:
            st.session_state.winner = 'AO'
        st.session_state.victory_reason = 'Victoria por diferencia de 8 puntos'
        return True
    
    return False

def add_score(competitor, points):
    """Agregar puntos y verificar Senshu"""
    if competitor == 'aka':
        st.session_state.aka_score += points
        if st.session_state.senshu is None and points > 0:
            st.session_state.senshu = 'aka'
    else:
        st.session_state.ao_score += points
        if st.session_state.senshu is None and points > 0:
            st.session_state.senshu = 'ao'
    
    check_victory()

def add_penalty(competitor, penalty_type):
    """Agregar penalización según reglamento WKF"""
    penalties = st.session_state.aka_penalties if competitor == 'aka' else st.session_state.ao_penalties
    opponent = 'ao' if competitor == 'aka' else 'aka'
    
    if penalty_type == 'chukoku':
        penalties['chukoku'] += 1
    elif penalty_type == 'keikoku':
        penalties['keikoku'] += 1
        # Keikoku otorga Yuko al oponente
        add_score(opponent, 1)
    elif penalty_type == 'hansoku_chui':
        penalties['hansoku_chui'] += 1
        # Hansoku-chui otorga Waza-ari al oponente
        add_score(opponent, 2)
    elif penalty_type == 'hansoku':
        penalties['hansoku'] = True
        check_victory()

def reset_competitor(competitor):
    """Resetear puntuación y penalizaciones de un competidor"""
    if competitor == 'aka':
        st.session_state.aka_score = 0
        st.session_state.aka_penalties = {'chukoku': 0, 'keikoku': 0, 'hansoku_chui': 0, 'hansoku': False}
    else:
        st.session_state.ao_score = 0
        st.session_state.ao_penalties = {'chukoku': 0, 'keikoku': 0, 'hansoku_chui': 0, 'hansoku': False}
    
    # Resetear Senshu si era de este competidor
    if st.session_state.senshu == competitor:
        st.session_state.senshu = None
    
    st.session_state.winner = None
    st.session_state.victory_reason = None

# Título principal
st.markdown('<h1 class="main-header">🥋 KARATE SCOREBOARD WKF</h1>', unsafe_allow_html=True)

# Configuración del combate
with st.expander("⚙️ Configuración del Combate", expanded=False):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        aka_name = st.text_input("Nombre AKA (Rojo)", value="AKA", key="aka_name")
    
    with col2:
        ao_name = st.text_input("Nombre AO (Azul)", value="AO", key="ao_name")
    
    with col3:
        duration_minutes = st.selectbox("Duración (minutos)", [1, 2, 3, 4, 5], index=2)
        st.session_state.match_duration = duration_minutes * 60

# Sección del temporizador
st.markdown('<div class="timer-section">', unsafe_allow_html=True)

# Calcular tiempo actual
current_time = st.session_state.elapsed_time
if st.session_state.timer_running and st.session_state.start_time:
    current_time += time.time() - st.session_state.start_time

remaining_time = max(0, st.session_state.match_duration - current_time)

st.markdown(f'<div class="timer-display">{format_time(remaining_time)}</div>', unsafe_allow_html=True)

# Controles del temporizador
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶️ Start" if not st.session_state.timer_running else "⏸️ Pause", key="timer_control"):
        if not st.session_state.timer_running:
            st.session_state.timer_running = True
            st.session_state.start_time = time.time()
        else:
            st.session_state.timer_running = False
            if st.session_state.start_time:
                st.session_state.elapsed_time += time.time() - st.session_state.start_time
            st.session_state.start_time = None

with col2:
    if st.button("⏹️ Stop", key="timer_stop"):
        st.session_state.timer_running = False
        if st.session_state.start_time:
            st.session_state.elapsed_time += time.time() - st.session_state.start_time
        st.session_state.start_time = None

with col3:
    if st.button("🔄 Reset Timer", key="timer_reset"):
        st.session_state.timer_running = False
        st.session_state.start_time = None
        st.session_state.elapsed_time = 0

st.markdown('</div>', unsafe_allow_html=True)

# Verificar si el tiempo se agotó
if remaining_time <= 0 and not st.session_state.winner:
    st.session_state.timer_running = False
    # Determinar ganador por puntos o Senshu
    if st.session_state.aka_score > st.session_state.ao_score:
        st.session_state.winner = 'AKA'
        st.session_state.victory_reason = 'Victoria por puntos'
    elif st.session_state.ao_score > st.session_state.aka_score:
        st.session_state.winner = 'AO'
        st.session_state.victory_reason = 'Victoria por puntos'
    elif st.session_state.senshu == 'aka':
        st.session_state.winner = 'AKA'
        st.session_state.victory_reason = 'Victoria por Senshu'
    elif st.session_state.senshu == 'ao':
        st.session_state.winner = 'AO'
        st.session_state.victory_reason = 'Victoria por Senshu'
    else:
        st.session_state.winner = 'EMPATE'
        st.session_state.victory_reason = 'Combate empatado'

# Banner de victoria
if st.session_state.winner:
    if st.session_state.winner == 'EMPATE':
        st.markdown(f'<div class="victory-banner">🤝 EMPATE<br><small>{st.session_state.victory_reason}</small></div>', unsafe_allow_html=True)
    else:
        winner_name = aka_name if st.session_state.winner == 'AKA' else ao_name
        st.markdown(f'<div class="victory-banner">🏆 VICTORIA: {winner_name} ({st.session_state.winner})<br><small>{st.session_state.victory_reason}</small></div>', unsafe_allow_html=True)

# Secciones de competidores
col1, col2 = st.columns(2)

# Competidor AKA (Izquierda)
with col1:
    st.markdown('<div class="competitor-section-aka">', unsafe_allow_html=True)
    st.markdown(f'<div class="competitor-name">🔴 {aka_name} (AKA)</div>', unsafe_allow_html=True)
    
    # Indicador Senshu
    if st.session_state.senshu == 'aka':
        st.markdown('<div class="senshu-indicator">⭐ SENSHU</div>', unsafe_allow_html=True)
    
    # Puntuación
    st.markdown(f'<div class="score-display">{st.session_state.aka_score}</div>', unsafe_allow_html=True)
    
    # Botones de puntuación
    st.markdown("**Puntuación:**")
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        if st.button("Yuko (1)", key="aka_yuko", disabled=bool(st.session_state.winner)):
            add_score('aka', 1)
    
    with col_b:
        if st.button("Waza-ari (2)", key="aka_waza", disabled=bool(st.session_state.winner)):
            add_score('aka', 2)
    
    with col_c:
        if st.button("Ippon (3)", key="aka_ippon", disabled=bool(st.session_state.winner)):
            add_score('aka', 3)
    
    # Penalizaciones
    st.markdown("**Penalizaciones:**")
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        if st.button("Chukoku", key="aka_chukoku", disabled=bool(st.session_state.winner)):
            add_penalty('aka', 'chukoku')
    
    with col_b:
        if st.button("Keikoku", key="aka_keikoku", disabled=bool(st.session_state.winner)):
            add_penalty('aka', 'keikoku')
    
    with col_c:
        if st.button("Hansoku-chui", key="aka_hansoku_chui", disabled=bool(st.session_state.winner)):
            add_penalty('aka', 'hansoku_chui')
    
    # Mostrar penalizaciones actuales
    if any(st.session_state.aka_penalties.values()):
        st.markdown('<div class="penalty-section-aka">', unsafe_allow_html=True)
        st.markdown("**Penalizaciones actuales:**")
        if st.session_state.aka_penalties['chukoku'] > 0:
            st.write(f"Chukoku: {st.session_state.aka_penalties['chukoku']}")
        if st.session_state.aka_penalties['keikoku'] > 0:
            st.write(f"Keikoku: {st.session_state.aka_penalties['keikoku']}")
        if st.session_state.aka_penalties['hansoku_chui'] > 0:
            st.write(f"Hansoku-chui: {st.session_state.aka_penalties['hansoku_chui']}")
        if st.session_state.aka_penalties['hansoku']:
            st.write("**HANSOKU**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Reset
    if st.button("🔄 Reset AKA", key="reset_aka"):
        reset_competitor('aka')
    
    st.markdown('</div>', unsafe_allow_html=True)

# Competidor AO (Derecha)
with col2:
    st.markdown('<div class="competitor-section-ao">', unsafe_allow_html=True)
    st.markdown(f'<div class="competitor-name">🔵 {ao_name} (AO)</div>', unsafe_allow_html=True)
    
    # Indicador Senshu
    if st.session_state.senshu == 'ao':
        st.markdown('<div class="senshu-indicator">⭐ SENSHU</div>', unsafe_allow_html=True)
    
    # Puntuación
    st.markdown(f'<div class="score-display">{st.session_state.ao_score}</div>', unsafe_allow_html=True)
    
    # Botones de puntuación
    st.markdown("**Puntuación:**")
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        if st.button("Yuko (1)", key="ao_yuko", disabled=bool(st.session_state.winner)):
            add_score('ao', 1)
    
    with col_b:
        if st.button("Waza-ari (2)", key="ao_waza", disabled=bool(st.session_state.winner)):
            add_score('ao', 2)
    
    with col_c:
        if st.button("Ippon (3)", key="ao_ippon", disabled=bool(st.session_state.winner)):
            add_score('ao', 3)
    
    # Penalizaciones
    st.markdown("**Penalizaciones:**")
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        if st.button("Chukoku", key="ao_chukoku", disabled=bool(st.session_state.winner)):
            add_penalty('ao', 'chukoku')
    
    with col_b:
        if st.button("Keikoku", key="ao_keikoku", disabled=bool(st.session_state.winner)):
            add_penalty('ao', 'keikoku')
    
    with col_c:
        if st.button("Hansoku-chui", key="ao_hansoku_chui", disabled=bool(st.session_state.winner)):
            add_penalty('ao', 'hansoku_chui')
    
    # Mostrar penalizaciones actuales
    if any(st.session_state.ao_penalties.values()):
        st.markdown('<div class="penalty-section-ao">', unsafe_allow_html=True)
        st.markdown("**Penalizaciones actuales:**")
        if st.session_state.ao_penalties['chukoku'] > 0:
            st.write(f"Chukoku: {st.session_state.ao_penalties['chukoku']}")
        if st.session_state.ao_penalties['keikoku'] > 0:
            st.write(f"Keikoku: {st.session_state.ao_penalties['keikoku']}")
        if st.session_state.ao_penalties['hansoku_chui'] > 0:
            st.write(f"Hansoku-chui: {st.session_state.ao_penalties['hansoku_chui']}")
        if st.session_state.ao_penalties['hansoku']:
            st.write("**HANSOKU**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Reset
    if st.button("🔄 Reset AO", key="reset_ao"):
        reset_competitor('ao')
    
    st.markdown('</div>', unsafe_allow_html=True)

# Controles generales
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Reset Todo", key="reset_all"):
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

with col2:
    if st.button("⚡ Hansoku AKA", key="hansoku_aka"):
        add_penalty('aka', 'hansoku')
