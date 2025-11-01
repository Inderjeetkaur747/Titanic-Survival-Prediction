from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

# Load the trained model and scaler
with open("random_forest_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)


# Define input schema
class Passenger(BaseModel):
    Pclass: int  # 1,2,3
    Sex: int  # 0 = female, 1 = male
    Age: float
    Fare: float
    Embarked: int  # 0 = C, 1 = Q, 2 = S
    IsAlone: int
    FamilySize: int


# Initialize FastAPI app
app = FastAPI(title="Titanic Survival Prediction API")


@app.get("/")
def root():
    return {"message": "Welcome to Titanic Survival Prediction API"}


@app.post("/predict")
def predict(passenger: Passenger):
    # Convert input to array
    data = np.array([[passenger.Pclass, passenger.Sex, passenger.Age,
                      passenger.Fare, passenger.Embarked,
                      passenger.IsAlone, passenger.FamilySize]])

    # Scale data
    data_scaled = scaler.transform(data)

    # Predict survival
    pred = model.predict(data_scaled)[0]
    prob = model.predict_proba(data_scaled)[0].tolist()

    return {
        "prediction": int(pred),  # 0 = Not Survived, 1 = Survived
        "probability": prob
    }
