from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib

from ui_transformation import ui_transformer

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

@app.get("/predict")
def predict(start_city, end_city, user_date):

    X_pred = ui_transformer(start_city, end_city, user_date)
    pipeline = joblib.load('model.joblib')
    y_pred = pipeline.predict(X_pred)

    return {"Delay": y_pred[0]}

if __name__ == "__main__":
    y_pred = predict('München',
                     'Köln',
                     '2022-06-06 17:00')
    print(y_pred)

#http://127.0.0.1:8000/predict?pickup_datetime=2013-07-06%2017:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=1
