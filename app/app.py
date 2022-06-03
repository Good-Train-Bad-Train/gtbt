import streamlit as st
import requests
import datetime
'''
# Get your Taxi Fare
## -NEW YORK CITY-
'''

columns = st.columns(2)
date = st.date_input("Date of Ride", datetime.datetime(2012, 10, 6, 12, 10, 20))
time = st.time_input('Time of Ride', datetime.datetime(2012, 10, 6, 12, 10, 20))

#date_time = st.text_input('Date and time', '2012-10-06%2012:10:20')
pick_long = st.text_input('Pickup longitude', '40.7614327')
pick_lat = st.text_input('Pickup latitude', '-73.9798156')
drop_long = st.text_input('Dropoff longitude', '40.6513111')
drop_lat = st.text_input('Dropoff latitude', '-73.8803331')
passenger_count = st.text_input('Passenger count', '2')


import requests
pred_url = f'https://taxifare.lewagon.ai/predict?pickup_datetime={date} {time}&pickup_longitude={pick_long}&pickup_latitude={pick_lat}&dropoff_longitude={drop_long}&dropoff_latitude={drop_lat}&passenger_count={passenger_count}'
response = requests.get(pred_url)
amount = response.json().get("fare")
st.text(f'Your fare will be: {amount}$')
