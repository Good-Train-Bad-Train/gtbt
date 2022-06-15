
![logo](http://goodtrainbadtrain.herokuapp.com/media/82fc3297c83d254d2eddf1a4df093b147d09e3a5666670ca98be86f3.png)

The experience of booking a train with Deutsche Bahn often requires guesswork. At the time of booking, you don't know if a train is usually delayed, or whether other information could help you make an informed decision about which train to choose. We developed a machine learning model to help people make better decisions for their train journeys in Germany.

## How it works

We gathered data of all train rides in the past 2 years between Cologne, Munich and Berlin and combined it with weather information for each ride. We then organized data into a format that could be understood by a machine learning model - for example, we encoded the time and date and name of the train -, and then trained it using more than 40 features. Because the past two years have been very unusual, we filtered data from Covid lockdown periods, and also flagged all major holidays so the model could understand special circumstances like those.

What is happening behind the scenes here is that we are sending the information you select to Deutsche Bahn, getting a list of journeys and then checking whether our model thinks you will catch a good or bad train. We do that by sending this info to our API, which gathers weather predictions from the future and combines that with other info we have about your ride, producing a prediction.

## Deploy

We developed our frontend with Streamlit, and deployed it with Heroku. Our API is hosted at GCP. Please check our site here: http://goodtrainbadtrain.herokuapp.com/

## About us

This project was developed by [Stefano Pupe](https://github.com/spupe), [Marie Macnee](https://github.com/mariemacnee), [Boris Bohsem](https://github.com/boribo7) and [Juan Cotrino](https://github.com/juancotrino) in a 2-week sprint as a requirement for the completion of a Data Science Bootcamp at Le Wagon. We would like to thank Deutsche Bahn, [meteostat.net](https://meteostat.net/en/) and Statweather for their APIs, Jose Aponte for the logo and [zugfinder.net](https://www.zugfinder.net/en/start) for the train dataset.
