import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# ───────────────────────────────────────────────────────────────
# Configuración de la página
# ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Modelo IS-LM Interactivo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ───────────────────────────────────────────────────────────────
# Título y descripción
# ──────────────────────────────────────────────────────────────
st.title(" Modelo IS-LM Interactivo")
st.markdown("""
Desplaza las curvas **IS** (mercado de bienes) y **LM** (mercado de dinero) 
para observar cómo cambia el punto de equilibrio en la economía.
""")

# ──────────────────────────────────────────────────────────────
# Parámetros base del modelo
# ──────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Parámetros Base")

# Parámetros de la curva IS: r = a - b*Y
a_base = st.sidebar.number_input("Intercepto IS (a)", value=9.0, step=0.1)
b = st.sidebar.number_input("Pendiente IS (b)", value=0.6, step=0.1)

# Parámetros de la curva LM: r = c + d*Y
c_base = st.sidebar.number_input("Intercepto LM (c)", value=1.0, step=0.1)
d = st.sidebar.number_input("Pendiente LM (d)", value=0.7, step=0.1)

st.sidebar.markdown("---")

# ───────────────────────────────────────────────────────────────
# Sliders de desplazamiento
# ──────────────────────────────────────────────────────────────
st.sidebar.header("🔄 Desplazamientos")

# Desplazamiento vertical de IS
delta_IS = st.sidebar.slider(
    "Desplazamiento IS (Δ)",
    min_value=-5.0,
    max_value=5.0,
    value=0.0,
    step=0.1,
    format="%.1f"
)

# Desplazamiento vertical de LM
delta_LM = st.sidebar.slider(
    "Desplazamiento LM (Δ)",
    min_value=-5.0,
    max_value=5.0,
    value=0.0,
    step=0.1,
    format="%.1f"
)

# ───────────────────────────────────────────────────────────────
# Calcular curvas con desplazamientos
# ──────────────────────────────────────────────────────────────
Y = np.linspace(0, 10, 100)

# Curva IS: r = (a + delta_IS) - b*Y
# Un delta positivo desplaza IS hacia arriba/derecha
r_IS = (a_base + delta_IS) - b * Y

# Curva LM: r = (c + delta_LM) + d*Y
# Un delta positivo desplaza LM hacia arriba/izquierda
r_LM = (c_base + delta_LM) + d * Y

# ───────────────────────────────────────────────────────────────
# Calcular punto de equilibrio
# ──────────────────────────────────────────────────────────────
# En equilibrio: IS = LM
# (a + delta_IS) - b*Y = (c + delta_LM) + d*Y
# (a + delta_IS) - (c + delta_LM) = (b + d)*Y
# Y = [(a + delta_IS) - (c + delta_LM)] / (b + d)

a_actual = a_base + delta_IS
c_actual = c_base + delta_LM

Y_eq = (a_actual - c_actual) / (b + d)
r_eq = a_actual - b * Y_eq  # o también: r_eq = c_actual + d * Y_eq

# ──────────────────────────────────────────────────────────────
# Mostrar métricas de equilibrio
# ──────────────────────────────────────────────────────────────
st.markdown("### 📈 Punto de Equilibrio Actual")
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Producto/Ingreso de Equilibrio (Y*)",
        value=f"{Y_eq:.2f}",
        delta=f"{Y_eq - ((a_base - c_base)/(b+d)):.2f} vs original"
    )

with col2:
    st.metric(
        label="Tasa de Interés de Equilibrio (r*)",
        value=f"{r_eq:.2f}%",
        delta=f"{r_eq - (a_base - b*((a_base-c_base)/(b+d))):.2f}% vs original"
    )

# ───────────────────────────────────────────────────────────────
# Crear la gráfica
# ─────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 7))

# Grid
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_axisbelow(True)

# Curva IS
ax.plot(Y, r_IS, 'b-', linewidth=2.5, label=f'IS (Bienes) [Δ={delta_IS:+.1f}]')

# Curva LM
ax.plot(Y, r_LM, 'r-', linewidth=2.5, label=f'LM (Dinero) [Δ={delta_LM:+.1f}]')

# Punto de equilibrio
ax.plot(Y_eq, r_eq, 'ko', markersize=10, markeredgecolor='black', 
        markerfacecolor='gold', markeredgewidth=2)

# Etiquetas del punto de equilibrio
ax.annotate(f'Eq. (Y={Y_eq:.1f}, r={r_eq:.1f})', 
            xy=(Y_eq, r_eq), 
            xytext=(Y_eq + 0.5, r_eq + 0.5),
            fontsize=10, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# Configuración de ejes
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xlabel('Ingreso / Producto (Y)', fontsize=12, fontweight='bold')
ax.set_ylabel('Tasa de Interés (r)', fontsize=12, fontweight='bold')
ax.set_title('Modelo IS-LM (Interactivo)', fontsize=14, fontweight='bold', pad=20)

# Leyenda
ax.legend(loc='upper right', fontsize=10, framealpha=0.9)

# Líneas punteadas desde el equilibrio
ax.axhline(y=r_eq, color='gray', linestyle=':', alpha=0.5)
ax.axvline(x=Y_eq, color='gray', linestyle=':', alpha=0.5)

plt.tight_layout()

# ───────────────────────────────────────────────────────────────
# Mostrar gráfica en Streamlit
# ──────────────────────────────────────────────────────────────
st.pyplot(fig)

# ───────────────────────────────────────────────────────────────
# Explicación económica
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📚 Interpretación Económica")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Curva IS (Bienes):**")
    if delta_IS > 0:
        st.info(f"✅ Desplazamiento **positivo** de {delta_IS:+.1f}\n\n"
                "Política fiscal **expansiva** o aumento del gasto autónomo")
    elif delta_IS < 0:
        st.warning(f"⬇️ Desplazamiento **negativo** de {delta_IS:+.1f}\n\n"
                   "Política fiscal **contractiva** o disminución del gasto")
    else:
        st.success("➡️ Sin desplazamiento (posición original)")

with col2:
    st.markdown("**Curva LM (Dinero):**")
    if delta_LM > 0:
        st.warning(f"️ Desplazamiento **positivo** de {delta_LM:+.1f}\n\n"
                   "Política monetaria **contractiva** o disminución de la oferta monetaria")
    elif delta_LM < 0:
        st.info(f"✅ Desplazamiento **negativo** de {delta_LM:+.1f}\n\n"
                "Política monetaria **expansiva** o aumento de la oferta monetaria")
    else:
        st.success("️ Sin desplazamiento (posición original)")

# ───────────────────────────────────────────────────────────────
# Ecuaciones
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📐 Ecuaciones del Modelo")

col1, col2 = st.columns(2)

with col1:
    st.latex(rf"\text{{IS: }} r = {a_actual:.1f} - {b}Y")

with col2:
    st.latex(rf"\text{{LM: }} r = {c_actual:.1f} + {d}Y")

st.markdown(f"""
**Punto de equilibrio:**
- Y* = {Y_eq:.2f}
- r* = {r_eq:.2f}
""")
