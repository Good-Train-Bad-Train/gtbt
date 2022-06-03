from numpy import cumprod
import numpy as np
import streamlit as st
import pandas as pd
import folium
import time
import datetime
from datetime import datetime, date, time
from streamlit_folium import folium_static
import openrouteservice
from openrouteservice import convert
import requests

'''
# good train bad train
'''
fare_estimate = 0

col0, col1 = st.columns(2)
with col0:
    pickup = st.selectbox(
        'Where are you taking the train?',
        ('Köln Hbf', 'München Hbf'))
with col1:
    dropoff = st.selectbox(
        'Where would you like to go?',
        ('München Hbf', 'Köln Hbf', ))


col3, col4, col5,col6,col7 = st.columns(5)
with col3:
    pickupdate = st.date_input('Date')
with col4:
    pickuptime = st.slider(
        "Time",
        value=(time(11, 30)))
if pickup == 'Köln Hbf':
    pickup_coord = [50.9432, 6.9586]
elif pickup == 'München Hbf':
    pickup_coord = [48.1403, 11.5600] 

if dropoff == 'Köln Hbf':
    dropoff_coord = [50.9432, 6.9586]
elif dropoff == 'München Hbf':
    dropoff_coord = [48.1403, 11.5600] 
with col5:
    center_button = st.button('Check prediction')

    '''


    '''
    
    if center_button:
        #pred_url = f'https://taxifare.lewagon.ai/predict?pickup_datetime={pickupdate} {pickuptime}&pickup_longitude={pickup_coord[1]}&pickup_latitude={pickup_coord[0]}&dropoff_longitude={dropoff_coord[1]}&dropoff_latitude={dropoff_coord[0]}&passenger_count={passengers}'
        #response = requests.get(pred_url)
        #amount = response.json().get("fare")

        #result = 12
        with col6:
            st.metric('Will it be delayed?',f"Yes")
        with col7:
            st.metric('Prediction confidence',f"80%")





#with col6:
#    st.metric('Fare estimate',f"${fare_estimate}")


### Map visualization

m = folium.Map(location=[51.1657, 10.4515], zoom_start=6, tiles ='cartodbpositron')#'Stamen Toner')#'openstreetmap')

# add marker for Liberty Bell
folium.Marker(
    pickup_coord, popup=pickup, tooltip='Start', icon=folium.Icon(color='blue', icon='fa-train')
).add_to(m)

folium.Marker(
    dropoff_coord, popup=dropoff, tooltip='Finish', icon=folium.Icon(color='red', icon='fa-train')
).add_to(m)

# call to render Folium map in Streamlit
folium_static(m)



