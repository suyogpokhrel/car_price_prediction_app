from fastapi import FastAPI
import joblib

app = FastAPI(title="Car Price Prediction API")

model = joblib.load("car_price_model.pkl")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Car price prediction API is running"}