from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import requests
from django.conf import settings
from .forms import CarPredictionForm
from django.contrib.auth.decorators import login_required
from .models import PredictionHistory
from django.shortcuts import get_object_or_404
import json
import os


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('predict')  # we'll create this page next phase
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'predictor/signup.html', {'form': form})

def predict_view(request):
    result = None
    error = None

    if request.method == 'POST':
        form = CarPredictionForm(request.POST)
        if form.is_valid():
            payload = form.cleaned_data
            try:
                response = requests.post(
                    f"{settings.FASTAPI_BASE_URL}/predict",
                    json=payload,
                    timeout=10,
                )
                if response.status_code == 200:
                    result = response.json()

                    PredictionHistory.objects.create(
                        user=request.user,
                        brand=payload['brand'],
                        model_name=payload['model'],
                        model_year=payload['model_year'],
                        mileage=payload['mileage'],
                        fuel_type=payload['fuel_type'],
                        transmission=payload['transmission'],
                        accident=payload['accident'],
                        clean_title=payload['clean_title'],
                        engine_hp=payload['engine_hp'],
                        engine_liters=payload['engine_liters'],
                        engine_cylinders=payload['engine_cylinders'],
                        predicted_price_usd=result['predicted_price_usd'],
                        predicted_price_npr=result['predicted_price_npr'],
                    )
                else:
                    error = f"Prediction service returned an error: {response.status_code}"
            except requests.exceptions.ConnectionError:
                error = "Could not reach the prediction service. Is FastAPI running?"
    else:
        form = CarPredictionForm()

    return render(request, 'predictor/predict.html', {
        'form': form,
        'result': result,
        'error': error,
    })

def history_view(request):
    predictions = PredictionHistory.objects.filter(user=request.user)
    return render(request, 'predictor/history.html', {'predictions': predictions})


def delete_history_view(request, pk):
    prediction = get_object_or_404(PredictionHistory, pk=pk, user=request.user)
    if request.method == 'POST':
        prediction.delete()
        return redirect('history')
    return render(request, 'predictor/confirm_delete.html', {'prediction': prediction})


def model_insights_view(request):
    model_comparison = [
        {'name': 'Linear Regression', 'r2': 0.7441, 'mae': 0.2637},
        {'name': 'Random Forest', 'r2': 0.8228, 'mae': 0.2285},
        {'name': 'Gradient Boosting', 'r2': 0.8214, 'mae': 0.2313},
    ]

    feature_importance = [
        {'feature': 'log_milage', 'importance': 0.5094},
        {'feature': 'engine_hp', 'importance': 0.1788},
        {'feature': 'car_age', 'importance': 0.1282},
        {'feature': 'engine_liters', 'importance': 0.0518},
        {'feature': 'brand_Porsche', 'importance': 0.0133},
        {'feature': 'brand_Lamborghini', 'importance': 0.0104},
        {'feature': 'brand_Rolls-Royce', 'importance': 0.0053},
        {'feature': 'transmission_Dual-Clutch', 'importance': 0.0050},
        {'feature': 'engine_cylinders', 'importance': 0.0044},
        {'feature': 'fuel_type_Diesel', 'importance': 0.0038},
    ]

    data_path = os.path.join(os.path.dirname(__file__), 'model_insights_data.json')
    with open(data_path) as f:
        insights_data = json.load(f)

    return render(request, 'predictor/model_insights.html', {
        'model_comparison': model_comparison,
        'feature_importance': feature_importance,
        'deployed_model': 'Random Forest',
        'actual_vs_predicted': insights_data['actual_vs_predicted'],
        'price_distribution': insights_data['price_distribution'],
    })