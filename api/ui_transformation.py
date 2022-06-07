import numpy as np
import pandas as pd

from datetime import datetime, timedelta

import requests

def ui_transformer(start_city, end_city, user_date, ice):
    """
    This function transforms user input into a DataFrame that's readable for the model
    to make the prediction.

    - start_city: input(From where are you going?) ---> Drop down list (Köln, München)
    - end_city: input(Where are you going to?) ---> Drop down list (Köln, München)
    - weekday: input(When are you going?) ---> Calendar menu (no more than 8 days (?))
    """

    start_city =  special_characters(start_city)
    end_city = special_characters(end_city)

    #assert isinstance(user_date, str)

    # get weather forecast
    key = '7DYDYYY5GVYHQA52HXFQV5A5Y'

    start_date = pd.Timestamp(user_date).round('H')
    user_date_round_str = datetime.strftime(start_date, '%Y-%m-%d %H:%M')
    end_date = start_date + timedelta(1)

    start_date_str = datetime.strftime(start_date, '%Y-%m-%d')
    end_date_str = datetime.strftime(end_date, '%Y-%m-%d')

    weekday = start_date.weekday()
    month = start_date.month

    time_of_day = day_categories(start_date)

    stations_lat_lon = pd.read_csv('api/data/Deutsche_Bahn_Haltestellen.csv', usecols=['X', 'Y', 'NAME'])
    stations = ['Köln Hbf',
                'München Hbf',
                'Mannheim Hbf',
                'Stuttgart Hbf',
                'Würzburg Hbf',
                'Frankfurt(Main)Hbf',
                'Nürnberg Hbf',
                'Essen Hbf',
                'Hamburg Hbf',
                'Berlin Hbf',
                'Hannover Hbf',
                'Hagen Hbf',
                'Erfurt Hbf',
                'Göttingen'
                ]

    coco_forecast = pd.read_csv('goodtrainbadtrain/data/weather_coco_forecast.csv', sep=';')
    coco_forecast.set_index('Code', inplace=True)
    coco_forecast = coco_forecast.to_dict()['Weather Condition']
    coco_forecast

    new_classes_forecast = {
        '1': [29, 42, 43],
        '2': [2, 8, 9, 19, 20, 21, 24, 27, 28, 30, 31, 32, 33, 36, 38, 39, 40, 41],
        '3': [1, 4, 6, 11, 12, 14, 18, 23, 26, 35, 37],
        '4': [3, 5, 7, 10, 13, 15, 16, 17, 22, 25, 34]
    }

    weather_response = {}
    weather = {}

    for station in stations:
        lat = stations_lat_lon[stations_lat_lon['NAME'] == station]['Y'].mean()
        lon = stations_lat_lon[stations_lat_lon['NAME'] == station]['X'].mean()

        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{str(lat)},{str(lon)}/{start_date_str}/{end_date_str}"
        params = {'key': key,
                    'unitGroup': 'metric'}
        response = requests.get(url, params=params).json()

        weather_response[station] = response

        days_list = pd.date_range(start_date, end_date)
        variables = ['datetime', 'temp', 'precip', 'snow', 'windspeed', 'windgust', 'conditions']
        sw_f = pd.DataFrame(columns=variables)
        for i, _ in enumerate(days_list):
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

        weather[station] = sw_f.copy()

        weather[station]['coco'] = weather[station]['coco'].apply(lambda x: coco_func(x, coco_forecast, new_classes_forecast))
        weather[station].reset_index(inplace=True)
        weather[station]['time']  = pd.to_datetime(weather[station]['time'])

    # Build prediction dataframe
    X = pd.DataFrame({
        'trip': '-'.join([start_city, end_city]),
        'temp': weather[end_city + ' Hbf'][weather[end_city + ' Hbf']['time'] == user_date_round_str]['temp'],
        'prcp': weather[end_city + ' Hbf'][weather[end_city + ' Hbf']['time'] == user_date_round_str]['prcp'],
        'wspd': weather[end_city + ' Hbf'][weather[end_city + ' Hbf']['time'] == user_date_round_str]['wspd'],
        'wpgt': weather[end_city + ' Hbf'][weather[end_city + ' Hbf']['time'] == user_date_round_str]['wpgt'],
        'snow': weather[end_city + ' Hbf'][weather[end_city + ' Hbf']['time'] == user_date_round_str]['snow'],
        'coco': weather[end_city + ' Hbf'][weather[end_city + ' Hbf']['time'] == user_date_round_str]['coco'],
        'weekday': weekday,
        'month': month,
        'time_of_day':time_of_day
    })

    ['trip','mean_delay','weekday','sin_time','cos_time','sin_day','cos_day','public_holiday',
            'covid_lockdown','temp_oc_6', 'prcp_oc_6',
            'snow_oc_6', 'wspd_oc_6', 'wpgt_oc_6', 'coco_oc_6', 'temp_dc_6',
            'prcp_dc_6', 'snow_dc_6', 'wspd_dc_6', 'wpgt_dc_6', 'coco_dc_6',
            'temp_oc_12', 'prcp_oc_12', 'snow_oc_12', 'wspd_oc_12', 'wpgt_oc_12',
            'coco_oc_12', 'temp_dc_12', 'prcp_dc_12', 'snow_dc_12', 'wspd_dc_12',
            'wpgt_dc_12', 'coco_dc_12']

    return X

def special_characters(city):
    if city == 'Munchen':
        return 'München'
    elif city == 'Koln':
        return 'Köln'
    elif city == 'Wurzburg':
        return 'Würzburg'
    elif city == 'Nurnberg':
        return 'Nürnberg'
    elif city == 'Gottingen':
        return 'Göttingen'
    else:
        return city

def day_categories(day):
    time_of_day_cat = ['night', 'morning', 'afternoon', 'evening']
    if 0 < day.hour < 6:
        return time_of_day_cat[0]
    elif 6 < day.hour < 12:
        return time_of_day_cat[1]
    elif 12 < day.hour < 18:
        return time_of_day_cat[2]
    elif 18 < day.hour < 24:
        return time_of_day_cat[3]

def coco_func(x, coco_forecast, new_classes_forecast):
    x_list = x.split(', ')
    for k, v in coco_forecast.items():
        if v in x_list:
            for c, i in new_classes_forecast.items():
                if k in i:
                    return c
