import numpy as np
import pandas as pd

from datetime import datetime, timedelta

import requests

def ui_transformer(start_city, end_city, user_date):
    """
    This function transforms user input into a DataFrame that's readable for the model
    to make the prediction.

    - start_city: input(From where are you going?) ---> Drop down list (Köln, München)
    - end_city: input(Where are you going to?) ---> Drop down list (Köln, München)
    - weekday: input(When are you going?) ---> Calendar menu (no more than 8 days (?))
    """

    if isinstance(user_date == str):
        user_date = datetime.strptime(user_date, format='%Y-%m-%d %H:%M')

    assert isinstance(user_date == datetime)

    weekday = user_date.weekday()
    month = user_date.month

    time_of_day_cat = ['night', 'morning', 'afternoon', 'evening']
    if 0 < user_date.hour < 6:
        time_of_day = time_of_day_cat[0]
    elif 6 < user_date.hour < 12:
        time_of_day = time_of_day_cat[1]
    elif 12 < user_date.hour < 18:
        time_of_day = time_of_day_cat[2]
    elif 18 < user_date.hour < 24:
        time_of_day = time_of_day_cat[3]

    # get weather forecast
    key = '7DYDYYY5GVYHQA52HXFQV5A5Y'
    start_date = datetime.strftime(user_date, format='%Y-%m-%d')
    end_date = datetime.strftime(user_date + timedelta(1), format='%Y-%m-%d')

    stations_lat_lon = pd.read_csv('../raw_data/Deutsche_Bahn_Haltestellen.csv', usecols=['X', 'Y', 'NAME'])
    stations = ['Köln Hbf', 'München Hbf']

    weather_response = {}
    weather = {}

    for station in stations:
        lat = stations_lat_lon[stations_lat_lon['NAME'] == station]['Y'].mean()
        lon = stations_lat_lon[stations_lat_lon['NAME'] == station]['X'].mean()

        url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/" + str(lat) + "," + str(lon) + "/" + start_date + "/" + end_date + "?key=" + key + "&unitGroup=metric"
        response = requests.get(url).json()

        weather_response[station] = response

        days_list = pd.date_range(start_date, end_date)
        variables = ['datetime', 'temp', 'precip', 'snow', 'windspeed', 'windgust', 'conditions']
        sw_f = pd.DataFrame(columns=variables)
        d_c = 0
        for i, d in enumerate(days_list):
            for h in range(24):
                date = response['days'][i]['datetime']
                hour = datetime.strftime(pd.to_datetime(h, format='%H'), '%H:%M:%S')
                date = date + ' ' + hour
                sw_f.loc[h + h*i + 24*i, 'datetime'] = date
                for v in variables[1:]:
                    sw_f.loc[h + h*i + 24*i, v] = response['days'][i]['hours'][h][v]

        sw_f.rename(columns={'datetime': 'time',
                            'precip': 'prcp',
                            'windspeed': 'wspd',
                            'windgust': 'wpgt',
                            'conditions': 'coco'}, inplace=True)

        sw_f.set_index('time', inplace=True)

        weather[station] = sw_f

    coco_forecast = pd.read_csv('../raw_data/weather_coco_forecast.csv', sep=';')
    coco_forecast.set_index('Code', inplace=True)
    coco_forecast = coco_forecast.to_dict()['Weather Condition']
    coco_forecast

    new_classes_forecast = {
        'good': [29, 42, 43],
        'medium': [2, 8, 9, 19, 20, 21, 24, 27, 28, 30, 31, 32, 33, 36, 38, 39, 40, 41],
        'bad': [1, 4, 6, 11, 12, 14, 18, 23, 26, 35, 37],
        'extreme': [3, 5, 7, 10, 13, 15, 16, 17, 22, 25, 34]
    }

    reclass_forecast = {}
    for k, v in coco_forecast.items():
        for c, i in new_classes_forecast.items():
            if k in i:
                reclass_forecast[v] = c

    reclass_forecast = dict(sorted(reclass_forecast.items()))

    for station in stations:
        weather[station]['coco'] = weather[station]['coco'].map(reclass_forecast)
        weather[station].reset_index(inplace=True)
        weather[station]['time']  = pd.to_datetime(weather[station]['time'])

    # Build prediction dataframe
    X = pd.DataFrame({
        'trip': '-'.join([start_city, end_city]),
        'temp': weather[end_city + ' Hbf'][weather[end_city + ' Hbf']['time'] == user_date]['temp'],
        'prcp': weather[end_city + ' Hbf'][weather[end_city + ' Hbf']['time'] == user_date]['prcp'],
        'wspd': weather[end_city + ' Hbf'][weather[end_city + ' Hbf']['time'] == user_date]['wspd'],
        'wpgt': weather[end_city + ' Hbf'][weather[end_city + ' Hbf']['time'] == user_date]['wpgt'],
        'snow': weather[end_city + ' Hbf'][weather[end_city + ' Hbf']['time'] == user_date]['snow'],
        'coco': weather[end_city + ' Hbf'][weather[end_city + ' Hbf']['time'] == user_date]['coco'],
        'weekday': weekday,
        'month': month,
        'time_of_day':time_of_day
    })

    return X