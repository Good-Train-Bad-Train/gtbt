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

# @app.get("/predict")
# def predict(start_city: str, end_city: str, user_date: str):

#     X_pred = ui_transformer(start_city, end_city, user_date)
#     pipeline = joblib.load('model.joblib')
#     y_pred = pipeline.predict(X_pred)

#     return dict(Delay = int(y_pred[0]))

@app.get("/predict")
def predict(start_city: list, end_city: list, user_date: list, ice: list):

    dict_result = {}
    for index in range(len(start_city)):
        X_pred = ui_transformer(start_city[index], end_city[index], user_date[index], ice[index])
        pipeline = joblib.load('model.joblib')
        y_pred = pipeline.predict(X_pred)
        y_pred_proba = pipeline.predict_proba(X_pred)
        dict_result[index] = [y_pred, y_pred_proba, X_pred.coco_max_combined, X_pred.mean_delay]

    return dict_result #dict(Delay = int(y_pred[0]))

if __name__ == "__main__":

    start_city = ['Koln','Mannheim']
    end_city = ['Mannheim','Munchen']
    user_date = ['2022-06-10 16:23',
                 '2022-06-10 18:47']
    ice = ['ICE 109', 'ICE 691']

    y_pred = predict(start_city,
                     end_city,
                     user_date,
                     ice)
    print(y_pred)

#http://127.0.0.1:8000/predict?start_city=Munchen&end_city=Koln&user_date=2022-06-06 17:00
#
#
# &dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=1
