from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import requests
from django.conf import settings
from .forms import CarPredictionForm

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