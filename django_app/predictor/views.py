from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import requests
from django.conf import settings
from .forms import CarPredictionForm
from django.contrib.auth.decorators import login_required
from .models import PredictionHistory
from django.shortcuts import get_object_or_404

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

