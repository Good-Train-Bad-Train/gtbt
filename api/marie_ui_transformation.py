import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date
import requests

def ui_transformer(start_city, end_city, user_date, ice_name):
    """
    This function transforms user input into a DataFrame that's readable for the model
    to make the prediction.
    """

    # variables for model
    #['trip','mean_delay','weekday','sin_time','cos_time','sin_day','cos_day','public_holiday','covid_lockdown','
    # temp_max_combined', 'temp_min_combined','prcp_max_combined', 'snow_max_combined',
    # 'wspd_max_combined','wpgt_max_combined', 'coco_max_combined']

    start_city =  special_characters(start_city)
    end_city = special_characters(end_city)
    arrival_date = pd.to_datetime(user_date) ###KEEP user_date as STRING ! datetime object called arrival_date

    #1: trip
    trip = start_city + '-' + end_city

    #2: mean_delay
    mean_delay_df = pd.read_csv('api/data/mean_delay_ices.csv')
    mean_delay = mean_delay_df.mean_delay[mean_delay_df.zugnr == ice_name]

    #3: weekday
    weekday = arrival_date.day_name()

    #4:sin_time
    seconds_in_day = 24*60*60
    time = user_date.split(" ")[1]
    seconds = sum(x * int(t) for x, t in zip([3600, 60, 1], time.split(":")))
    sin_time = np.sin(2*np.pi*seconds/seconds_in_day)
    cos_time = np.cos(2*np.pi*seconds/seconds_in_day)

    #6:sin_day
    #7:cos_day
    days_in_year = 366
    day_of_year = int(arrival_date.strftime('%j'))
    sin_day = np.sin(2*np.pi*day_of_year/days_in_year)
    cos_day = np.cos(2*np.pi*day_of_year/days_in_year)

    #8:public_holiday
    public_holiday = 0

    #9:covid_lockdown
    covid_lockdown = 0


    return([trip,mean_delay,weekday,sin_time,cos_time,sin_day,cos_day,public_holiday,covid_lockdown])


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

if __name__ == "__main__":
    print(ui_transformer('München','Köln','2022-06-06 17:27','ICE 101'))
