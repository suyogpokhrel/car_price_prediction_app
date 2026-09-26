from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal
import joblib
import pandas as pd
import numpy as np

app = FastAPI(title="Car Price Prediction API")

model = joblib.load("car_price_model.pkl")
reference_df = pd.read_csv("reference_prices.csv")

USD_TO_NPR_RATE = 152.0  # approximate reference rate, update as needed
TRAINING_REFERENCE_YEAR = 2025  # must match df['car_age'] = 2025 - model_year used in training


class CarInput(BaseModel):
    brand: str
    model: str
    fuel_type: Literal["Diesel", "E85 Flex Fuel", "Gasoline", "Hybrid", "Plug-In Hybrid", "Unknown"]
    transmission: Literal["Automatic", "Automatic (Dual-Clutch)", "CVT", "Manual", "Unknown"]
    accident: Literal["At least 1 accident or damage reported", "None reported", "Unknown"]
    clean_title: Literal["Unknown", "Yes"]
    model_year: int = Field(..., ge=1980, le=2026)
    mileage: float = Field(..., ge=0)
    engine_hp: float = Field(..., ge=0)
    engine_liters: float = Field(..., ge=0)
    engine_cylinders: float = Field(..., ge=0)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Car price prediction API is running"}


@app.post("/predict")
def predict_price(car: CarInput):
    car_age = TRAINING_REFERENCE_YEAR - car.model_year
    log_milage = np.log1p(car.mileage)

    input_row = pd.DataFrame([{
        "brand": car.brand,
        "model": car.model,
        "fuel_type": car.fuel_type,
        "transmission": car.transmission,
        "accident": car.accident,
        "clean_title": car.clean_title,
        "car_age": car_age,
        "engine_hp": car.engine_hp,
        "engine_liters": car.engine_liters,
        "engine_cylinders": car.engine_cylinders,
        "log_milage": log_milage,
    }])

    log_price_pred = model.predict(input_row)[0]
    predicted_price_usd = float(np.expm1(log_price_pred))
    predicted_price_npr = predicted_price_usd * USD_TO_NPR_RATE

    preprocessor = model.named_steps["prep"]
    regressor = model.named_steps["rf"]

    feature_names = preprocessor.get_feature_names_out()
    importances = regressor.feature_importances_

    # Transform this specific input row so we know which one-hot columns are actually "on" for THIS car
    transformed_row = preprocessor.transform(input_row)
    if hasattr(transformed_row, "toarray"):
        transformed_row = transformed_row.toarray()
    active_values = transformed_row[0]

    active_features = [
        (name, imp) for name, imp, val in zip(feature_names, importances, active_values)
        if val != 0
    ]

    contributions = sorted(active_features, key=lambda x: x[1], reverse=True)[:5]

    feature_contributions = [
        {"feature": name, "importance": round(float(imp), 4)}
        for name, imp in contributions
    ]

        # "How this compares" — average price of similar cars (same brand, age within ±3 years)
    similar_cars = reference_df[
        (reference_df["brand"] == car.brand) &
        (reference_df["car_age"].between(car_age - 3, car_age + 3))
    ]

    if len(similar_cars) >= 3:
        comparison = {
            "available": True,
            "similar_car_count": int(len(similar_cars)),
            "average_price_usd": round(float(similar_cars["price"].mean()), 2),
            "predicted_vs_average_pct": round(
                ((predicted_price_usd - similar_cars["price"].mean()) / similar_cars["price"].mean()) * 100, 1
            ),
        }
    else:
        comparison = {"available": False, "similar_car_count": int(len(similar_cars))}

    return {
        "predicted_price_usd": round(predicted_price_usd, 2),
        "predicted_price_npr": round(predicted_price_npr, 2),
        "npr_rate_used": USD_TO_NPR_RATE,
        "feature_contributions": feature_contributions,
        "comparison": comparison,
    }