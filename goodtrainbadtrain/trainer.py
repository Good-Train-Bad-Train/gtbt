import joblib
from termcolor import colored
import mlflow
from goodtrainbadtrain.preprocessor import create_preproc
from goodtrainbadtrain.data import get_data_from_gcp, clean_data
from goodtrainbadtrain.gcp import storage_upload
from goodtrainbadtrain.params import MLFLOW_URI, EXPERIMENT_NAME, BUCKET_NAME, MODEL_VERSION, MODEL_VERSION
from memoized_property import memoized_property
from mlflow.tracking import MlflowClient
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class Trainer(object):
    def __init__(self, X, y):
        """
            X: pandas DataFrame
            y: pandas Series
        """
        self.pipeline = None
        self.X = X
        self.y = y

    def set_pipeline(self):
        """defines the pipeline as a class attribute"""

        preproc_pipe = create_preproc()

        self.pipeline = Pipeline([
            ('preproc', preproc_pipe),
            ('linear_model', LinearRegression())
        ])

        #goodtrainbadtrain.model.initialize_model()

    def run(self):
        self.set_pipeline()
        self.mlflow_log_param("model", "Linear")
        self.pipeline.fit(self.X, self.y)

    def evaluate(self, X_test, y_test):
        """evaluates the pipeline on df_test and return the RMSE"""
        y_pred = self.pipeline.predict(X_test)
        rmse = compute_rmse(y_pred, y_test)
        self.mlflow_log_metric("rmse", rmse)
        return round(rmse, 2)

        #res = model.evaluate(X_val_preproc, y_val, verbose = 0)
        #print(f"RMLSE achieved after {epochs} epochs = {round(res**0.5,3)}")

    def save_model_locally(self):
        """Save the model into a .joblib format"""
        joblib.dump(self.pipeline, 'model.joblib')
        print(colored("model.joblib saved locally", "green"))

    def upload_model_to_gcp():
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(STORAGE_LOCATION)
        blob.upload_from_filename('model.joblib')


STORAGE_LOCATION = 'models/goodtrainbadtrain/model.joblib'

def save_model(reg):
    """method that saves the model into a .joblib file and uploads it on Google Storage /models folder
    HINTS : use joblib library and google-cloud-storage"""

    # saving the trained model to disk is mandatory to then beeing able to upload it to storage
    # Implement here
    joblib.dump(reg, 'model.joblib')
    print("saved model.joblib locally")

    # Implement here
    upload_model_to_gcp()
    print(f"uploaded model.joblib to gcp cloud storage under \n => {STORAGE_LOCATION}")


if __name__ == "__main__":
    df = get_data()
    #df = clean_data(df)
    y = df["fare_amount"]
    X = df.drop("fare_amount", axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    # Train and save model, locally and
    trainer = Trainer(X=X_train, y=y_train)
    trainer.set_experiment_name('xp2')
    trainer.run()
    rmse = trainer.evaluate(X_test, y_test)
    print(f"rmse: {rmse}")
    trainer.save_model_locally()
    storage_upload()

    ##code from adding model to GCP
    # get training data from GCP bucket
    df = get_data()
    # preprocess data
    X_train, y_train = preprocess(df)
    # train model (locally if this file was called through the run_locally command
    # or on GCP if it was called through the gcp_submit_training, in which case
    # this package is uploaded to GCP before being executed)
    reg = train_model(X_train, y_train)
    # save trained model to GCP bucket (whether the training occured locally or on GCP)
    save_model(reg)


# 1. Initializing a NeuralNet with its architecture and its compilation method
#model = initialize_model(X_train_preproc)
#model.summary()

# 2. Training the model
#epochs = 50
#batch_size = 16

#history = model.fit(X_train_preproc,
#                    y_train,
#                    validation_data = (X_val_preproc, y_val),
#                    epochs = epochs,         # Play with this until your validation loss overfit
#                    batch_size = batch_size, # Let's keep a small batch size for faster iterations
#                    verbose = 1)

# 3. Evaluating the model
#res = model.evaluate(X_val_preproc, y_val, verbose = 0)
#print(f"RMLSE achieved after {epochs} epochs = {round(res**0.5,3)}")

# 4. Looking at the lowest loss
#minimium_rmlse_val = min(history.history['val_loss'])**0.5
#optimal_momentum = np.argmin(history.history['val_loss'])

#print(f"Lowest RMLSE achieved = {round(minimium_rmlse_val,3)}")
#print(f"This was achieved at the epoch number {optimal_momentum}")
