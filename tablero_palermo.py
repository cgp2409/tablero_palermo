#instalación de paquetes 

import pandas as pd
import json
import streamlit as st
import pip
import gspread
import client 
from oauth2client.service_account import ServiceAccountCredentials

#credenciales de google-drive para hojas de calculo
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'] #definir scope
creds = ServiceAccountCredentials.from_json_keyfile_name('prueba-finca-palermo-0d0dae3feaea.json', scope) 

client = gspread.authorize(creds) # authorize the clientsheet 
sheet = client.open("prueba_palermo").sheet1   
data = sheet.get_all_records() 




