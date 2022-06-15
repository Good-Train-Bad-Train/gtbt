from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
from api.ui_transformation import ui_transformer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}

#@app.get("/predict")
#def predict(start_city: list, end_city: list, user_date: list, ice: list):
#
#    dict_result = {}
#    for index in range(len(start_city)):
#        leg_dict = {}
#        X_pred = ui_transformer(start_city[index], end_city[index], user_date[index], ice[index]).reset_index(drop=True)
#        pipeline = joblib.load('model.joblib')
#        y_pred = pipeline.predict(X_pred)[0]
#        y_pred_proba = pipeline.predict_proba(X_pred)[0]
#        leg_dict['start_city'] = start_city[index]
#        leg_dict['end_city'] = end_city[index]
#        leg_dict['train'] = ice[index]
#        leg_dict['prediction'] = y_pred
#        leg_dict['probability'] = y_pred_proba
#        leg_dict['expected_conditions'] = X_pred.loc[0, 'coco_max_combined']
#        leg_dict['mean_delay'] = X_pred.loc[0, 'mean_delay']
#        dict_result[index] = leg_dict
#
#    return dict_result

@app.get("/predict")
def predict(start_city: str, end_city: str, user_date: str, ice: str):
    X_pred = ui_transformer(start_city, end_city, user_date, ice).reset_index(drop=True)
    pipeline = joblib.load('model.joblib')
    y_pred = pipeline.predict(X_pred)[0]
    if y_pred == 0:
        y_pred_proba = pipeline.predict_proba(X_pred)[0][0]
    elif y_pred == 1:
        y_pred_proba = pipeline.predict_proba(X_pred)[0][1]
    leg_dict = dict(
        start_city = start_city,
        end_city = end_city,
        train = ice,
        prediction = int(y_pred),
        probability = y_pred_proba,
        expected_weather_conditions = int(X_pred.loc[0, 'coco_max_combined']),
        mean_delay = float(X_pred.loc[0, 'mean_delay'])
    )

    return leg_dict

if __name__ == "__main__":

    #start_city = ['Koln','Mannheim']
    #end_city = ['Mannheim','Munchen']
    #user_date = ['2022-06-10 16:23:00',
    #             '2022-06-10 18:47:00']
    #ice = ['ICE 109', 'ICE 691']

    start_city = 'Koln'
    end_city = 'Mannheim'
    user_date = '2022-06-10 16:23:00'
    ice = 'ICE 109'

    y_pred = predict(start_city,
                     end_city,
                     user_date,
                     ice)

    print(y_pred)

#http://127.0.0.1:8000/predict?start_city=Munchen&end_city=Koln&user_date=2022-06-06 17:00
