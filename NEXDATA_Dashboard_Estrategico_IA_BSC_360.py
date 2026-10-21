import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime, timezone

st.set_page_config(page_title="NEXDATA | Dashboard Estratégico IA", page_icon="🧠", layout="wide")

NAVY="#0B1F3A"; BLUE="#2563EB"; CYAN="#00B8D9"; GREEN="#20C997"; ORANGE="#FFB020"; RED="#EF476F"; BG="#F5F7FB"; TEXT="#172B4D"

# ---------- PROFESSIONAL CHART SYSTEM ----------
CHART_COLORS = {
    "Marketing": "#4F7CFF",                 # electric blue
    "RR. HH.": "#8B5CF6",                  # violet
    "Finanzas": "#2DD4BF",                 # mint
    "Operaciones / Logística": "#21B8D7",  # cyan
    "Dirección": "#F2B84B",                 # amber
}
CHART_SEQUENCE = ["#4F7CFF","#8B5CF6","#2DD4BF","#21B8D7","#F2B84B","#F0648A"]

def professional_chart(fig, height=390, showlegend=True):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Inter, Arial, sans-serif", color="#17243B", size=12),
        title=dict(font=dict(family="Inter, Arial, sans-serif", size=18, color="#0B1F3A"), x=0.02, xanchor="left"),
        margin=dict(l=55, r=30, t=70, b=55),
        showlegend=showlegend,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            bgcolor="rgba(255,255,255,0)", font=dict(color="#5F7088", size=11)
        ),
        hoverlabel=dict(bgcolor="#0B1F3A", bordercolor="#0B1F3A", font=dict(color="white", family="Inter")),
        bargap=0.32,
    )
    fig.update_xaxes(showgrid=False, linecolor="#DCE5F0", tickfont=dict(color="#6F8097", size=11), title_font=dict(color="#52647B"))
    fig.update_yaxes(gridcolor="#EAF0F6", gridwidth=1, zeroline=False, linecolor="#DCE5F0",
                     tickfont=dict(color="#6F8097", size=11), title_font=dict(color="#52647B"))
    return fig

st.markdown(f"""
<style>
:root {{
 --navy:#071426; --navy2:#0B1F3A; --blue:#2563EB; --cyan:#00B8D9;
 --green:#20C997; --orange:#FFB020; --red:#EF476F; --bg:#F4F7FB;
 --text:#172B4D; --muted:#6B7F99; --line:#DDE6F1;
}}
.stApp {{
 background:
 radial-gradient(circle at 92% 3%, rgba(0,184,217,.10), transparent 22rem),
 radial-gradient(circle at 7% 14%, rgba(37,99,235,.08), transparent 24rem),
 var(--bg);
 color:var(--text);
}}
.block-container {{padding-top:1.25rem; padding-bottom:3rem; max-width:1500px;}}
h1,h2,h3,h4,p,span,label {{color:var(--text);}}
h2 {{font-weight:800!important; letter-spacing:-.02em;}}
.hero {{
 position:relative; overflow:hidden;
 background:linear-gradient(125deg,#071426 0%,#0B1F3A 58%,#123B67 100%);
 border:1px solid rgba(255,255,255,.10); border-radius:22px;
 padding:27px 30px; margin-bottom:18px;
 box-shadow:0 16px 45px rgba(7,20,38,.18);
}}
.hero:after {{
 content:""; position:absolute; width:260px;height:260px;border-radius:50%;
 right:-80px;top:-125px;background:radial-gradient(circle,rgba(0,184,217,.35),transparent 68%);
}}
.hero h1 {{margin:6px 0 0;color:white!important;font-size:32px;letter-spacing:-.03em;}}
.hero p {{margin:8px 0 0;color:#C8D8EC!important;max-width:1050px;}}
.hero .badge {{background:rgba(0,184,217,.13);color:#75E7FA!important;border:1px solid rgba(117,231,250,.25)}}
.card {{
 background:rgba(255,255,255,.94);border:1px solid var(--line);border-radius:18px;
 padding:19px;height:100%;box-shadow:0 7px 24px rgba(11,31,58,.055);
}}
.card:hover {{transform:translateY(-2px);box-shadow:0 11px 28px rgba(11,31,58,.09);transition:.18s ease;}}
.small {{font-size:13px;color:var(--muted)!important;line-height:1.55;}}
.kpi {{font-size:27px;font-weight:800;color:var(--navy2)!important;}}
.badge {{display:inline-block;background:#EAF2FF;color:var(--blue)!important;padding:5px 10px;border-radius:20px;font-weight:750;font-size:12px}}
.flow {{
 background:linear-gradient(180deg,#FFFFFF,#F8FBFF);border:1px solid #DCE7F4;
 border-top:3px solid var(--blue);border-radius:15px;padding:14px 9px;text-align:center;
 font-weight:750;color:var(--navy2)!important;min-height:72px;display:flex;align-items:center;justify-content:center;
 box-shadow:0 4px 13px rgba(11,31,58,.04);
}}
.ai {{
 background:linear-gradient(120deg,#ECF8FF,#F4F1FF);border:1px solid #CFE9FA;
 border-left:5px solid var(--blue);padding:20px 22px;border-radius:15px;color:var(--text);
 box-shadow:0 6px 20px rgba(37,99,235,.07);
}}
div[data-testid="stMetric"] {{
 background:rgba(255,255,255,.96);border:1px solid var(--line);padding:16px 17px;border-radius:17px;
 box-shadow:0 6px 18px rgba(11,31,58,.05);
}}
div[data-testid="stMetric"] label {{color:#61758F!important;font-weight:650!important;}}
div[data-testid="stMetricValue"] {{color:var(--navy2)!important;font-weight:850!important;}}
div[data-baseweb="tab-list"] {{
 gap:7px;background:#EAF0F7;padding:6px;border-radius:15px;overflow-x:auto;
}}
button[data-baseweb="tab"] {{
 background:transparent;border-radius:10px;padding:8px 13px;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
 background:white;box-shadow:0 3px 10px rgba(11,31,58,.09);
}}
button[data-baseweb="tab"] p {{font-weight:700!important;}}
[data-testid="stDataFrame"] {{border:1px solid var(--line);border-radius:14px;overflow:hidden;}}
[data-testid="stAlert"] {{border-radius:14px;}}
hr {{border-color:#E2EAF3!important;}}
</style>
""", unsafe_allow_html=True)

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif}
.stApp{background:radial-gradient(circle at 88% 3%,rgba(78,124,255,.11),transparent 24rem),radial-gradient(circle at 8% 14%,rgba(34,211,238,.08),transparent 24rem),#F4F7FC}
h1,h2,h3{font-family:'Space Grotesk','Inter',sans-serif!important;letter-spacing:-.03em}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#061321 0%,#0A1E34 58%,#0D2B49 100%);border-right:1px solid rgba(255,255,255,.06)}
[data-testid="stSidebar"] *{color:#DCEBFA!important}
.hero{background:linear-gradient(120deg,#061321 0%,#102B4A 55%,#16466E 100%)!important;border-radius:26px!important;padding:32px!important;box-shadow:0 20px 52px rgba(7,20,38,.20)!important}
.hero h1{font-family:'Space Grotesk'!important;font-size:36px!important}
.card{border-radius:20px!important;box-shadow:0 9px 30px rgba(18,45,75,.06)!important;border:1px solid #E1E8F2!important}
.card:hover{transform:translateY(-4px)!important;box-shadow:0 16px 34px rgba(18,45,75,.10)!important}
.flow{border-radius:16px!important;border-top:3px solid #4F7CFF!important;box-shadow:0 6px 18px rgba(18,45,75,.05)!important}
.ai{background:linear-gradient(120deg,#EEF4FF,#EEFBFF 48%,#F6F0FF)!important;border:1px solid #D6E4FA!important;border-left:5px solid #8B5CF6!important;border-radius:18px!important}
div[data-testid="stMetric"]{border-radius:18px!important;box-shadow:0 8px 24px rgba(18,45,75,.055)!important;border:1px solid #E1E8F2!important}
div[data-testid="stMetricValue"]{font-family:'Space Grotesk'!important;color:#0A1E34!important}
div[data-baseweb="tab-list"]{background:#E9EFF7!important;padding:7px!important;border-radius:16px!important;gap:5px!important}
button[data-baseweb="tab"]{border-radius:11px!important;padding:9px 13px!important}
button[data-baseweb="tab"][aria-selected="true"]{background:white!important;box-shadow:0 4px 12px rgba(18,45,75,.10)!important}
[data-testid="stPlotlyChart"]{background:white;border:1px solid #E1E8F2;border-radius:20px;padding:8px;box-shadow:0 8px 24px rgba(18,45,75,.045)}
[data-testid="stDataFrame"]{border:1px solid #E1E8F2;border-radius:16px;overflow:hidden}
</style>
''', unsafe_allow_html=True)


st.markdown("""<div class="hero">
<span class="badge">DASHBOARD IA · SISTEMA DE GESTIÓN ESTRATÉGICA</span>
<h1>NEXDATA Intelligence Strategy Hub</h1>
<p>Visión + Misión + Valores → Objetivos y Metas → Indicadores → Acciones / Entregables → Cronograma → Presupuesto. Integrado con el Modelo de Negocio, herramientas de Dirección Estratégica y las 4 funciones claves de la gestión.</p>
</div>""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div style='font-size:27px;font-weight:800;color:white'>◈ NEXDATA</div><div style='font-size:11px;letter-spacing:.15em;color:#6FE8FF;margin-bottom:18px'>STRATEGY AI</div>", unsafe_allow_html=True)
    st.caption("PLAN ESTRATÉGICO · SISTEMA DE GESTIÓN")
tabs = st.tabs(["◈ Centro Estratégico", "◇ Modelo de negocio", "◎ Dirección estratégica", "⚙ Gestión", "▥ Objetivos & KPI", "◷ Cronograma", "◉ Presupuesto", "✦ Análisis IA", "✧ BSC Intelligence"])

areas = pd.DataFrame({
    "Área":["Marketing","RR. HH.","Finanzas","Operaciones / Logística"],
    "Objetivo":[
        "Posicionar NEXDATA y captar MYPES interesadas en soluciones de analítica de datos.",
        "Fortalecer las competencias del equipo para asegurar una gestión eficiente del servicio.",
        "Alcanzar sostenibilidad financiera mediante el control de ingresos, costos y presupuesto.",
        "Garantizar el funcionamiento eficiente, continuo y mejorable de la plataforma."
    ],
    "Meta":[
        "30 prospectos y 10 clientes en 6 meses",
        "100% del equipo con 2 capacitaciones en 6 meses",
        "Cubrir ≥100% de los costos operativos al mes 6",
        "Disponibilidad ≥95% y atención crítica ≤24 h"
    ],
    "KPI":["Tasa de conversión","% de personal capacitado","Cobertura de costos","Disponibilidad de plataforma"],
    "Fórmula":[
        "Clientes / Prospectos × 100",
        "Personal capacitado / Total × 100",
        "Ingresos / Costos × 100",
        "Horas disponibles / Horas totales × 100"
    ],
    "Meta_KPI":[33.0,100.0,100.0,95.0],
})

if "actuales" not in st.session_state:
    st.session_state.actuales={"Marketing":28.0,"RR. HH.":75.0,"Finanzas":82.0,"Operaciones / Logística":97.0}
if "presupuesto_ejecutado" not in st.session_state:
    st.session_state.presupuesto_ejecutado=1420

with tabs[0]:
    st.subheader("Resumen ejecutivo del sistema de gestión")
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="card"><b>VISIÓN</b><br><br>Ser una plataforma referente en analítica de datos para las MYPES peruanas, reconocida por facilitar la gestión empresarial mediante información clara, accesible y orientada a la toma de decisiones.</div>""",unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="card"><b>MISIÓN</b><br><br>Transformar los datos de las MYPES en información útil y comprensible mediante herramientas digitales que permitan analizar su desempeño, identificar oportunidades y tomar mejores decisiones empresariales.</div>""",unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="card"><b>CULTURA Y VALORES</b><br><br>Innovación · orientación al cliente · trabajo colaborativo · orientación a resultados · responsabilidad · mejora continua.</div>""",unsafe_allow_html=True)

    st.markdown("### Integración del Plan Estratégico")
    cols=st.columns(7)
    flow=["Modelo de negocio","Visión, misión y cultura","Dirección estratégica","Objetivos + metas","KPI + acciones","Cronograma + presupuesto","Control + decisiones"]
    for col,label in zip(cols,flow):
        with col: st.markdown(f'<div class="flow">{label}</div>',unsafe_allow_html=True)

    vals=[]
    for _,r in areas.iterrows():
        actual=st.session_state.actuales[r["Área"]]
        vals.append(min(actual/r["Meta_KPI"]*100,100))
    cumplimiento=sum(vals)/len(vals)
    k1,k2,k3,k4=st.columns(4)
    k1.metric("Cumplimiento estratégico",f"{cumplimiento:.0f}%")
    k2.metric("Objetivos en meta",f"{sum(st.session_state.actuales[r['Área']]>=r['Meta_KPI'] for _,r in areas.iterrows())}/4")
    k3.metric("Presupuesto total","S/ 2,100")
    k4.metric("Presupuesto ejecutado",f"S/ {st.session_state.presupuesto_ejecutado:,.0f}")

    progress_df = areas[["Área","Meta_KPI"]].copy()
    progress_df["Actual"] = [st.session_state.actuales[a] for a in progress_df["Área"]]
    progress_df["Cumplimiento"] = (progress_df["Actual"] / progress_df["Meta_KPI"] * 100).clip(upper=120)
    fig = go.Figure()
    fig.add_bar(
        y=progress_df["Área"], x=progress_df["Cumplimiento"], orientation="h",
        marker=dict(color=[CHART_COLORS[a] for a in progress_df["Área"]], line=dict(width=0)),
        text=[f"{v:.0f}%" for v in progress_df["Cumplimiento"]],
        textposition="inside", insidetextanchor="end",
        textfont=dict(color="white", size=12),
        hovertemplate="<b>%{y}</b><br>Cumplimiento: %{x:.1f}%<extra></extra>"
    )
    fig.add_vline(x=100, line_width=2, line_dash="dot", line_color="#9AA9BC",
                  annotation_text="META", annotation_position="top")
    fig.update_layout(title="Cumplimiento por área estratégica", xaxis_title="% de cumplimiento", yaxis_title="")
    st.plotly_chart(professional_chart(fig, 360, False), use_container_width=True, config={"displayModeBar":False})

with tabs[1]:
    st.subheader("Modelo de negocio NEXDATA — Business Model Canvas")
    canvas=[
        ("Socios clave","Proveedores tecnológicos, servicios cloud, aliados empresariales y organizaciones vinculadas con MYPES."),
        ("Actividades clave","Desarrollo y mantenimiento de la plataforma, análisis de datos, soporte, captación y mejora continua."),
        ("Recursos clave","Plataforma web, infraestructura tecnológica, conocimiento analítico, equipo y base de usuarios."),
        ("Propuesta de valor","Convertir datos empresariales en información visual, comprensible y útil para que las MYPES tomen mejores decisiones."),
        ("Relación con clientes","Acompañamiento digital, soporte, demostraciones, capacitación y atención continua."),
        ("Canales","Plataforma web, redes sociales, contacto digital, demostraciones y alianzas."),
        ("Segmentos de clientes","MYPES que necesitan analizar ventas, rentabilidad y desempeño sin contar con herramientas avanzadas de BI."),
        ("Estructura de costos","Desarrollo, hosting, herramientas digitales, marketing, soporte y capacitación."),
        ("Fuentes de ingresos","Planes de suscripción y servicios asociados a funcionalidades y análisis de la plataforma.")
    ]
    canvas_icons=["🤝","⚡","◆","✦","💬","◉","👥","▦","↗"]
    canvas_classes=["c-blue","c-cyan","c-violet","c-mint","c-amber","c-blue","c-violet","c-rose","c-mint"]
    for i in range(0,len(canvas),3):
        cc=st.columns(3)
        for j,(title,body) in enumerate(canvas[i:i+3]):
            ix=i+j
            with cc[j]:
                st.markdown(f"""<div class="dynamic-grid-card {canvas_classes[ix]}">
                <div class="dynamic-icon">{canvas_icons[ix]}</div>
                <div class="dynamic-number">BMC · {ix+1:02d}</div>
                <h4>{title}</h4><p>{body}</p></div>""",unsafe_allow_html=True)

with tabs[2]:
    st.subheader("Diagnóstico FODA y decisiones estratégicas de NEXDATA")
    st.caption("Diagnóstico propuesto para la etapa de desarrollo y validación comercial; no representa resultados de un estudio de mercado.")
    foda_items=[
        ("✦","FORTALEZAS","NEXDATA ya permite cargar Excel/CSV, visualizar ventas y rentabilidad y simular escenarios.","Mostrar un caso de uso realista de una MYPE y demostrar que el análisis es fácil de utilizar.","Marketing","c-mint"),
        ("↗","OPORTUNIDADES","Las MYPES pueden beneficiarse de digitalizar su información y medir sus resultados.","Realizar demostraciones y una prueba piloto con negocios interesados.","Marketing","c-blue"),
        ("△","DEBILIDADES","La plataforma está en desarrollo; faltan validación comercial, retroalimentación de usuarios y ajustes.","Registrar incidencias, entrevistar usuarios piloto y priorizar mejoras de usabilidad.","Operaciones / Logística","c-amber"),
        ("!","AMENAZAS","Existen herramientas BI consolidadas y resistencia de algunos negocios a adoptar soluciones nuevas.","Diferenciar NEXDATA por simplicidad, soporte y enfoque en MYPES; ofrecer una capacitación inicial.","Dirección / Marketing","c-rose"),
    ]
    cards=st.columns(2)
    for i,(icon,title,diagnostico,accion,area,color) in enumerate(foda_items):
        with cards[i%2]:
            st.markdown(f"""<div class="dynamic-grid-card {color}" style="min-height:235px">
            <div class="dynamic-icon">{icon}</div><h4>{title}</h4>
            <p><b>Situación NEXDATA:</b> {diagnostico}</p><br>
            <p><b>Respuesta estratégica:</b> {accion}</p><br>
            <div class="dynamic-number">Responsable: {area}</div></div>""",unsafe_allow_html=True)
    st.markdown("### De la matriz FODA a la ejecución")
    decisiones=pd.DataFrame([
        ["FO · Crecimiento","Aprovechar las funciones de análisis para captar MYPES","Demostraciones y campañas digitales","Marketing","Tasa de conversión","30 prospectos y 10 clientes / 6 meses"],
        ["DO · Validación","Reducir incertidumbre del producto con usuarios piloto","Pruebas, entrevistas y mejoras","Operaciones","Disponibilidad de plataforma","≥95%"],
        ["FA · Diferenciación","Competir mediante sencillez y acompañamiento","Tutoriales y demostraciones guiadas","Marketing / RR. HH.","Tasa de conversión / capacitación","33% / 100%"],
        ["DA · Sostenibilidad","Controlar costos mientras se mejora la plataforma","Flujo de caja y revisión mensual","Finanzas","Cobertura de costos","≥100% al mes 6"]
    ],columns=["Estrategia","Decisión para NEXDATA","Acción / entregable","Responsable","KPI asociado","Meta"])
    st.dataframe(decisiones,use_container_width=True,hide_index=True)
    st.markdown("""<div class="strategy-ribbon"><b>Integración estratégica</b><br><br>
    <span class="flow-chip">Canvas: valor para MYPES</span> ›
    <span class="flow-chip">FODA: diagnóstico NEXDATA</span> ›
    <span class="flow-chip">Estrategias FO / DO / FA / DA</span> ›
    <span class="flow-chip">Acciones por área</span> ›
    <span class="flow-chip">KPI y control</span></div>""",unsafe_allow_html=True)

with tabs[3]:
    st.subheader("Las 4 funciones de gestión ejecutadas en NEXDATA")
    st.caption("Cada función incluye qué hará el equipo, quién responde, qué se entregará y cómo se comprobará.")
    funciones=[
        ("01 · PLANIFICACIÓN","Definir el lanzamiento piloto: captar 30 prospectos, convertir 10 clientes y lograr cobertura de costos al mes 6.","Dirección + Marketing + Finanzas","Plan de captación, metas por área, cronograma de seis meses y presupuesto de S/ 2,100.","Metas y presupuesto aprobados","c-blue"),
        ("02 · ORGANIZACIÓN","Asignar Marketing a captación; RR. HH. a formación; Finanzas a flujo de caja; Operaciones a pruebas y disponibilidad.","Responsables de las cuatro áreas","Matriz de responsables, recursos asignados y calendario de actividades.","100% de actividades con responsable","c-cyan"),
        ("03 · DIRECCIÓN / EJECUCIÓN","Lanzar campañas, demostrar el dashboard a MYPES, capacitar al equipo y corregir errores reportados en pruebas.","Dirección y líderes de área","Campañas, registro de demostraciones, actas de capacitación y versión mejorada.","Conversión, capacitación y disponibilidad","c-violet"),
        ("04 · CONTROL Y MEJORA","Comparar mensualmente los KPI reales con las metas; si RR. HH. llega solo a 75%, reprogramar la capacitación pendiente.","Dirección + responsables de KPI","Semáforo, reporte de desviaciones, decisiones correctivas y seguimiento.","4 KPI monitoreados cada mes","c-mint"),
    ]
    cols=st.columns(2)
    for i,(title,accion,responsable,entregable,control,color) in enumerate(funciones):
        with cols[i%2]:
            st.markdown(f"""<div class="dynamic-grid-card {color}" style="min-height:260px">
            <div class="dynamic-number">FUNCIÓN {i+1:02d}</div><h4>{title}</h4>
            <p><b>Aplicación:</b> {accion}</p><br>
            <p><b>Responsables:</b> {responsable}</p><br>
            <p><b>Entregable:</b> {entregable}</p><br>
            <p><b>Control:</b> {control}</p></div>""",unsafe_allow_html=True)
    st.markdown("### Ejemplo de decisión correctiva")
    st.info("Si el indicador de capacitación marca 75% frente a una meta de 100%, Dirección encarga a RR. HH. programar la capacitación faltante, registrar la asistencia y revisar nuevamente el KPI el mes siguiente.")
    st.markdown("""<div class="management-loop"><b>Ciclo de gestión aplicado a NEXDATA</b><br><br>
    <span class="loop-step" style="background:#4F7CFF">PLANIFICAR METAS</span> →
    <span class="loop-step" style="background:#16B9D4">ASIGNAR RESPONSABLES</span> →
    <span class="loop-step" style="background:#8B5CF6">EJECUTAR CAMPAÑAS Y MEJORAS</span> →
    <span class="loop-step" style="background:#19B99F">MEDIR KPI</span> →
    <span class="loop-step" style="background:#D99518">CORREGIR DESVIACIONES</span></div>""",unsafe_allow_html=True)

with tabs[4]:
    st.subheader("Objetivos estratégicos, metas e indicadores")
    st.dataframe(areas[["Área","Objetivo","Meta","KPI","Fórmula"]],use_container_width=True,hide_index=True)
    st.markdown("### Simulación de avance de KPI")
    cols=st.columns(4)
    ranges={"Marketing":100,"RR. HH.":100,"Finanzas":160,"Operaciones / Logística":100}
    for col,(_,r) in zip(cols,areas.iterrows()):
        with col:
            st.session_state.actuales[r["Área"]] = st.slider(
                r["Área"],0.0,float(ranges[r["Área"]]),float(st.session_state.actuales[r["Área"]]),1.0,
                help=f"{r['KPI']} | Meta: {r['Meta_KPI']}"
            )
            actual=st.session_state.actuales[r["Área"]]
            estado="🟢 Cumple" if actual>=r["Meta_KPI"] else ("🟡 En riesgo" if actual>=r["Meta_KPI"]*.75 else "🔴 Crítico")
            st.caption(f"{r['KPI']}: {actual:.1f}% · Meta {r['Meta_KPI']:.0f}%")
            st.write(estado)

    st.markdown("### Acciones y entregables vinculados a la estrategia NEXDATA")
    actions=pd.DataFrame([
        ["Marketing","Campañas digitales y contenido educativo","Plan de contenidos + piezas digitales","Marketing"],
        ["Marketing","Demostraciones y prueba piloto","Base de prospectos + reporte de captación","Marketing"],
        ["RR. HH.","Capacitación en datos y atención","Plan y registro de capacitación","RR. HH."],
        ["Finanzas","Control mensual de ingresos y costos","Reporte financiero y flujo de caja","Finanzas"],
        ["Operaciones / Logística","Pruebas y corrección de incidencias","Registro de incidencias","Tecnología"],
        ["Operaciones / Logística","Mejoras funcionales de la plataforma","Versión optimizada de NEXDATA","Tecnología"],
    ],columns=["Área","Acción","Entregable","Responsable"])
    actions["Relación estratégica"]=["FO · Captación","FO · Prueba piloto","FA · Diferenciación","DA · Sostenibilidad","DO · Validación","DO · Mejora"]
    st.dataframe(actions,use_container_width=True,hide_index=True)
    st.caption("Cada acción responde a un hallazgo FODA y aporta al seguimiento de los KPI.")

with tabs[5]:
    st.subheader("Cronograma estratégico")
    cron=pd.DataFrame([
        ["Optimización de plataforma","Operaciones / Logística","2026-10-01","2026-11-30"],
        ["Pruebas de funcionamiento","Operaciones / Logística","2026-10-15","2026-12-15"],
        ["Capacitación del equipo","RR. HH.","2026-11-01","2027-02-28"],
        ["Contenido y campaña digital","Marketing","2026-10-15","2027-03-31"],
        ["Captación de MYPES","Marketing","2026-11-01","2027-03-31"],
        ["Seguimiento financiero","Finanzas","2026-10-01","2027-03-31"],
        ["Evaluación de indicadores","Dirección","2026-12-15","2027-03-31"],
    ],columns=["Actividad","Área","Inicio","Fin"])
    cron["Inicio"]=pd.to_datetime(cron["Inicio"]); cron["Fin"]=pd.to_datetime(cron["Fin"])
    fig=px.timeline(
        cron,x_start="Inicio",x_end="Fin",y="Actividad",color="Área",
        color_discrete_map=CHART_COLORS,
        title="Roadmap estratégico · Oct. 2026 — Mar. 2027"
    )
    fig.update_traces(marker_line_width=0, opacity=.92)
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(professional_chart(fig, 470, True),use_container_width=True,config={"displayModeBar":False})
    st.dataframe(cron,use_container_width=True,hide_index=True)

with tabs[6]:
    st.subheader("Presupuesto estratégico")
    budget=pd.DataFrame({
        "Concepto":["Desarrollo y mejoras","Hosting y herramientas","Marketing y publicidad","Capacitación","Pruebas y soporte","Contingencias"],
        "Presupuesto":[500,300,600,300,200,200]
    })
    st.session_state.presupuesto_ejecutado=st.slider("Presupuesto ejecutado (S/)",0,2100,int(st.session_state.presupuesto_ejecutado),50)
    b1,b2,b3=st.columns(3)
    b1.metric("Presupuesto planificado","S/ 2,100")
    b2.metric("Ejecutado",f"S/ {st.session_state.presupuesto_ejecutado:,}")
    b3.metric("Disponible",f"S/ {2100-st.session_state.presupuesto_ejecutado:,}")
    fig=px.bar(
        budget,x="Concepto",y="Presupuesto",text="Presupuesto",
        title="Distribución del presupuesto",
        color="Concepto", color_discrete_sequence=CHART_SEQUENCE
    )
    fig.update_traces(
        texttemplate="S/ %{text:,.0f}", textposition="outside",
        marker_line_width=0, hovertemplate="<b>%{x}</b><br>S/ %{y:,.0f}<extra></extra>"
    )
    st.plotly_chart(professional_chart(fig, 390, False),use_container_width=True,config={"displayModeBar":False})
    st.dataframe(budget,use_container_width=True,hide_index=True)

with tabs[7]:
    st.subheader("🤖 Análisis estratégico automatizado de NEXDATA")
    st.caption("Las recomendaciones se generan mediante reglas según los KPI simulados; no se conectan a un modelo generativo.")
    gaps=[]
    for _,r in areas.iterrows():
        actual=st.session_state.actuales[r["Área"]]
        gap=(actual-r["Meta_KPI"])/r["Meta_KPI"]*100
        gaps.append((r["Área"],gap,actual,r["Meta_KPI"],r["KPI"]))
    worst=min(gaps,key=lambda x:x[1])
    best=max(gaps,key=lambda x:x[1])
    cumplimiento=sum(min(st.session_state.actuales[r["Área"]]/r["Meta_KPI"]*100,100) for _,r in areas.iterrows())/4
    recs={
        "Marketing":"reforzar las demostraciones, contenido educativo y seguimiento de prospectos para elevar la conversión.",
        "RR. HH.":"completar el plan de capacitación y verificar la aplicación de los conocimientos en las actividades del equipo.",
        "Finanzas":"revisar costos operativos y priorizar acciones que incrementen los ingresos recurrentes.",
        "Operaciones / Logística":"priorizar incidencias críticas, monitorear disponibilidad y mantener un ciclo de mejora continua."
    }
    st.markdown(f"""<div class="ai"><b>Diagnóstico automático</b><br><br>
El Plan Estratégico registra un cumplimiento aproximado de <b>{cumplimiento:.0f}%</b>. 
El área con mayor desviación relativa es <b>{worst[0]}</b>, con un resultado actual de <b>{worst[2]:.1f}%</b> frente a una meta de <b>{worst[3]:.0f}%</b>.
El mejor desempeño relativo corresponde a <b>{best[0]}</b>.<br><br>
<b>Recomendación IA:</b> Se recomienda {recs[worst[0]]}
El resultado debe revisarse periódicamente para retroalimentar la planificación y aplicar acciones correctivas.</div>""",unsafe_allow_html=True)

    st.markdown("### Semáforo estratégico")
    sem=[]
    for _,r in areas.iterrows():
        actual=st.session_state.actuales[r["Área"]]
        ratio=actual/r["Meta_KPI"]
        estado="🟢 Cumple" if ratio>=1 else ("🟡 En riesgo" if ratio>=.75 else "🔴 Crítico")
        sem.append([r["Área"],r["KPI"],f"{actual:.1f}%",f"{r['Meta_KPI']:.0f}%",estado])
    st.dataframe(pd.DataFrame(sem,columns=["Área","KPI","Actual","Meta","Estado"]),use_container_width=True,hide_index=True)


st.markdown("""
<style>
/* HIGH CONTRAST HERO */
div.hero {
  background:
    radial-gradient(circle at 90% 15%, rgba(34,211,238,.34), transparent 24%),
    radial-gradient(circle at 70% 115%, rgba(139,92,246,.38), transparent 30%),
    linear-gradient(120deg,#071426 0%,#102B52 52%,#164B73 100%) !important;
  border:1px solid rgba(255,255,255,.14) !important;
}
div.hero h1, div.hero h1 * {
  color:#FFFFFF !important;
  -webkit-text-fill-color:#FFFFFF !important;
  opacity:1 !important;
  text-shadow:0 2px 18px rgba(0,0,0,.20);
}
div.hero p, div.hero p * {color:#E8F4FF !important;}
div.hero .badge, div.hero .badge * {
  color:#79F0FF !important;
  background:rgba(0,210,255,.12) !important;
  border-color:rgba(121,240,255,.32) !important;
}

/* MORE COLOR, WITHOUT LOSING READABILITY */
.card:nth-of-type(3n+1){border-top:4px solid #4F7CFF !important}
.card:nth-of-type(3n+2){border-top:4px solid #21D4FD !important}
.card:nth-of-type(3n+3){border-top:4px solid #8B5CF6 !important}
div[data-testid="stMetric"]:nth-of-type(4n+1){border-top:4px solid #4F7CFF !important}
div[data-testid="stMetric"]:nth-of-type(4n+2){border-top:4px solid #2DD4BF !important}
div[data-testid="stMetric"]:nth-of-type(4n+3){border-top:4px solid #8B5CF6 !important}
div[data-testid="stMetric"]:nth-of-type(4n+4){border-top:4px solid #F6B84A !important}

/* Tabs: stronger active state */
button[data-baseweb="tab"][aria-selected="true"]{
  background:linear-gradient(135deg,#4F7CFF,#6E5CF6) !important;
}
button[data-baseweb="tab"][aria-selected="true"] p{
  color:#FFFFFF !important;
}

/* Section titles */
.block-container h2{
  color:#0B1F3A !important;
  font-weight:800 !important;
}
.block-container h3{
  color:#173B69 !important;
  font-weight:750 !important;
}

/* Data + charts */
[data-testid="stPlotlyChart"]{
  border-top:4px solid #21D4FD !important;
  background:linear-gradient(180deg,#FFFFFF,#FBFDFF) !important;
}
.ai{
  background:linear-gradient(125deg,#EDF4FF 0%,#EBFCFF 45%,#F6EFFF 100%) !important;
  border-left:6px solid #8B5CF6 !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
[data-testid="stPlotlyChart"]{
    background:linear-gradient(180deg,#FFFFFF 0%,#FBFCFF 100%) !important;
    border:1px solid #E1E8F2 !important;
    border-top:0 !important;
    border-radius:20px !important;
    padding:12px 14px 8px !important;
    box-shadow:0 10px 30px rgba(17,38,67,.055) !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* ===== ELEVATED STRATEGIC MODULES ===== */
.dynamic-grid-card{
    position:relative; overflow:hidden; min-height:190px;
    background:linear-gradient(145deg,#FFFFFF 0%,#F8FBFF 100%);
    border:1px solid #E1E8F2; border-radius:22px; padding:22px;
    box-shadow:0 12px 32px rgba(18,45,75,.07);
    transition:transform .22s ease, box-shadow .22s ease;
}
.dynamic-grid-card:hover{transform:translateY(-6px);box-shadow:0 20px 40px rgba(18,45,75,.13)}
.dynamic-grid-card:after{
    content:""; position:absolute; width:115px;height:115px;border-radius:50%;
    right:-45px;top:-45px;background:var(--glow);opacity:.16;
}
.dynamic-icon{
    width:42px;height:42px;border-radius:13px;display:flex;align-items:center;justify-content:center;
    font-size:20px;margin-bottom:14px;background:var(--soft);color:var(--accent)!important;
}
.dynamic-number{font-size:11px;font-weight:850;letter-spacing:.12em;color:var(--accent)!important;text-transform:uppercase}
.dynamic-grid-card h4{font-size:17px!important;margin:6px 0 8px;color:#0B1F3A!important}
.dynamic-grid-card p{font-size:13px!important;line-height:1.6;color:#61758F!important;margin:0}
.c-blue{--accent:#4F7CFF;--soft:#EDF2FF;--glow:#4F7CFF;border-top:4px solid #4F7CFF}
.c-cyan{--accent:#16B9D4;--soft:#E9FAFD;--glow:#21D4FD;border-top:4px solid #21D4FD}
.c-violet{--accent:#8B5CF6;--soft:#F3EEFF;--glow:#8B5CF6;border-top:4px solid #8B5CF6}
.c-mint{--accent:#19B99F;--soft:#EAFBF7;--glow:#2DD4BF;border-top:4px solid #2DD4BF}
.c-amber{--accent:#D99518;--soft:#FFF7E6;--glow:#F6B84A;border-top:4px solid #F6B84A}
.c-rose{--accent:#DF557A;--soft:#FFF0F4;--glow:#F0648A;border-top:4px solid #F0648A}

.strategy-ribbon{
 background:linear-gradient(110deg,#0B1F3A 0%,#173B69 48%,#245A82 100%);
 border-radius:20px;padding:19px 22px;color:white!important;box-shadow:0 12px 30px rgba(11,31,58,.15);
}
.strategy-ribbon *{color:white!important}
.flow-chip{
 display:inline-flex;align-items:center;padding:9px 13px;margin:5px 2px;border-radius:999px;
 font-size:12px;font-weight:750;background:rgba(255,255,255,.11);border:1px solid rgba(255,255,255,.16);
}
.flow-arrow2{color:#66E6F6!important;padding:0 3px;font-weight:900}

.foda-card{
 min-height:180px;border-radius:20px;padding:20px;color:white!important;
 box-shadow:0 12px 30px rgba(18,45,75,.11);transition:.2s ease;
}
.foda-card:hover{transform:translateY(-5px) scale(1.01)}
.foda-card *{color:white!important}
.foda-card h4{font-size:18px!important;margin:7px 0}
.foda-card p{font-size:13px!important;line-height:1.55;opacity:.92}
.f-strength{background:linear-gradient(145deg,#0E9F87,#2DD4BF)}
.f-opportunity{background:linear-gradient(145deg,#3566E8,#5B8CFF)}
.f-weakness{background:linear-gradient(145deg,#D68D13,#F6B84A)}
.f-threat{background:linear-gradient(145deg,#D94A70,#F0648A)}

.management-loop{
 background:linear-gradient(135deg,#0B1F3A,#153D68);border-radius:22px;padding:22px;
 color:white!important;box-shadow:0 15px 36px rgba(11,31,58,.16);margin-top:15px
}
.management-loop *{color:white!important}
.loop-step{
 display:inline-block;padding:10px 15px;margin:5px;border-radius:12px;font-size:12px;font-weight:800;
 border:1px solid rgba(255,255,255,.14)
}
</style>
""", unsafe_allow_html=True)

st.caption("NEXDATA · Dashboard IA del Plan Estratégico · Actividad académica")


# ============================================================
# BSC INTELLIGENCE — BALANCED SCORECARD NEXDATA
# ============================================================
@st.cache_data(ttl=86400, show_spinner=False)
def worldbank_peru_internet():
    """Live external World Bank WDI API; gracefully handles offline operation."""
    endpoint = "https://api.worldbank.org/v2/country/PER/indicator/IT.NET.USER.ZS"
    try:
        response = requests.get(endpoint, params={"format":"json", "per_page":25}, timeout=8,
                                headers={"User-Agent":"NEXDATA-academic-BSC/1.0"})
        response.raise_for_status()
        payload=response.json()
        records=payload[1] if isinstance(payload,list) and len(payload)>1 else []
        records=[{"Año":int(r["date"]),"Uso de internet (%)":float(r["value"])}
                 for r in records if r.get("value") is not None]
        records.sort(key=lambda x:x["Año"])
        if not records:
            return [], "La API respondió sin observaciones disponibles.", None
        return records, None, datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    except Exception as exc:
        return [], "No se pudo consultar la API del Banco Mundial en este momento.", None

BSC_COLORS=["#24E3C0","#54A0FF","#B17CFF","#FFBF69"]
BSC_NAMES=["Financiera","Clientes","Procesos internos","Aprendizaje y crecimiento"]
BSC_AREAS=["Finanzas","Marketing","Operaciones / Logística","RR. HH."]
BSC_GOALS=[100.,33.,95.,100.]
BSC_OBJECTIVES=[
    "Cubrir los costos operativos y sostener NEXDATA",
    "Captar 10 clientes de 30 prospectos en 6 meses",
    "Mantener la plataforma disponible y operativa",
    "Capacitar al 100% del equipo de NEXDATA",
]
BSC_ACTIONS=[
    "Control mensual de ingresos, costos y suscripciones",
    "Demostraciones, campañas y seguimiento a MYPES",
    "Pruebas piloto, monitoreo de servicio y corrección de incidencias",
    "Dos capacitaciones y verificación de competencias",
]
BSC_FODA=["DA · Sostenibilidad","FO · Crecimiento","DO · Validación","FA · Diferenciación"]

with tabs[8]:
    st.markdown("""<style>
    .bsc-hero{background:linear-gradient(110deg,#081329,#15264F 55%,#123D52);border:1px solid #35516D;
      border-radius:23px;padding:24px 27px;margin-bottom:18px;box-shadow:0 18px 38px rgba(6,19,41,.16)}
    .bsc-hero h2{color:#F6FAFF!important;margin:0;font-size:31px}
    .bsc-hero p{color:#C7E2F3!important;margin:8px 0 0}
    .bsc-pill{background:#10213D;border:1px solid #27435F;border-radius:17px;padding:15px 16px;margin:5px 0 13px}
    .bsc-pill small{color:#A5BCD8!important;font-size:12px}.bsc-pill strong{color:white!important;font-size:23px}
    .bsc-step{background:linear-gradient(120deg,#122443,#233C60);border:1px solid #365779;border-radius:14px;
      color:white!important;padding:15px;text-align:center;font-weight:750;min-height:82px}
    .bsc-step span{color:#D4E7FA!important;font-size:12px;font-weight:450}
    </style>""", unsafe_allow_html=True)
    st.markdown("""<div class='bsc-hero'><div style='color:#4BE7CE;letter-spacing:3px;font-size:12px;font-weight:800'>NEXDATA · STRATEGY INTELLIGENCE</div>
      <h2>✧ Balanced Scorecard 360°</h2><p>De la estrategia FODA a la ejecución medible · Cuatro perspectivas · Datos externos online · Simulación de decisiones</p></div>""",unsafe_allow_html=True)
    st.caption("Los KPI de NEXDATA son datos académicos simulados. Los datos del Banco Mundial son externos y se consultan online cuando hay conexión.")

    st.markdown("#### 🎛 Laboratorio de escenarios — modifica los indicadores")
    ctrl=st.columns(4)
    for idx,(col,area) in enumerate(zip(ctrl,BSC_AREAS)):
        with col:
            upper=160. if area=="Finanzas" else 100.
            st.session_state.actuales[area]=st.slider(BSC_NAMES[idx],0.,upper,
                float(st.session_state.actuales[area]),1.,key=f"bsc_slider_{idx}",
                help=f"{BSC_OBJECTIVES[idx]} | Meta {BSC_GOALS[idx]:.0f}%")
    actuals=[float(st.session_state.actuales[a]) for a in BSC_AREAS]
    ratios=[v/g*100 for v,g in zip(actuals,BSC_GOALS)]
    meets=sum(v>=g for v,g in zip(actuals,BSC_GOALS))
    bsc_avg=sum(min(r,100) for r in ratios)/4
    m1,m2,m3,m4=st.columns(4)
    for col,name,actual,goal,color in zip([m1,m2,m3,m4],BSC_NAMES,actuals,BSC_GOALS,BSC_COLORS):
        with col:
            st.markdown(f"<div class='bsc-pill'><small>{name.upper()}</small><br><strong style='color:{color}!important'>{actual:.0f}%</strong><br><small>Meta {goal:.0f}% · {'EN META' if actual>=goal else 'POR MEJORAR'}</small></div>",unsafe_allow_html=True)
    st.metric("Índice global de cumplimiento del BSC (promedio de cumplimiento de metas, tope 100%)",f"{bsc_avg:.1f}%",f"{meets} de 4 perspectivas en meta",delta_color="off")

    st.markdown("### ◉ Anillos de desempeño + radar estratégico")
    left,right=st.columns([1.05,1],gap="large")
    with left:
        rings=go.Figure()
        for i,(name,ratio,color) in enumerate(zip(BSC_NAMES,ratios,BSC_COLORS)):
            rings.add_trace(go.Indicator(mode="gauge+number",value=min(ratio,100),
                title={"text":name,"font":{"size":12,"color":"#C6D8F1"}},
                number={"suffix":"%","font":{"size":25,"color":"#FFFFFF"}},
                gauge={"axis":{"range":[0,100],"visible":False},"bar":{"color":color,"thickness":.23},
                       "bgcolor":"#1B2D4C","borderwidth":0},
                domain={"x":[(i%2)*.51,(i%2)*.51+.47],"y":[.53-(i//2)*.53,.98-(i//2)*.53]}))
        rings.update_layout(height=450,paper_bgcolor="#0A1931",font_color="white",margin=dict(l=20,r=20,t=24,b=14))
        st.plotly_chart(rings,use_container_width=True,key="bsc_rings",config={"displayModeBar":False})
    with right:
        labels=BSC_NAMES+[BSC_NAMES[0]]
        radar=go.Figure()
        radar.add_trace(go.Scatterpolar(r=[100]*5,theta=labels,name="Meta 100%",mode="lines",
                      line=dict(color="#9BA9BC",dash="dash",width=2)))
        radar.add_trace(go.Scatterpolar(r=[min(x,130) for x in ratios]+[min(ratios[0],130)],theta=labels,
                      name="Cumplimiento actual",fill="toself",line=dict(color="#23DCC8",width=4),
                      fillcolor="rgba(35,220,200,.28)",marker=dict(size=9,color="#B17CFF")))
        radar.update_layout(height=450,paper_bgcolor="#0A1931",font=dict(color="#DFEAFA",size=11),
            polar=dict(bgcolor="#0A1931",radialaxis=dict(visible=True,range=[0,135],gridcolor="#2B4462",tickfont=dict(color="#93ABC7")),
                       angularaxis=dict(gridcolor="#2B4462",tickfont=dict(color="#E5EFFF"))),
            legend=dict(orientation="h",y=-.1),margin=dict(l=58,r=58,t=32,b=64))
        st.plotly_chart(radar,use_container_width=True,key="bsc_radar",config={"displayModeBar":False})

    st.markdown("### ↝ Flujo Sankey — de la estrategia a los resultados")
    st.caption("Las conexiones son relaciones estratégicas propuestas, no flujos financieros medidos. El grosor representa ponderaciones ilustrativas.")
    nodes=["FODA: DA / sostenibilidad","FODA: FO / crecimiento","FODA: DO / validación","FODA: FA / diferenciación",
           "Finanzas","Marketing","Operaciones","RR. HH.","Cobertura de costos","Conversión de clientes","Disponibilidad","Capacitación"]
    sources=list(range(8));targets=list(range(4,12));values=[4,5,4,3,4,5,4,3]
    sankey=go.Figure(go.Sankey(arrangement="snap",node=dict(pad=21,thickness=19,label=nodes,
         color=["#526B9B"]*4+BSC_COLORS+BSC_COLORS,line=dict(color="#90A9C8",width=.5)),
         link=dict(source=sources,target=targets,value=values,color=["rgba(36,227,192,.27)","rgba(84,160,255,.27)","rgba(177,124,255,.27)","rgba(255,191,105,.27)"]*2)))
    sankey.update_layout(height=400,paper_bgcolor="#0D1C35",font=dict(color="white",size=12),margin=dict(l=18,r=20,t=18,b=18))
    st.plotly_chart(sankey,use_container_width=True,key="bsc_sankey",config={"displayModeBar":False})

    st.markdown("### ▦ Mapa de prioridades + matriz de impacto")
    a,b=st.columns(2,gap="large")
    priorities=[max(1,100-min(r,100)) for r in ratios]
    priority_df=pd.DataFrame({"Perspectiva":BSC_NAMES,"Brecha pendiente":priorities,
        "Cumplimiento":ratios,"Área":BSC_AREAS})
    with a:
        tree=go.Figure(go.Treemap(labels=BSC_NAMES,parents=[""]*4,values=[max(8,x) for x in priorities],
            marker=dict(colors=priorities,colorscale=[[0,"#1DCEAE"],[.45,"#FFD06A"],[1,"#F16D96"]],
                        line=dict(color="#0B1F3A",width=4)),
            texttemplate="<b>%{label}</b><br>Brecha: %{value:.1f} pp",textfont=dict(size=15,color="white"),
            hovertemplate="%{label}<br>Brecha al 100% de cumplimiento: %{value:.1f} pp<extra></extra>"))
        tree.update_layout(height=370,paper_bgcolor="#0C1B35",margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(tree,use_container_width=True,key="bsc_treemap",config={"displayModeBar":False})
        st.caption("El tamaño del bloque representa la brecha de cumplimiento (mínimo visual de 8 para mantener legibilidad).")
    with b:
        bubble_df=pd.DataFrame({"Área":BSC_NAMES,"Impacto":[8,9,8,7],"Esfuerzo":[6,7,5,4],
            "Urgencia":priorities,"color":BSC_COLORS})
        bubbles=go.Figure()
        for i,row in bubble_df.iterrows():
            bubbles.add_trace(go.Scatter(x=[row["Esfuerzo"]],y=[row["Impacto"]],mode="markers+text",
                name=row["Área"],text=[row["Área"]],textposition="top center",
                marker=dict(size=26+min(row["Urgencia"],100)*.72,color=row["color"],opacity=.75,line=dict(width=2,color="#F3F7FF")),
                hovertemplate=f"{row['Área']}<br>Impacto estimado: {row['Impacto']}/10<br>Esfuerzo estimado: {row['Esfuerzo']}/10<extra></extra>"))
        bubbles.update_layout(height=370,paper_bgcolor="#0C1B35",plot_bgcolor="#0C1B35",
            font=dict(color="#E7F0FF"),xaxis=dict(title="Esfuerzo estimado (1–10)",range=[1,10],gridcolor="#233A58"),
            yaxis=dict(title="Impacto estimado (1–10)",range=[1,10],gridcolor="#233A58"),
            legend=dict(orientation="h",y=-.38),margin=dict(l=45,r=18,t=22,b=85))
        st.plotly_chart(bubbles,use_container_width=True,key="bsc_bubbles",config={"displayModeBar":False})
        st.caption("Impacto y esfuerzo son estimaciones didácticas, no datos obtenidos de una investigación.")

    st.markdown("### 🌐 Señal externa online — digitalización en Perú")
    records,api_error,checked_at=worldbank_peru_internet()
    if records:
        df_external=pd.DataFrame(records)
        latest=df_external.iloc[-1]
        c1,c2=st.columns([1,3])
        with c1:
            st.metric("Uso de internet en Perú",f"{latest['Uso de internet (%)']:.1f}%",help="Último año disponible en la API; no mide directamente uso de BI por MYPES.")
            st.caption(f"Año del dato: {int(latest['Año'])} · Consultado: {checked_at}")
        with c2:
            fig=go.Figure(go.Scatter(x=df_external["Año"],y=df_external["Uso de internet (%)"],mode="lines+markers",
                fill="tozeroy",line=dict(color="#20DCC3",width=4,shape="spline"),
                fillcolor="rgba(32,220,195,.20)",marker=dict(size=8,color="#A57DFF"),
                hovertemplate="Año %{x}<br>Usuarios de internet: %{y:.1f}%<extra></extra>"))
            fig.update_layout(height=285,paper_bgcolor="#0B1B33",plot_bgcolor="#0B1B33",font=dict(color="#DCE9FC"),
                xaxis=dict(gridcolor="#253E5E",dtick=2),yaxis=dict(title="% de población",gridcolor="#253E5E",range=[0,100]),
                margin=dict(l=45,r=20,t=15,b=40))
            st.plotly_chart(fig,use_container_width=True,key="bsc_worldbank",config={"displayModeBar":False})
        st.success("Fuente online consultada: Banco Mundial, indicador IT.NET.USER.ZS. Los datos son contexto de digitalización, no métricas internas de NEXDATA.")
    else:
        st.warning(api_error+" El BSC y las simulaciones siguen funcionando sin internet.")
    st.markdown("**Fuentes y trazabilidad:** [API Banco Mundial — Perú, uso de internet](https://api.worldbank.org/v2/country/PER/indicator/IT.NET.USER.ZS?format=json) · [INEI](https://www.inei.gob.pe/) (consulta documental, sin conexión automática) · [Balanced Scorecard Institute](https://balancedscorecard.org/bsc-basics/) (referencia metodológica).")

    st.markdown("### ✦ Diagnóstico estratégico y decisiones recomendadas")
    weak=sorted(range(4),key=lambda i:ratios[i])
    corrective=[
        "Revisar costos fijos, evaluar suscripciones y controlar flujo de caja mensualmente.",
        "Incrementar demostraciones a MYPES y dar seguimiento a los prospectos.",
        "Revisar incidencias, hacer pruebas de disponibilidad y priorizar correcciones.",
        "Programar las capacitaciones pendientes y verificar su cumplimiento.",
    ]
    if ratios[weak[0]]>=100:
        st.success("Las cuatro perspectivas alcanzan sus metas en la simulación. Se recomienda sostener el monitoreo mensual y validar estos resultados con datos reales.")
    else:
        ix=weak[0]
        st.warning(f"Prioridad: {BSC_NAMES[ix]}. Cumplimiento de meta: {ratios[ix]:.1f}%. Acción: {corrective[ix]}")
    report=[]
    for i in range(4):
        report.append({"Perspectiva":BSC_NAMES[i],"Objetivo":BSC_OBJECTIVES[i],"FODA":BSC_FODA[i],
                       "KPI actual (%)":round(actuals[i],1),"Meta (%)":BSC_GOALS[i],
                       "Cumplimiento (%)":round(ratios[i],1),"Acción":BSC_ACTIONS[i],
                       "Decisión correctiva":corrective[i] if ratios[i]<100 else "Mantener el resultado y monitorear"})
    st.dataframe(pd.DataFrame(report),hide_index=True,use_container_width=True,
                 column_config={"Cumplimiento (%)":st.column_config.ProgressColumn("Cumplimiento de meta (%)",min_value=0,max_value=100,format="%.1f%%")})
    st.download_button("⬇ Exportar BSC y decisiones (CSV)",data=pd.DataFrame(report).to_csv(index=False).encode("utf-8-sig"),
                       file_name="NEXDATA_BSC_estrategico.csv",mime="text/csv",key="download_bsc")
    st.caption("Diagnóstico automatizado por reglas: no utiliza un modelo de IA generativa. Para IA generativa se requiere una integración API adicional.")
