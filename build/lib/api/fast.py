from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib

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
def predict(pickup_datetime, pickup_longitude, pickup_latitude, dropoff_longitude,
            dropoff_latitude, passenger_count):

    dict= {"key": "2013-07-06 17:18:00.000000119",
           "pickup_datetime": [str('2009-12-05 10:58:03 UTC')],
            "pickup_longitude": [float(pickup_longitude)],
            "pickup_latitude": [float(pickup_latitude)],
            "dropoff_longitude": [float(dropoff_longitude)],
            "dropoff_latitude": [float(dropoff_latitude)],
            "passenger_count": [int(passenger_count)]
            }
    X_pred = pd.DataFrame(dict)

    pipeline = joblib.load('model.joblib')
    y_pred = pipeline.predict(X_pred)

    return {"fare": y_pred[0]
            }

"%Y-%m-%d %H:%M:%S UTC"

if __name__ == "__main__":
    y_pred = predict('2009-12-05 10:58:03 UTC',
                     '73.950655',
                     '40.783282',
                     '-73.984365',
                     '40.769802',
                     '1')
    print(y_pred[0])


    #http://127.0.0.1:8000/predict?pickup_datetime=2013-07-06%2017:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=1
