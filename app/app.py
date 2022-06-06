### TODO: Implement color change when leg is delayed
# Implement weight change if trip is selected
# Implement main dashboard function
# Create more data visualization features

### Imports and functions

from numpy import cumprod
import numpy as np
import streamlit as st
import pandas as pd
import folium
import time
import datetime as dt
from datetime import datetime, date, time, timedelta
from streamlit_folium import folium_static
from pyhafas import HafasClient
from pyhafas.profile import VSNProfile
#from pyhafas.profile import DBProfile
#from pyhafas.types.fptf import Leg


@st.cache
def create_journeydf(journeylist):

    journey_start = []
    journey_end = []    
    journey_origin = []
    journey_destination = []
    journey_numberlegs = []
    leg1_train = []
    leg1_destination = []
    leg2_train = []
    leg2_destination = []
    leg3_train = []
    leg3_destination = []
  
    for journey in journeylist:
        journey_origin.append(journey.legs[0].origin.name)
        journey_destination.append(journey.legs[-1].destination.name)
        journey_start.append(journey.legs[0].departure.strftime("%H:%M"))
        journey_end.append(journey.legs[-1].arrival.strftime("%H:%M"))
        journey_numberlegs.append(len(journey.legs))
        leg1_train.append(journey.legs[0].name)
        leg1_destination.append(journey.legs[0].destination.name)
        
        if len(journey.legs) == 1:
            leg2_train.append(' ')
            leg2_destination.append(' ')
            leg3_train.append(' ')
            leg3_destination.append(' ')
        elif len(journey.legs) == 2:
            leg2_train.append(journey.legs[1].name)
            leg2_destination.append(journey.legs[1].destination.name)
            leg3_train.append(' ')
            leg3_destination.append(' ')
        elif len(journey.legs) == 3:
            leg2_train.append(journey.legs[1].name)
            leg2_destination.append(journey.legs[1].destination.name)
            leg3_train.append(journey.legs[2].name)
            leg3_destination.append(journey.legs[2].destination.name)
        elif len(journey.legs) == 4: #there are somehow some trips with four stops, I'm filtering those out later
            leg2_train.append(' ')
            leg2_destination.append(' ')
            leg3_train.append(' ')
            leg3_destination.append(' ')

    journeydf = pd.DataFrame(columns = ['Start','End','Origin','Destination','Connections', 'Leg1_Dest', 'Leg2_Dest', 'Leg3_Dest'])

    journeydf.Start = journey_start
    journeydf.End = journey_end 
    journeydf.Origin = journey_origin
    journeydf.Destination = journey_destination
    journeydf.Connections = journey_numberlegs            
    journeydf.Leg1_Dest = leg1_destination
    journeydf.Leg2_Dest = leg2_destination
    journeydf.Leg3_Dest = leg3_destination
    journeydf.Origin.replace('Köln Messe/Deutz Gl.11-12', 'Köln Messe',inplace=True)
    journeydf.Destination.replace('Köln Messe/Deutz Gl.11-12', 'Köln Messe',inplace=True)
    journeydf.Destination.replace('Köln Messe/Deutz Gl.11-12', 'Köln Messe',inplace=True)
    journeydf = journeydf.sort_values(by=['Connections']) # Sort so that trains with fewer connections get listed first - we can later sort by our model predictions
    journeydf = journeydf.reset_index(drop=True)
    
    return journeydf

# @st.cache # st cache doesn't work with map object, at least so far
def create_map(coordlist1,coordlist2,coordlist3):

    m = folium.Map(width=1000,height=500,location=[50.5657, 11.8515], zoom_start=6, tiles ='Cartodb dark_matter')#'cartodbpositron')#'Stamen Toner')#'openstreetmap')

    normalweight=4
    selectedweight=6
    if checkbox1:
        aline1=folium.PolyLine(locations=leglist1,weight=selectedweight,color = '#E55635')  
    else:
        aline1=folium.PolyLine(locations=leglist1,weight=normalweight,color = '#E55635')
    if checkbox2:
        aline2=folium.PolyLine(locations=leglist2,weight=selectedweight,color = '#EC9706')
    else:
        aline2=folium.PolyLine(locations=leglist2,weight=normalweight,color = '#EC9706')
    if checkbox3:
        aline3=folium.PolyLine(locations=leglist3,weight=selectedweight,color = '#7A3803')
    else:
        aline3=folium.PolyLine(locations=leglist3,weight=normalweight,color = '#7A3803')
    m.add_child(aline1)
    m.add_child(aline2)
    m.add_child(aline3)

    for i in leglist1:
        folium.CircleMarker(location=[i[0], i[1]],
                            radius=5,
                            color='blue',
                            fill_color='blue',
                            fill=True).add_to(m)
        coords = i

    for i in leglist2:
        folium.CircleMarker(location=[i[0], i[1]],
                            radius=5,
                            color='purple',
                            fill_color='purple',
                            fill=True).add_to(m)

    for i in leglist3:
        folium.CircleMarker(location=[i[0], i[1]],
                            radius=5,
                            color='orange',
                            fill_color='orange',
                            fill=True).add_to(m)
    return m



### Main
st.set_page_config(page_title='Good Train Bad Train', page_icon='gtbt_good.png', layout="centered", initial_sidebar_state="auto", menu_items=None)
st.image('gtbtlogo_black.png')

client = HafasClient(VSNProfile())
m = folium.Map(width=800,height=500,location=[50.5657, 11.8515], zoom_start=6, tiles ='Cartodb dark_matter')#'cartodbpositron')#'Stamen Toner')#'openstreetmap')
pickup_coord = [50.9432, 6.9586]
dropoff_coord = [48.1403, 11.5600]

st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(229, 86, 53);
}
</style>""", unsafe_allow_html=True)

tomorrowdate = datetime.now() + timedelta(days=1)
maxdate = datetime.now() + timedelta(days=365)
datetodisplay = tomorrowdate.date()

col0, col1,col3,col4,col5 = st.columns([4,4,3,3,1])
with col0:
    pickup = st.selectbox(
        'From',
        ('Köln Hbf', 'Köln Messe', 'München Hbf'))
with col1:
    dropoff = st.selectbox(
        'To',
        ('München Hbf', 'Köln Hbf', 'Köln Messe'))
with col3:
    pickupdate = st.date_input('Date', value=datetodisplay,min_value=datetime.now(),max_value = maxdate)
with col4:
    pickuptime = st.slider(
        "Time",
        value=(time(14, 00)))
with col5:
    st.image('blackpadding.png',width=30)
    center_button = st.button('Search')

date_time_obj = dt.datetime.combine(pickupdate, pickuptime)
origin = client.locations(pickup)[0]
destination = client.locations(dropoff)[0]

if center_button:
    #display_dashboard() # Need to implement a function that does all the below, and gets activated on checkboxchange as well
    origin = client.locations(pickup)[0]
    destination = client.locations(dropoff)[0]
    journeys = client.journeys(
    origin=origin,
    destination=destination,
    date=date_time_obj,
    max_changes=2,
    min_change_time=10,
    max_journeys=-1,
        products={
        'long_distance_express': True,
        'regional_express': False,
        'regional': False,
        'suburban': False,
        'bus': False,
        'ferry': False,
        'subway': False,
        'tram': False,
        'taxi': False
    })

    journeydf = create_journeydf(journeys)
    #print(journeydf)

    string1 = f'{journeydf.Origin[0]} ({journeydf.Start[0]}) to {journeydf.Destination[0]} ({journeydf.End[0]}), with {journeydf.Connections[0]-1} connections'
    string2 = f'{journeydf.Origin[1]} ({journeydf.Start[1]}) to {journeydf.Destination[1]} ({journeydf.End[1]}), with {journeydf.Connections[1]-1} connections'
    string3 = f'{journeydf.Origin[2]} ({journeydf.Start[2]}) to {journeydf.Destination[2]} ({journeydf.End[2]}), with {journeydf.Connections[2]-1} connections'
       
    colcheck11,colcheck12,colcheck13,colcheck14 =st.columns([1,10,3,1])
    with colcheck11:
        st.image('gtbt_icon_blue.png',width=15)
    with colcheck12:
        checkbox1 = st.checkbox(string1,value = True) 
    with colcheck13:
        st.markdown("""
        <font color='green'>
        No delays</font>""",unsafe_allow_html=True)
    with colcheck14:
        st.image('gtbt_good_green.png',width=20)
  
    colcheck21,colcheck22,colcheck23,colcheck24 =st.columns([1,10,3,1])   
    with colcheck21:
        st.image('gtbt_icon_yellow.png',width=15)
    with colcheck22:
        checkbox2 = st.checkbox(string2,value = False)
    with colcheck23:
        st.markdown("""
        <font color='green'>
        Small delay</font>""",unsafe_allow_html=True)
    with colcheck24:
        st.image('gtbt_good_green.png',width=20)
        
    colcheck31,colcheck32,colcheck33,colcheck34 =st.columns([1,10,3,1])   
    with colcheck31:
        st.image('gtbt_icon_purple.png',width=15)  
    with colcheck32:
        checkbox3 = st.checkbox(string3,value=False)
    with colcheck33:
        st.markdown("""
        <font color='red'>
        Missed connection</font>""",unsafe_allow_html=True)
    with colcheck34:
        st.image('gtbt_bad_red.png',width=20)
    
    querydate = date_time_obj.strftime("%Y/%m/%d, %H:%M")
    querydate = str(querydate).replace(',','')
    querydate = str(querydate).replace('/','-')
    pred_url = f'https://gtbt3image-4muwooak2q-ew.a.run.app/predict?start_city={pickup}&end_city={dropoff}&user_date={querydate}'                
    #response = requests.get(pred_url)
    #delay = response.json().get("Delay")

    leglist = [journeydf.Origin,journeydf.Leg1_Dest,journeydf.Leg2_Dest,journeydf.Leg3_Dest]
    leglist1 = [leglist[0][0],leglist[1][0],leglist[2][0],leglist[3][0],' '] # We are adding ' ' for the trick below
    leglist2 = [leglist[0][1],leglist[1][1],leglist[2][1],leglist[3][1],' ']
    leglist3 = [leglist[0][2],leglist[1][2],leglist[2][2],leglist[3][2],' ']
    leglist1 = leglist1[0:leglist1.index(' ')] # Find out where ' ' first appears in the list, and the position before that is the end destination, and you can work from there. Useful for coordinates
    leglist2 = leglist2[0:leglist2.index(' ')]
    leglist3 = leglist3[0:leglist3.index(' ')]
    my_dict = {'Köln Hbf': [50.9432, 6.9586], 
                'Köln Messe': [50.9469, 6.9832], 'Köln Messe/Deutz Gl.11-12': [50.9469, 6.9832],
                'München Hbf': [48.1403, 11.5600], 'Mannheim Hbf': [49.4796, 8.4699],
                'Frankfurt(Main) Flughafen Fernbf': [50.0529, 8.5698],'Stuttgart Hbf':[48.7832, 9.1823], 
                'Nürnberg Hbf': [49.4456, 11.0825]}
    leglist1[:]=[my_dict.get(e,'') for e in leglist1]
    leglist2[:]=[my_dict.get(e,'') for e in leglist2]
    leglist3[:]=[my_dict.get(e,'') for e in leglist3]

    m = create_map(leglist1,leglist2,leglist3)

    folium_static(m)





