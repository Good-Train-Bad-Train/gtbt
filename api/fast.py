from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
from api.ui_transformation import ui_transformer
# from api.ui_transformation_presentation import ui_transformer

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
def predict(start_city: str, end_city: str, user_date: str, ice: str):

    start_city = start_city.split(',')
    end_city =end_city.split(',')
    user_date = user_date.split(',')
    ice= ice.split(',')

    start_city_output = []
    end_city_output = []
    train_output = []
    prediction_output = []
    probability_output = []
    expected_weather_conditions_output = []
    mean_delay_output = []

    mean_delay_df = pd.read_csv('api/data/mean_delay_ices.csv')

    for index in range(len(start_city)):

        if ice[index] in mean_delay_df.zugnr.to_list():
            ice_fix = ice[index]
        else:
            ice_fix = 'ICE 109'

        X_pred = ui_transformer(start_city[index], end_city[index], user_date[index], ice_fix).reset_index(drop=True)
        pipeline = joblib.load('model.joblib')
        y_pred = pipeline.predict(X_pred)[0]
        if y_pred == 0:
            y_pred_proba = pipeline.predict_proba(X_pred)[0][0]
        elif y_pred == 1:
            y_pred_proba = pipeline.predict_proba(X_pred)[0][1]

        start_city_output.append(start_city[index])
        end_city_output.append(end_city[index])
        train_output.append(ice_fix)
        prediction_output.append(str(int(y_pred)))
        probability_output.append(str(y_pred_proba))
        expected_weather_conditions_output.append(str(int(X_pred.loc[0, 'coco_max_combined'])))
        mean_delay_output.append(str(float(X_pred.loc[0, 'mean_delay'])))


    start_city_output = ','.join(start_city_output)
    end_city_output = ','.join(end_city_output)
    train_output = ','.join(train_output)
    prediction_output = ','.join(prediction_output)
    probability_output = ','.join(probability_output)
    expected_weather_conditions_output = ','.join(expected_weather_conditions_output)
    mean_delay_output = ','.join(mean_delay_output)


    leg_dict = dict(
        start_city = start_city_output,
        end_city = end_city_output,
        train = train_output,
        prediction = prediction_output,
        probability = probability_output,
        expected_weather_conditions = expected_weather_conditions_output,
        mean_delay = mean_delay_output
    )

    return leg_dict

if __name__ == "__main__":

    start_city = 'Koln,Koln'
    end_city = 'Mannheim,Mannheim'
    user_date = '2022-06-10 16:23:00,2022-06-10 16:23:00'
    ice = 'ICE 109,ICE 109'

    y_pred = predict(start_city,
                     end_city,
                     user_date,
                     ice)

    print(y_pred)
