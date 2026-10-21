import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime
import json

st.set_page_config(page_title="NEXDATA | BSC Intelligence 360°",page_icon="✦",layout="wide",initial_sidebar_state="collapsed")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"],.stApp{font-family:'DM Sans',sans-serif}
.stApp{background:linear-gradient(135deg,#070f22,#101c38 52%,#081427);color:#eef5ff}
h1,h2,h3,h4,p,label{color:#edf5ff!important}
[data-testid="stMetric"]{background:linear-gradient(145deg,#182e50,#0f203a);padding:18px;border:1px solid #365176;border-radius:18px}
[data-testid="stMetricLabel"] *,[data-testid="stMetricValue"]{color:#f5fbff!important}
[data-baseweb="tab-list"]{gap:8px;flex-wrap:wrap}
button[data-baseweb="tab"]{border:1px solid #315175;border-radius:12px;background:#142642;color:#e9f5ff;padding:9px 15px}
button[data-baseweb="tab"][aria-selected="true"]{background:#196b8a;color:white}
[data-testid="stDataFrame"]{border:1px solid #315175;border-radius:12px}
.hero{background:linear-gradient(120deg,#122c55,#153d59,#1a244f);border:1px solid #3b6484;border-radius:22px;padding:26px;margin-bottom:16px}
.hero h1{color:white!important;margin:0;font-size:2.1rem}
.hero p{color:#c9e2f5!important;margin-top:8px}
.note{background:#112d43;border-left:4px solid #28d8cf;padding:12px 16px;border-radius:8px;color:#d4efff;margin:12px 0}
.small{color:#a8c5e0!important;font-size:.88rem}
</style>""",unsafe_allow_html=True)
COLORS=['#3ad5d0','#a68cff','#ffbd69','#5b9aff','#ff7197']
st.markdown('<div class="hero"><h1>✦ NEXDATA · BSC Intelligence 360°</h1><p>Cuadro de Mando Integral independiente · Plan Estratégico NEXDATA · Horizonte: octubre 2026 – marzo 2027</p></div>',unsafe_allow_html=True)
st.caption('PROYECTO ACADÉMICO · KPI internos simulados y editables. Las fuentes externas son contexto, no resultados comerciales de NEXDATA.')

if 'inputs' not in st.session_state:
    st.session_state.inputs={'prospectos':30,'clientes':8,'ingresos':820,'costos':1000,'horas_total':720,'horas_disp':698.4,'equipo':4,'capacitados':3,'acciones_rrhh':4,'acciones_rrhh_realizadas':3}
if 'initiatives' not in st.session_state:
    st.session_state.initiatives=pd.DataFrame([
      ['Finanzas','Control de gastos y revisión de suscripciones','Finanzas','Flujo de caja mensual','Mensual','Planificado'],
      ['Clientes','Campaña digital y demostraciones a MYPES','Marketing','Registro de prospectos y clientes','Mensual','En ejecución'],
      ['Procesos','Pruebas piloto y corrección de incidencias','Operaciones','Bitácora y versión mejorada','Mensual','En ejecución'],
      ['RR. HH.','Asignación de responsables y seguimiento','Dirección / RR. HH.','Matriz de responsabilidades','Mensual','Planificado'],
      ['Aprendizaje','Dos sesiones de formación y evaluación','RR. HH.','Registro y evaluación de capacitación','Bimestral','En ejecución'],
    ],columns=['Dimensión','Iniciativa NEXDATA','Responsable','Entregable','Frecuencia','Estado'])
v=st.session_state.inputs

def kpis():
    return {'Finanzas':100*v['ingresos']/v['costos'] if v['costos'] else 0,
            'Clientes':100*v['clientes']/v['prospectos'] if v['prospectos'] else 0,
            'Procesos':100*v['horas_disp']/v['horas_total'] if v['horas_total'] else 0,
            'RR. HH.':100*v['acciones_rrhh_realizadas']/v['acciones_rrhh'] if v['acciones_rrhh'] else 0,
            'Aprendizaje':100*v['capacitados']/v['equipo'] if v['equipo'] else 0}
TARGET={'Finanzas':100.,'Clientes':100*10/30,'Procesos':95.,'RR. HH.':100.,'Aprendizaje':100.}
OWNERS={'Finanzas':'Finanzas','Clientes':'Marketing','Procesos':'Operaciones / Logística','RR. HH.':'Dirección / RR. HH.','Aprendizaje':'RR. HH.'}
GOALS={'Finanzas':'Cubrir los costos operativos al mes 6','Clientes':'Captar 30 prospectos y convertir 10 en clientes','Procesos':'Mantener disponibilidad de plataforma ≥95%','RR. HH.':'Cumplir el 100% de actividades de organización del equipo','Aprendizaje':'Capacitar al 100% del equipo (al menos dos sesiones)'}
FORMULAS={'Finanzas':'Ingresos / costos × 100','Clientes':'Clientes / prospectos × 100','Procesos':'Horas disponibles / horas totales × 100','RR. HH.':'Acciones de RR. HH. realizadas / planificadas × 100','Aprendizaje':'Personal capacitado / total del equipo × 100'}


def radial(title,actual,target,color):
    fig=go.Figure(go.Indicator(mode='gauge+number',value=min(actual,150),number={'suffix':'%','font':{'size':31,'color':'#e8f8ff'}},title={'text':title,'font':{'size':15,'color':'#bcdaf1'}},gauge={'axis':{'range':[0,max(110,target*1.15)],'tickcolor':'#b8d3e9'},'bar':{'color':color,'thickness':0.24},'bgcolor':'#152843','borderwidth':0,'steps':[{'range':[0,max(110,target*1.15)],'color':'#263958'}],'threshold':{'line':{'color':'#fff','width':3},'thickness':0.7,'value':target}}))
    fig.update_layout(height=255,margin=dict(l=22,r=22,t=52,b=15),paper_bgcolor='rgba(0,0,0,0)',font_color='#dff2ff')
    return fig

def radar():
    vals=kpis();names=list(vals);norm=[min(vals[x]/TARGET[x]*100,130) for x in names]
    fig=go.Figure()
    fig.add_trace(go.Scatterpolar(r=norm+[norm[0]],theta=names+[names[0]],fill='toself',name='Cumplimiento relativo',line_color='#3ad5d0',fillcolor='rgba(58,213,208,.26)'))
    fig.add_trace(go.Scatterpolar(r=[100]*6,theta=names+[names[0]],name='Meta 100%',line=dict(color='#ffbd69',dash='dot')))
    fig.update_layout(polar=dict(bgcolor='#142742',radialaxis=dict(range=[0,135],gridcolor='#3b5875',color='#c5e3f5'),angularaxis=dict(gridcolor='#355373',color='#f2f8ff')),paper_bgcolor='rgba(0,0,0,0)',font_color='#d7f0ff',height=390,margin=dict(t=30,b=30,l=45,r=45),legend=dict(orientation='h'))
    return fig

def sankey():
    fig=go.Figure(go.Sankey(arrangement='snap',node=dict(pad=19,thickness=17,line=dict(color='#abc',width=.3),label=['Capacitación','Equipo organizado','Plataforma estable','Clientes MYPE','Ingresos sostenibles'],color=COLORS),link=dict(source=[0,1,2,3],target=[1,2,3,4],value=[1,1,1,1],color=['rgba(58,213,208,.4)','rgba(166,140,255,.4)','rgba(255,189,105,.4)','rgba(91,154,255,.4)'])))
    fig.update_layout(title='Hipótesis de causa–efecto del plan estratégico',height=300,paper_bgcolor='rgba(0,0,0,0)',font_color='#e5f7ff',margin=dict(l=20,r=20,b=20,t=60))
    return fig

def score_table():
    vals=kpis();return pd.DataFrame([{'Dimensión':x,'Objetivo NEXDATA':GOALS[x],'KPI':FORMULAS[x],'Actual (%)':round(vals[x],2),'Meta (%)':round(TARGET[x],2),'Cumplimiento (%)':round(vals[x]/TARGET[x]*100,1),'Responsable':OWNERS[x],'Estado':'En meta' if vals[x]>=TARGET[x] else 'Requiere acción'} for x in vals])

def plot_bubble():
    df=score_table();df['Brecha (pp)']=(df['Meta (%)']-df['Actual (%)']).clip(lower=0)
    df['Impacto propuesto']=[5,5,5,3,4]
    fig=px.scatter(df,x='Brecha (pp)',y='Impacto propuesto',size='Brecha (pp)',size_max=58,color='Dimensión',hover_data=['Objetivo NEXDATA','Responsable'],color_discrete_sequence=COLORS,title='Matriz de prioridad: brecha frente a impacto estimado')
    fig.update_traces(marker=dict(line=dict(width=2,color='#ffffff')))
    fig.update_layout(height=390,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='#152842',font_color='#eaf7ff',legend=dict(orientation='h'),xaxis=dict(gridcolor='#35516e'),yaxis=dict(gridcolor='#35516e',range=[1,6]))
    return fig

@st.cache_data(ttl=86400,show_spinner=False)
def get_worldbank():
    url='https://api.worldbank.org/v2/country/PER/indicator/IT.NET.USER.ZS?format=json&per_page=70'
    try:
        resp=requests.get(url,timeout=10);resp.raise_for_status();rows=resp.json()[1]
        data=sorted([(int(z['date']),float(z['value'])) for z in rows if z.get('value') is not None])
        return data,None,url
    except Exception as exc:return [],str(exc),url

def recommendation(name):
    return {'Finanzas':'Revisar el flujo de caja, gastos de hosting y costos de desarrollo; validar el precio de suscripción antes de expandirse.',
            'Clientes':'Ejecutar demostraciones con MYPES, registrar prospectos y dar seguimiento a las oportunidades comerciales.',
            'Procesos':'Priorizar corrección de incidencias, pruebas de carga y seguimiento de disponibilidad de la plataforma.',
            'RR. HH.':'Asignar responsables faltantes, verificar tareas pendientes y formalizar el calendario de seguimiento.',
            'Aprendizaje':'Programar las capacitaciones pendientes, documentar asistencia y evaluar las competencias adquiridas.'}[name]

tabs=st.tabs(['◉ Resumen BSC','◈ Finanzas','◎ Clientes y Marketing','⚙ Procesos internos','♧ Recursos Humanos','✦ Capacitación y aprendizaje','✧ Inteligencia y fuentes'])
with tabs[0]:
    st.subheader('Mapa estratégico y cumplimiento de NEXDATA')
    st.markdown('<div class="note">Visión → convertir a NEXDATA en una plataforma de analítica accesible para MYPES peruanas. Las relaciones del mapa son hipótesis estratégicas por validar.</div>',unsafe_allow_html=True)
    cols=st.columns(5)
    for i,(name,val) in enumerate(kpis().items()):
        with cols[i]:st.plotly_chart(radial(name,val,TARGET[name],COLORS[i]),use_container_width=True,key='gauge_'+str(i))
    a,b=st.columns([1,1])
    with a:st.plotly_chart(radar(),use_container_width=True,key='radar_summary')
    with b:st.plotly_chart(sankey(),use_container_width=True,key='sankey_summary')
    st.dataframe(score_table(),use_container_width=True,hide_index=True)
    st.caption('El KPI de RR. HH. (cumplimiento de actividades organizativas) es un indicador complementario; en el BSC clásico RR. HH. y capacitación pertenecen a aprendizaje y crecimiento.')

with tabs[1]:
    st.subheader('Perspectiva financiera · Sostenibilidad del negocio')
    st.write('**Objetivo del plan:** que los ingresos de NEXDATA cubran al menos el 100% de los costos operativos al sexto mes. Responsable: Finanzas.')
    a,b=st.columns(2)
    with a:v['ingresos']=st.number_input('Ingresos mensuales simulados (S/)',min_value=0.0,value=float(v['ingresos']),step=50.0)
    with b:v['costos']=st.number_input('Costos operativos mensuales simulados (S/)',min_value=1.0,value=float(v['costos']),step=50.0)
    st.plotly_chart(radial('Cobertura de costos',kpis()['Finanzas'],100,COLORS[0]),use_container_width=True,key='gauge_fin')
    st.metric('Resultado neto mensual simulado',f"S/ {v['ingresos']-v['costos']:,.2f}")
    scenarios=pd.DataFrame({'Escenario':['Actual','+10% ingresos','-10% costos','Ambos'],'Cobertura (%)':[kpis()['Finanzas'],v['ingresos']*1.1/v['costos']*100,v['ingresos']/(v['costos']*.9)*100,v['ingresos']*1.1/(v['costos']*.9)*100]})
    fig=px.line(scenarios,x='Escenario',y='Cobertura (%)',markers=True,title='Simulación de cobertura financiera',color_discrete_sequence=[COLORS[0]])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='#142742',font_color='#eaf7ff');st.plotly_chart(fig,use_container_width=True)
    st.info('Iniciativa: controlar costos de infraestructura y evaluar un modelo de suscripción. Entregable: flujo de caja mensual.')
with tabs[2]:
    st.subheader('Perspectiva clientes · Captación de MYPES')
    st.write('**Objetivo del plan:** obtener 30 prospectos y 10 clientes en seis meses. Responsable: Marketing. KPI: tasa de conversión.')
    a,b=st.columns(2)
    with a:v['prospectos']=st.number_input('Prospectos registrados (simulación)',min_value=1,value=int(v['prospectos']))
    with b:v['clientes']=st.number_input('Clientes convertidos (simulación)',min_value=0,max_value=int(v['prospectos']),value=min(int(v['clientes']),int(v['prospectos'])))
    st.plotly_chart(radial('Tasa de conversión',kpis()['Clientes'],TARGET['Clientes'],COLORS[1]),use_container_width=True,key='gauge_cli')
    fig=go.Figure(go.Funnel(y=['Prospectos','Clientes'],x=[v['prospectos'],v['clientes']],marker={'color':[COLORS[1],COLORS[0]]},textinfo='value+percent initial'))
    fig.update_layout(title='Embudo comercial de NEXDATA',paper_bgcolor='rgba(0,0,0,0)',font_color='#eaf7ff',height=340);st.plotly_chart(fig,use_container_width=True)
    st.info('Iniciativa: campañas digitales y demostraciones de la plataforma para MYPES. Entregable: base de prospectos y reporte de conversión.')
with tabs[3]:
    st.subheader('Perspectiva procesos internos · Plataforma confiable')
    st.write('**Objetivo del plan:** disponibilidad mínima del 95%. Responsable: Operaciones / Logística.')
    a,b=st.columns(2)
    with a:v['horas_total']=st.number_input('Horas totales del periodo',min_value=1.0,value=float(v['horas_total']))
    with b:v['horas_disp']=st.number_input('Horas disponibles',min_value=0.0,max_value=float(v['horas_total']),value=min(float(v['horas_disp']),float(v['horas_total'])))
    st.plotly_chart(radial('Disponibilidad',kpis()['Procesos'],95,COLORS[2]),use_container_width=True,key='gauge_proc')
    fig=go.Figure(go.Pie(labels=['Disponibilidad','Interrupción'],values=[v['horas_disp'],max(0,v['horas_total']-v['horas_disp'])],hole=.74,marker={'colors':[COLORS[0],'#ff7197']}))
    fig.update_layout(title='Composición del tiempo operativo',paper_bgcolor='rgba(0,0,0,0)',font_color='#eaf7ff',height=340);st.plotly_chart(fig,use_container_width=True)
    st.info('Iniciativa: pruebas piloto, registro de incidencias y mejoras de usabilidad. Entregable: bitácora de incidentes y versión optimizada.')
with tabs[4]:
    st.subheader('Gestión de Recursos Humanos · Organización y ejecución')
    st.write('**Objetivo complementario:** que todas las actividades de coordinación del equipo tengan seguimiento. Responsable: Dirección / RR. HH.')
    a,b=st.columns(2)
    with a:v['acciones_rrhh']=st.number_input('Acciones organizativas planificadas',min_value=1,value=int(v['acciones_rrhh']))
    with b:v['acciones_rrhh_realizadas']=st.number_input('Acciones organizativas realizadas',min_value=0,max_value=int(v['acciones_rrhh']),value=min(int(v['acciones_rrhh_realizadas']),int(v['acciones_rrhh'])))
    st.plotly_chart(radial('Ejecución RR. HH.',kpis()['RR. HH.'],100,COLORS[3]),use_container_width=True,key='gauge_rrhh')
    st.dataframe(pd.DataFrame([['Marketing','Captación y demostraciones'],['Finanzas','Control presupuestal'],['Operaciones','Disponibilidad y soporte'],['RR. HH.','Asignación y seguimiento del equipo']],columns=['Área','Responsabilidad NEXDATA']),hide_index=True,use_container_width=True)
    st.info('Iniciativa: asignar responsables y realizar reuniones de seguimiento. Entregable: matriz de responsabilidades y actas.')
with tabs[5]:
    st.subheader('Aprendizaje y crecimiento · Capacitación del equipo')
    st.write('**Objetivo del plan:** capacitar al 100% del equipo mediante al menos dos sesiones durante seis meses. Responsable: RR. HH.')
    a,b=st.columns(2)
    with a:v['equipo']=st.number_input('Integrantes del equipo',min_value=1,value=int(v['equipo']))
    with b:v['capacitados']=st.number_input('Integrantes capacitados',min_value=0,max_value=int(v['equipo']),value=min(int(v['capacitados']),int(v['equipo'])))
    st.plotly_chart(radial('Personal capacitado',kpis()['Aprendizaje'],100,COLORS[4]),use_container_width=True,key='gauge_cap')
    fig=go.Figure(go.Pie(labels=['Capacitados','Pendientes'],values=[v['capacitados'],v['equipo']-v['capacitados']],hole=.62,marker={'colors':[COLORS[0],COLORS[4]]}))
    fig.update_layout(title='Progreso de formación',paper_bgcolor='rgba(0,0,0,0)',font_color='#eaf7ff',height=320);st.plotly_chart(fig,use_container_width=True)
    st.info('Iniciativa: formación en análisis de datos, atención a MYPES y uso de la plataforma. Entregable: registros de asistencia y evaluación.')
with tabs[6]:
    st.subheader('Inteligencia estratégica · Evidencia y decisiones')
    st.caption('El motor local aplica reglas verificables. Para IA generativa opcional, configure una clave privada de API en Streamlit Secrets.')
    st.plotly_chart(plot_bubble(),use_container_width=True,key='bubble')
    df=score_table().sort_values('Cumplimiento (%)')
    critical=df.iloc[0]['Dimensión']
    st.warning(f"**Prioridad detectada:** {critical} · {df.iloc[0]['Cumplimiento (%)']:.1f}% de cumplimiento relativo de la meta. **Acción:** {recommendation(critical)}")
    st.subheader('Iniciativas editables y trazabilidad')
    st.session_state.initiatives=st.data_editor(st.session_state.initiatives,use_container_width=True,num_rows='dynamic',hide_index=True,key='initiatives_editor')
    st.subheader('Fuente externa online · Banco Mundial')
    data,err,url=get_worldbank()
    if data:
        d=pd.DataFrame(data,columns=['Año','Población usuaria de internet (%)'])
        latest=d.iloc[-1]
        st.metric('Perú · último dato disponible',f"{latest.iloc[1]:.1f}%",help=f'Año de referencia: {int(latest.iloc[0])}. No mide directamente adopción de software por MYPES.')
        fig=px.area(d.tail(15),x='Año',y='Población usuaria de internet (%)',title='Contexto de digitalización en Perú',color_discrete_sequence=[COLORS[0]])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='#142742',font_color='#eaf7ff');st.plotly_chart(fig,use_container_width=True)
        st.caption(f'Banco Mundial · indicador IT.NET.USER.ZS · año {int(latest.iloc[0])} · consulta {datetime.now().strftime("%Y-%m-%d")} · {url}')
    else:st.error(f'No se pudo consultar la API en este momento: {err}. No se inventan datos.');st.markdown(f'[Abrir fuente]({url})')
    st.markdown('**Referencias metodológicas:** [Balanced Scorecard Institute](https://balancedscorecard.org/bsc-basics/) · [Banco Mundial, API WDI](https://data.worldbank.org/indicator/IT.NET.USER.ZS?locations=PE) · [INEI](https://www.inei.gob.pe/)')
    st.markdown('**Interpretación:** la penetración de internet es un indicador de contexto y no prueba demanda de NEXDATA ni sustituye una investigación de clientes.')
    st.subheader('Asistente estratégico (opcional: IA generativa)')
    prompt=st.text_area('Pregunta para el asesor de NEXDATA',value='¿Qué decisiones debemos priorizar según el BSC y cómo medir sus resultados?')
    if st.button('Analizar el BSC',type='primary'):
        try:
            from openai import OpenAI
            key=st.secrets.get('OPENAI_API_KEY',None)
            if not key:st.info('Sin clave API: análisis automatizado disponible. Configure OPENAI_API_KEY en los secretos privados de esta nueva app para activar IA generativa.');st.write(f'Prioridad: {critical}. {recommendation(critical)}')
            else:
                client=OpenAI(api_key=key)
                context={'plan':'NEXDATA: plataforma de análisis para MYPES, metas académicas a seis meses','kpis_simulados':score_table().to_dict('records'),'iniciativas':st.session_state.initiatives.to_dict('records')}
                response=client.responses.create(model=st.secrets.get('OPENAI_MODEL','gpt-4.1-mini'),instructions='Eres asesor de estrategia de NEXDATA. Responde en español, distingue simulaciones de datos reales, no inventes fuentes ni resultados, fundamenta decisiones en KPI, acciones y responsables.',input=json.dumps(context,ensure_ascii=False)+'\nPregunta: '+prompt)
                st.write(response.output_text)
        except Exception as exc:st.error(f'No fue posible completar la consulta IA: {exc}')
    st.download_button('Descargar matriz BSC (CSV)',score_table().to_csv(index=False).encode('utf-8-sig'),'NEXDATA_BSC_indicadores.csv','text/csv')
