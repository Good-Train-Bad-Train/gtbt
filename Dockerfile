FROM python:3.8.6-buster
COPY model.joblib /model.joblib
COPY goodtrainbadtrain /goodtrainbadtrain
COPY requirements.txt /requirements.txt
COPY api /api
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn api.fast:app --host 0.0.0.0
