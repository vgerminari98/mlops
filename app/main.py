import os
import json
import mlflow
import uvicorn
import numpy as np
from pydantic import BaseModel
from fastapi import FastAPI


class FetalHealthData(BaseModel):
    accelerations: float
    fetal_movement: float
    uterine_contractions: float
    severe_decelerations: float

app = FastAPI(title="Fetal Health API",
              openapi_tags=[
              {
                "name" : "Health",
                "description" : "Get api health"
              }, 
              {
                "name" : "Prediction",
                "description" : "Model prediction"
              }]
              )

def load_model():
    print('reading envs')
    MLFLOW_TRACKING_URI = 'https://dagshub.com/vgerminari98/mlops-ead.mlflow'
    MLFLOW_TRACKING_USERNAME = 'vgerminari98'
    MLFLOW_TRACKING_PASSWORD = 'a0ddc5d0f5eff4309f6778a01dcfd861bdc75d8c'
    print('read')
    os.environ['MLFLOW_TRACKING_USERNAME'] = MLFLOW_TRACKING_USERNAME
    os.environ['MLFLOW_TRACKING_PASSWORD'] = MLFLOW_TRACKING_PASSWORD
    print('setting mlflow ...')
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    print('creating client')
    client = mlflow.MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
    print('getting registered model')
    registered_model = client.get_registered_model('fetal_health')
    print('read model')
    run_id = registered_model.latest_versions[-1].run_id
    logged_model = f'runs:/{run_id}/model'
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    print(load_model)
    return loaded_model

@app.on_event(event_type='startup')
def startup_event():
    global loaded_model
    loaded_model = load_model()


@app.get(path='/', tags=['Health'])
def api_health():
    return {"status": "healthy"}


@app.post(path='/predict', tags=['Prediction'])
def predict(request: FetalHealthData):
    global loaded_model

    received_data = np.array([
        request.accelerations,
        request.fetal_movement,
        request.uterine_contractions,
        request.severe_decelerations,
    ]).reshape(1, -1)

    prediction = loaded_model.predict(received_data)
    print(prediction)

    if loaded_model:
        return {"status": 200,
                "prediction": str(np.argmax(prediction[0]))}
    else:
        return {"status": 400}
