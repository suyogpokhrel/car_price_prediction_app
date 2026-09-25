from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


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