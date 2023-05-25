#---------------------------------------------------
#IMPORTE DE LIBRERIAS
#---------------------------------------------------
import pandas as pd
import json
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import gspread
import plotly.graph_objects as go
#import client 


st.set_page_config(layout="wide") #streamlit modo ancho
 
datajson = open('credencialdrive.json','a') 

from oauth2client.service_account import ServiceAccountCredentials
#pip.main(["install", "client"])
#credenciales de google-drive para hojas de calculo
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'] #definir scope
creds = ServiceAccountCredentials.from_json_keyfile_name('credencialdrive.json', scope) 

client = gspread.authorize(creds) # authorize the clientsheet 
sheet = client.open("datos_palermo").sheet1   
data = sheet.get_all_records() 

df_inicial=pd.DataFrame(data)
df_inicial.drop('Marca temporal', inplace=True, axis=1)
df_inicial.columns = df_inicial.columns.str.replace(' ', '_')
df_inicial = df_inicial.convert_dtypes()
df_inicial["Kilogramos_vendidos"] = df_inicial.Kilogramos_vendidos.replace('',np.nan,regex = True)
df_inicial["Precio_de_kilogramo"] = df_inicial.Precio_de_kilogramo.replace('',np.nan,regex = True)
df_inicial["Cantidad"] = df_inicial.Cantidad.replace('',np.nan,regex = True)
df_inicial["Kilogramos_vendidos"] = df_inicial["Kilogramos_vendidos"].astype(float)
df_inicial["Precio_de_kilogramo"] = df_inicial["Precio_de_kilogramo"].astype(float)
df_inicial["Cantidad"] = df_inicial["Cantidad"].astype(float)
df_inicial['Fecha'] = pd.to_datetime(df_inicial['Fecha'], format='%d/%m/%Y')

df_inicial["Etiqueta_de_gasto"] = df_inicial.Etiqueta_de_gasto.replace('','Sin asignar',regex = True)


#--------------------------------------------------
#STREAMLIT
#---------------------------------------------------


# Mostrar encabezado
# Configurar el diseño de la página en dos columnas

# Mostrar encabezado centrado
st.markdown("<h3 style='text-align: center; color: black;'>Gastos Totales </h3>", unsafe_allow_html=True)

# Dividir la página en dos columnas
col1, col2 = st.columns(2)

# Configurar el tamaño y la posición del gráfico en la mitad izquierda de la pantalla
with col1:
    # Gráfico de pastel
    gastos_totales = df_inicial.loc[df_inicial['Tipo_de_dato'] != 'Ingreso de dinero']
    fig = px.pie(gastos_totales, values='Cantidad', names='Etiqueta_de_gasto',
                 title='Porcentaje de gastos por etiqueta', color_discrete_sequence=px.colors.qualitative.G10)
    st.plotly_chart(fig, use_container_width=True)

# Colocar contenido adicional en la mitad derecha de la pantalla (col2)
with col2:
    
    # Filtrar los datos por etiquetas de gasto y tipo de datos
    gastos_totales = df_inicial[df_inicial['Tipo_de_dato'] != 'Ingreso de dinero']
    
    # Agrupar los datos por etiquetas de gasto y origen del dinero
    grouped_data = gastos_totales.groupby(['Etiqueta_de_gasto', 'Tipo_de_dato'])['Cantidad'].sum().reset_index()
    
    # Crear un diccionario para mapear el origen del dinero a un color
    colors = {'Inversiones de Hermidez': 'rgb(255, 0, 0)',
              'Inversiones de Felipe': 'rgb(0, 255, 0)',
              'Gasto general de dinero': 'rgb(0, 0, 255)'}
    
    # Configurar el diseño del gráfico de barras
    fig = go.Figure()
    
    # Agregar cada barra al gráfico con el color correspondiente
    for tipo_dato, color in colors.items():
        data = grouped_data[grouped_data['Tipo_de_dato'] == tipo_dato]
        fig.add_trace(go.Bar(x=data['Etiqueta_de_gasto'], y=data['Cantidad'], name=tipo_dato, marker_color=color))
    
    # Configurar los títulos de los ejes y el título del gráfico
    fig.update_layout(xaxis_title='Etiqueta de gasto', yaxis_title='Cantidad', title='Proporción de gastos por etiqueta')
    
    # Mostrar el gráfico de barras en Streamlit
    st.plotly_chart(fig, use_container_width=True)
