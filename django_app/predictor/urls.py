from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.predict_view, login_url='login'), name='predict'),
    path('history/', login_required(views.history_view, login_url='login'), name='history'),
    path('history/delete/<int:pk>/', login_required(views.delete_history_view, login_url='login'), name='delete_history'),
    path('login/', auth_views.LoginView.as_view(template_name='predictor/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('insights/', login_required(views.model_insights_view, login_url='login'), name='model_insights'),
]