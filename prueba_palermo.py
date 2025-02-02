#base de datos0
import pandas as pd
import json
with open('credencialdrive.json','r') as sampledata:
    datajson = json.load(sampledata)
import streamlit as st
import pip
import gspread
pip.main(["install", "client"])
from oauth2client.service_account import ServiceAccountCredentials
# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('credencialdrive.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

sheet = client.open("datos_palermo").sheet1   
data = sheet.get_all_records() 
print(data)

df=pd.DataFrame(data)
df = df.drop(['Marca temporal'],axis=1)
print(df)
df['fecha'] = pd.to_datetime(df['Fecha']) # convertir fecha a formato fecha 
df = df.drop(['Fecha'],axis=1)
pd.to_numeric(df['Cantidad'])

"""fig = df.groupby(['Tipo de aporte']).sum().plot(kind='pie', y='Cantidad')"""
st.markdown("<h3 style='text-align: center; color: black;'>Grafico 1 </h3>", unsafe_allow_html=True)

import plotly.express as px
fig = px.pie(df, values = 'Cantidad', names ='Etiqueta de gasto',
             title= 'Porcentaje',
             color_discrete_sequence=px.colors.qualitative.G10)
fig.update_layout(
    xaxis_title = 'Numero de hurtos',
    yaxis_title = 'Arma empleada',
    template = 'simple_white',
    title_x = 0.1)
st.write(fig)
