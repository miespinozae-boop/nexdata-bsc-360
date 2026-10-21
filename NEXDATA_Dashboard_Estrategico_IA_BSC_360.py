import json
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
import streamlit as st

st.set_page_config(page_title='NEXDATA | BSC Live 360',page_icon='✦',layout='wide',initial_sidebar_state='expanded')
st.markdown("""<style>
:root{color-scheme:light;--nx-bg:#F8F9FC;--nx-ink:#172554;--nx-muted:#475569;--nx-border:#DCE2F0;--nx-blue:#4F46E5}
html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:#F8F9FC!important;color:#172554!important}
[data-testid="stHeader"]{background:rgba(248,249,252,.96)!important}
[data-testid="stSidebar"],[data-testid="stSidebarContent"]{background:#F0F1FC!important;border-right:1px solid #DCE2F0!important}
.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp h5,.stApp h6,.stApp p,.stApp li,.stApp label,.stApp strong,.stApp small,.stApp [data-testid="stMarkdownContainer"] p,.stApp [data-testid="stMarkdownContainer"] li,.stApp [data-testid="stMarkdownContainer"] strong,[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,[data-testid="stSidebar"] p,[data-testid="stSidebar"] label,[data-testid="stWidgetLabel"] p{color:#172554!important}
.stApp [data-testid="stCaptionContainer"],.stApp [data-testid="stCaptionContainer"] p,.stApp [data-testid="stMarkdownContainer"] em{color:#475569!important}
.stApp a,.stApp a:visited{color:#4338CA!important;text-decoration:underline!important;text-underline-offset:3px}
[data-testid="stMetric"]{background:#FFFFFF!important;padding:16px!important;border:1px solid #E0E4F1!important;border-radius:16px!important;box-shadow:0 5px 22px rgba(30,41,90,.06)}
[data-testid="stMetric"] *,[data-testid="stMetricLabel"] *,[data-testid="stMetricValue"] *{color:#172554!important}
[data-testid="stMetricDelta"] *{color:#166534!important}
[data-baseweb="tab-list"]{gap:8px!important;flex-wrap:wrap!important;padding:8px 0 14px!important}
button[data-baseweb="tab"]{background:#EDE9FE!important;border:1px solid #D8D0FC!important;border-radius:12px!important;padding:10px 14px!important;color:#3730A3!important;font-weight:650!important}
button[data-baseweb="tab"] *{color:#3730A3!important}
button[data-baseweb="tab"]:hover{background:#DDD6FE!important}
button[data-baseweb="tab"][aria-selected="true"]{background:#4F46E5!important;border-color:#4F46E5!important;box-shadow:0 4px 14px rgba(79,70,229,.2)!important}
button[data-baseweb="tab"][aria-selected="true"] *{color:#FFFFFF!important}
[data-testid="stTextArea"] textarea,[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,[data-testid="stDateInput"] input,[data-baseweb="input"] input,[data-baseweb="textarea"] textarea,[data-baseweb="select"]>div{background:#FFFFFF!important;color:#172554!important;-webkit-text-fill-color:#172554!important;caret-color:#4F46E5!important;border-color:#CBD3E7!important}
[data-baseweb="input"] input::placeholder,[data-baseweb="textarea"] textarea::placeholder{color:#64748B!important;-webkit-text-fill-color:#64748B!important}
[data-baseweb="select"] span,[data-baseweb="select"] svg{color:#172554!important}
[data-testid="stNumberInput"] button{background:#EDE9FE!important;color:#3730A3!important;border-color:#D8D0FC!important}
[data-testid="stNumberInput"] button svg{color:#3730A3!important;fill:#3730A3!important}
[data-testid="stButton"] button{background:#4F46E5!important;color:#FFFFFF!important;border:1px solid #4F46E5!important;font-weight:700!important;border-radius:10px!important}
[data-testid="stButton"] button *{color:#FFFFFF!important}
[data-testid="stButton"] button:hover{background:#3730A3!important}
[data-testid="stDownloadButton"] button,[data-testid="stFileUploader"] button{background:#EDE9FE!important;color:#3730A3!important;border:1px solid #C4B5FD!important;font-weight:700!important}
[data-testid="stDownloadButton"] button *{color:#3730A3!important}
[data-testid="stExpander"]{background:#FFFFFF!important;border:1px solid #E0E4F1!important;border-radius:13px!important}
[data-testid="stExpander"] summary,[data-testid="stExpander"] summary *{color:#172554!important}
[data-testid="stFileUploader"]{background:#FFFFFF!important;border:1px solid #DCE2F0!important;border-radius:12px!important;padding:8px!important}
[data-testid="stDataEditor"],[data-testid="stDataFrame"]{border:1px solid #DCE2F0!important;border-radius:12px!important;overflow:hidden;background:#FFFFFF!important}
[data-testid="stDataEditor"] [role="grid"],[data-testid="stDataFrame"] [role="grid"]{background:#FFFFFF!important;color:#172554!important}
[data-testid="stDataEditor"] [role="grid"] *,[data-testid="stDataFrame"] [role="grid"] *{color:#172554!important}
[data-testid="stAlert"]{border-radius:12px!important}
[data-testid="stAlert"] p,[data-testid="stAlert"] strong{color:#172554!important}
[data-testid="stSlider"] [role="slider"]{background:#4F46E5!important}
.hero{background:linear-gradient(115deg,#EDE9FE,#F4F3FF 55%,#E8ECFF)!important;padding:26px!important;border:1px solid #D9D2FB!important;border-radius:20px!important;margin-bottom:18px!important;box-shadow:0 8px 24px rgba(55,48,163,.06)}
.hero h1{margin:0!important;color:#172554!important;font-size:2.05rem!important}
.hero p{color:#433878!important;font-size:1rem!important}
@media(max-width:800px){.hero{padding:17px!important}.hero h1{font-size:1.5rem!important}}
</style>""",unsafe_allow_html=True)

FIELDS={
 'prospectos':('Prospectos captados',30,1,100000,1), 'clientes':('Clientes convertidos',8,0,100000,1),
 'ingresos':('Ingresos mensuales S/',820.,0.,10000000.,50.), 'costos':('Costos mensuales S/',1000.,1.,10000000.,50.),
 'horas_total':('Horas del periodo',720.,1.,100000.,1.),'horas_disp':('Horas disponibles',698.4,0.,100000.,1.),
 'equipo':('Total de integrantes',4,1,100000,1),'capacitados':('Integrantes capacitados',3,0,100000,1),
 'rrhh_total':('Acciones RR. HH. planificadas',4,1,100000,1),'rrhh_hechas':('Acciones RR. HH. realizadas',3,0,100000,1)}
DEFAULT_TARGET={'Finanzas':100.,'Clientes':33.333333,'Procesos':95.,'Aprendizaje':100.}
COLORS={'Finanzas':'#4F46E5','Clientes':'#0F766E','Procesos':'#D97706','Aprendizaje':'#7C3AED'}
OWNERS={'Finanzas':'Finanzas','Clientes':'Marketing','Procesos':'Operaciones / Logística','Aprendizaje':'RR. HH.'}
GOALS={'Finanzas':'Cubrir costos operativos al sexto mes','Clientes':'Captar 30 prospectos y 10 clientes en seis meses','Procesos':'Garantizar disponibilidad y atender incidencias','Aprendizaje':'Capacitar al 100% del equipo en seis meses'}
FORMULAS={'Finanzas':'Ingresos / costos × 100','Clientes':'Clientes / prospectos × 100','Procesos':'Horas disponibles / horas totales × 100','Aprendizaje':'Integrantes capacitados / total × 100'}
ACTIONS=pd.DataFrame([
 ['Finanzas','Control de hosting, desarrollo y suscripciones','Finanzas','Flujo de caja','Mensual','En ejecución'],
 ['Clientes','Campañas y demostraciones para MYPES','Marketing','Registro de prospectos','Mensual','En ejecución'],
 ['Procesos','Pruebas piloto y seguimiento de incidencias','Operaciones','Bitácora de incidencias','Semanal','En ejecución'],
 ['Aprendizaje','Asignar responsables y hacer seguimiento','Dirección / RR. HH.','Matriz de responsabilidades','Mensual','Planificado'],
 ['Aprendizaje','Realizar dos sesiones de capacitación','RR. HH.','Asistencia y evaluación','Bimestral','Planificado']],columns=['Dimensión','Iniciativa','Responsable','Entregable','Frecuencia','Estado'])
if 'actions_seed' not in st.session_state:st.session_state.actions_seed=ACTIONS.copy()
for key,(_,default,_,_,_) in FIELDS.items():
 if 'live_'+key not in st.session_state:st.session_state['live_'+key]=default
for name,val in DEFAULT_TARGET.items():
 if 'goal_'+name not in st.session_state:st.session_state['goal_'+name]=val

with st.sidebar:
 st.header('✦ Centro de edición en vivo')
 st.caption('Modifica valores y pulsa Enter o sal del campo. Streamlit recalcula automáticamente los KPI y gráficos en cada interacción.')
 with st.expander('Finanzas',expanded=True):
  for key in ['ingresos','costos']:
   label,_,low,high,step=FIELDS[key];st.number_input(label,min_value=low,max_value=high,step=step,key='live_'+key)
 with st.expander('Clientes / Marketing',expanded=True):
  for key in ['prospectos','clientes']:
   label,_,low,high,step=FIELDS[key];st.number_input(label,min_value=low,max_value=high,step=step,key='live_'+key)
 with st.expander('Procesos internos'):
  for key in ['horas_total','horas_disp']:
   label,_,low,high,step=FIELDS[key];st.number_input(label,min_value=low,max_value=high,step=step,key='live_'+key)
 with st.expander('Aprendizaje y crecimiento · RR. HH. y capacitación'):
  for key in ['rrhh_total','rrhh_hechas','equipo','capacitados']:
   label,_,low,high,step=FIELDS[key];st.number_input(label,min_value=low,max_value=high,step=step,key='live_'+key)
 with st.expander('Modificar metas KPI'):
  for name in DEFAULT_TARGET:st.number_input('Meta '+name+' (%)',min_value=.1,max_value=10000.,step=1.,key='goal_'+name)
 if st.button('Restablecer indicadores',use_container_width=True):
  for key,(_,default,_,_,_) in FIELDS.items():st.session_state['live_'+key]=default
  for name,val in DEFAULT_TARGET.items():st.session_state['goal_'+name]=val
  st.rerun()

v={k:st.session_state['live_'+k] for k in FIELDS}
target={n:st.session_state['goal_'+n] for n in DEFAULT_TARGET}

def safe_ratio(a,b):return 100*a/b if b else 0.
actual={'Finanzas':safe_ratio(v['ingresos'],v['costos']),'Clientes':safe_ratio(v['clientes'],v['prospectos']),
 'Procesos':safe_ratio(min(v['horas_disp'],v['horas_total']),v['horas_total']),
 'Aprendizaje':safe_ratio(min(v['capacitados'],v['equipo']),v['equipo'])}
score=pd.DataFrame([{'Dimensión':n,'Objetivo del plan':GOALS[n],'KPI / fórmula':FORMULAS[n],
 'Actual (%)':round(actual[n],2),'Meta (%)':round(target[n],2),'Cumplimiento relativo (%)':round(safe_ratio(actual[n],target[n]),1),
 'Responsable':OWNERS[n],'Estado':'Cumple' if actual[n]>=target[n] else 'Pendiente'} for n in actual])

def layout(fig,height=350):
 fig.update_layout(height=height,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='#ffffff',font=dict(color='#172554',size=13),hoverlabel=dict(bgcolor='#ffffff',font_color='#172554',font_size=13),margin=dict(l=30,r=30,t=55,b=25),legend=dict(font=dict(color='#172554')))
 return fig

def gauge(name):
 val=actual[name];tar=target[name];cap=max(110.,val*1.12,tar*1.12)
 fig=go.Figure(go.Indicator(mode='gauge+number',value=val,number={'suffix':'%','font':{'color':'#172554','size':31}},title={'text':name,'font':{'color':'#172554'}},
 gauge={'axis':{'range':[0,cap],'tickcolor':'#64748B'},'bar':{'color':COLORS[name]},'bgcolor':'#EDE9FE',
 'steps':[{'range':[0,cap],'color':'#e6eef8'}],'threshold':{'line':{'color':'#243c54','width':4},'value':tar}}))
 return layout(fig,245)

def radar():
 names=list(actual);norm=[min(safe_ratio(actual[n],target[n]),150) for n in names]
 fig=go.Figure()
 fig.add_trace(go.Scatterpolar(r=norm+[norm[0]],theta=names+[names[0]],fill='toself',line_color='#38ded3',fillcolor='rgba(56,222,211,.25)',name='Cumplimiento'))
 fig.add_trace(go.Scatterpolar(r=[100]*(len(names)+1),theta=names+[names[0]],line=dict(color='#ffc579',dash='dash'),name='Meta'))
 fig.update_layout(polar=dict(bgcolor='#ffffff',radialaxis=dict(range=[0,155],gridcolor='#DCE2F0',color='#172554'),angularaxis=dict(color='#172554')),legend=dict(orientation='h'))
 return layout(fig,405)

def sankey():
 names=['Aprendizaje y RR. HH.','Procesos confiables','Clientes MYPE','Sostenibilidad financiera']
 fig=go.Figure(go.Sankey(node=dict(pad=20,thickness=20,label=names,color=list(COLORS.values())),link=dict(source=[0,1,2],target=[1,2,3],value=[1,1,1],color=['rgba(39,211,179,.35)','rgba(102,173,255,.35)','rgba(255,189,112,.35)'])))
 fig.update_layout(title='Hipótesis estratégica causa–efecto (no flujo financiero medido)')
 return layout(fig,360)

def priority():
 df=score.copy();df['Brecha (pp)']=(df['Meta (%)']-df['Actual (%)']).clip(lower=0);df['Impacto propuesto']=[5,5,4,4]
 df['Tamaño']=df['Brecha (pp)'].clip(lower=2)
 fig=px.scatter(df,x='Brecha (pp)',y='Impacto propuesto',size='Tamaño',color='Dimensión',hover_data=['Objetivo del plan','Responsable'],color_discrete_map=COLORS,size_max=55,title='Matriz de prioridades: brecha vs. impacto estimado')
 return layout(fig,385)

@st.cache_data(ttl=3600,show_spinner=False)
def worldbank():
 url='https://api.worldbank.org/v2/country/PER/indicator/IT.NET.USER.ZS?format=json&per_page=70'
 try:
  response=requests.get(url,timeout=12);response.raise_for_status();body=response.json()
  rows=sorted([(int(x['date']),float(x['value'])) for x in body[1] if x.get('value') is not None]);return rows,None,url
 except Exception as exc:return [],str(exc),url

RECOMMEND={
 'Finanzas':'Finanzas debe revisar costos de hosting, estimar ingresos por suscripciones y actualizar el flujo de caja mensual.',
 'Clientes':'Marketing debe ampliar demostraciones a MYPES, registrar prospectos y mejorar el seguimiento de conversiones.',
 'Procesos':'Operaciones debe revisar incidencias, ejecutar pruebas piloto y verificar la disponibilidad de la plataforma.',
  'Aprendizaje':'RR. HH. debe programar las capacitaciones faltantes, registrar asistencia y evaluar conocimientos.'}

st.markdown('<div class="hero"><h1>✦ NEXDATA | BSC LIVE 360°</h1><p>Aplicación independiente · Balanced Scorecard alineado al plan estratégico · Edición y simulación en tiempo real</p></div>',unsafe_allow_html=True)
st.caption('PROYECTO ACADÉMICO · Datos internos de demostración, editables. Los datos externos se consultan online cuando existe conexión. La información se mantiene en la sesión actual, no en una base de datos compartida.')
if v['clientes']>v['prospectos'] or v['horas_disp']>v['horas_total'] or v['rrhh_hechas']>v['rrhh_total'] or v['capacitados']>v['equipo']:
 st.warning('Algunos datos superan sus totales. Para evitar porcentajes imposibles, los cálculos de Procesos, RR. HH. y Aprendizaje se limitan al total; revisa los campos de edición.')

tabs=st.tabs(['◉ Resumen','◈ Finanzas','◎ Clientes','⚙ Procesos','✦ Aprendizaje y crecimiento','✧ Inteligencia y fuentes','▦ Matriz editable y exportación'])
with tabs[0]:
 st.subheader('Mapa estratégico y cumplimiento')
 cols=st.columns(4)
 for i,name in enumerate(actual):
  with cols[i]:st.plotly_chart(gauge(name),use_container_width=True,key='sum_g'+str(i))
 a,b=st.columns(2)
 with a:st.plotly_chart(radar(),use_container_width=True,key='radar')
 with b:st.plotly_chart(sankey(),use_container_width=True,key='sankey')
 st.dataframe(score,hide_index=True,use_container_width=True)
 st.info('El BSC tiene cuatro perspectivas. Recursos Humanos, organización del equipo y capacitación se integran en Aprendizaje y Crecimiento.')
with tabs[1]:
 st.subheader('Finanzas | Sostenibilidad de NEXDATA')
 st.write('**Objetivo:** cubrir al menos el 100% de costos operativos al sexto mes. **Responsable:** Finanzas.')
 a,b=st.columns(2)
 with a:st.plotly_chart(gauge('Finanzas'),use_container_width=True,key='fin_g')
 with b:st.metric('Resultado mensual simulado',f"S/ {v['ingresos']-v['costos']:,.2f}")
 c,d=st.columns(2)
 with c:inc=st.slider('Variación hipotética de ingresos (%)',-50,100,10,key='sc_inc')
 with d:cost=st.slider('Variación hipotética de costos (%)',-50,100,-10,key='sc_cost')
 sc=safe_ratio(v['ingresos']*(1+inc/100),v['costos']*(1+cost/100))
 st.metric('Cobertura con escenario',f'{sc:.1f}%',delta=f'{sc-actual["Finanzas"]:+.1f} puntos porcentuales')
 fig=go.Figure(go.Waterfall(x=['Ingresos actuales','Variación ingresos','Costos escenario','Resultado escenario'],measure=['absolute','relative','relative','total'],y=[v['ingresos'],v['ingresos']*inc/100,-v['costos']*(1+cost/100),0],connector={'line':{'color':'#94A3B8'}}))
 st.plotly_chart(layout(fig,340),use_container_width=True)
 st.info('Acción del plan: evaluar suscripciones, controlar gastos y revisar el flujo de caja cada mes.')
with tabs[2]:
 st.subheader('Clientes y Marketing | Captación de MYPES')
 st.write('**Objetivo:** 30 prospectos y 10 clientes en seis meses. **Responsable:** Marketing.')
 st.plotly_chart(gauge('Clientes'),use_container_width=True,key='cli_g')
 fig=go.Figure(go.Funnel(y=['Prospectos','Clientes'],x=[v['prospectos'],min(v['clientes'],v['prospectos'])],marker={'color':['#aa91ff','#27d3b3']},textinfo='value+percent initial'))
 st.plotly_chart(layout(fig,360),use_container_width=True)
 st.info('Acción del plan: realizar campañas digitales y demostraciones guiadas para MYPES; medir la conversión mensual.')
with tabs[3]:
 st.subheader('Procesos internos | Disponibilidad y mejora')
 st.write('**Objetivo:** disponibilidad ≥95% y atención oportuna de incidencias. **Responsable:** Operaciones.')
 st.plotly_chart(gauge('Procesos'),use_container_width=True,key='proc_g')
 fig=go.Figure(go.Pie(labels=['Disponible','Interrupción'],values=[min(v['horas_disp'],v['horas_total']),max(0,v['horas_total']-v['horas_disp'])],hole=.73,marker={'colors':['#27d3b3','#ff80b1']}))
 st.plotly_chart(layout(fig,340),use_container_width=True)
 st.info('Acción del plan: pruebas piloto, registro de incidencias y mejora de usabilidad. Entregable: bitácora y versión optimizada.')
with tabs[4]:
 st.subheader('Aprendizaje y crecimiento | Recursos Humanos y capacitación')
 st.write('**Objetivo estratégico:** desarrollar las competencias del equipo NEXDATA y asegurar la ejecución de las actividades de gestión del talento. **Responsable:** Recursos Humanos y Dirección.')
 c1,c2=st.columns(2)
 with c1:
  st.plotly_chart(gauge('Aprendizaje'),use_container_width=True,key='learn_g')
 with c2:
  rr=safe_ratio(min(v['rrhh_hechas'],v['rrhh_total']),v['rrhh_total'])
  st.metric('Seguimiento de tareas RR. HH. (indicador complementario)',f'{rr:.1f}%',help='No es una quinta perspectiva del BSC. Mide las actividades de coordinación completadas.')
  st.metric('Personal capacitado',f"{min(v['capacitados'],v['equipo'])} de {v['equipo']}")
 st.markdown('#### Capacitación del equipo')
 fig=go.Figure(go.Pie(labels=['Capacitados','Pendientes'],values=[min(v['capacitados'],v['equipo']),max(0,v['equipo']-v['capacitados'])],hole=.73,marker={'colors':['#27d3b3','#ff80b1']}))
 st.plotly_chart(layout(fig,320),use_container_width=True)
 st.markdown('#### Organización y responsabilidades de NEXDATA')
 st.dataframe(pd.DataFrame([['Marketing','Captación y demostraciones'],['Finanzas','Presupuesto y flujo de caja'],['Operaciones','Disponibilidad, soporte y pruebas'],['RR. HH.','Organización, capacitación y seguimiento']],columns=['Área','Responsabilidad concreta']),hide_index=True,use_container_width=True)
 st.info('**Acciones:** programar al menos dos capacitaciones, registrar asistencia y evaluación, asignar responsables y dar seguimiento a tareas. **Entregables:** actas de capacitación y matriz de responsabilidades. **KPI principal:** 100% del personal capacitado.')
with tabs[5]:
 st.subheader('Inteligencia estratégica y fuentes externas')
 st.plotly_chart(priority(),use_container_width=True,key='priority')
 bad=score.sort_values('Cumplimiento relativo (%)').iloc[0]
 st.warning(f"**Prioridad actual:** {bad['Dimensión']} — cumplimiento relativo de {bad['Cumplimiento relativo (%)']:.1f}%. {RECOMMEND[bad['Dimensión']]}")
 st.markdown('### Datos oficiales online: Banco Mundial')
 rows,err,url=worldbank()
 if rows:
  d=pd.DataFrame(rows,columns=['Año','Usuarios de internet (%)']);latest=d.iloc[-1]
  st.metric('Perú · último año publicado',f'{latest.iloc[1]:.1f}%',help=f'Año {int(latest.iloc[0])}; indicador contextual, no demanda de NEXDATA')
  fig=px.area(d.tail(18),x='Año',y='Usuarios de internet (%)',color_discrete_sequence=['#2bd5cb'])
  st.plotly_chart(layout(fig,340),use_container_width=True)
  st.caption(f'Banco Mundial | IT.NET.USER.ZS | Año de dato: {int(latest.iloc[0])} | Consultado: {datetime.now():%Y-%m-%d} | {url}')
 else:st.error(f'No se pudo obtener la fuente online: {err}');st.markdown(f'[Consultar API]({url})')
 st.markdown('Fuentes: [Banco Mundial](https://data.worldbank.org/indicator/IT.NET.USER.ZS?locations=PE) · [Balanced Scorecard Institute](https://balancedscorecard.org/bsc-basics/) · [INEI](https://www.inei.gob.pe/)')
 st.caption('El uso de internet contextualiza la digitalización del país; no demuestra la demanda comercial de NEXDATA.')
 st.markdown('### Diagnóstico estratégico automático · sin pagos ni API')
 st.caption('El análisis utiliza los KPI editables de esta sesión y reglas transparentes; no es IA generativa.')
 pending=score[score['Estado']=='Pendiente'].sort_values('Cumplimiento relativo (%)')
 if pending.empty:
  st.success('Las cuatro perspectivas alcanzan sus metas actuales. Corresponde mantener el seguimiento y validar los datos con evidencia.')
 else:
  st.markdown(f'**{len(pending)} de {len(score)} perspectivas requieren acciones correctivas.**')
  for _,r in pending.iterrows():
   gap=round(r['Meta (%)']-r['Actual (%)'],2)
   with st.expander(f"{r['Dimensión']} · brecha {gap:.1f} puntos porcentuales",expanded=False):
    st.write(f"**Objetivo:** {r['Objetivo del plan']}")
    st.write(f"**Resultado:** {r['Actual (%)']:.1f}% | **Meta:** {r['Meta (%)']:.1f}% | **Responsable:** {r['Responsable']}")
    st.write(f"**Acción correctiva sugerida:** {RECOMMEND[r['Dimensión']]}")
    st.write('**Control:** revisar el indicador en el siguiente corte y registrar evidencia de ejecución.')
 st.info('Para la exposición: modifica ingresos, clientes, disponibilidad o capacitación en el panel lateral y observa cómo cambian las prioridades automáticamente.')
with tabs[6]:
 st.subheader('Matriz BSC, acciones y exportación')
 st.write('Los valores y metas se editan en la barra lateral. Las iniciativas pueden editarse directamente en la siguiente tabla.')
 edited=st.data_editor(st.session_state.actions_seed,num_rows='dynamic',hide_index=True,use_container_width=True,key='actions_editor',column_config={'Estado':st.column_config.SelectboxColumn('Estado',options=['Planificado','En ejecución','Completado','En riesgo'])})
 st.caption('Las modificaciones de esta tabla se mantienen durante la sesión. Descarga el archivo para conservarlas después de cerrar la aplicación.')
 st.dataframe(score,hide_index=True,use_container_width=True)
 st.download_button('Descargar indicadores (CSV)',score.to_csv(index=False).encode('utf-8-sig'),file_name='NEXDATA_BSC_KPI.csv',mime='text/csv')
 st.download_button('Descargar iniciativas editadas (CSV)',edited.to_csv(index=False).encode('utf-8-sig'),file_name='NEXDATA_BSC_iniciativas.csv',mime='text/csv')
 snapshot={'fecha':datetime.now().isoformat(timespec='seconds'),'valores':v,'metas':target,'kpi':score.to_dict('records'),'iniciativas':edited.to_dict('records')}
 st.download_button('Descargar respaldo completo (JSON)',json.dumps(snapshot,ensure_ascii=False,indent=2).encode('utf-8'),file_name='NEXDATA_BSC_respaldo.json',mime='application/json')
 uploaded=st.file_uploader('Restaurar indicadores y metas desde un respaldo JSON',type=['json'])
 if uploaded is not None and st.button('Restaurar respaldo'):
  try:
   content=json.load(uploaded)
   for k in FIELDS:
    if k in content.get('valores',{}):st.session_state['live_'+k]=content['valores'][k]
   for k in DEFAULT_TARGET:
    if k in content.get('metas',{}):st.session_state['goal_'+k]=content['metas'][k]
   if 'iniciativas' in content:st.session_state.actions_seed=pd.DataFrame(content['iniciativas']);st.session_state.pop('actions_editor',None)
   st.rerun()
  except Exception as exc:st.error(f'Respaldo inválido: {exc}')
