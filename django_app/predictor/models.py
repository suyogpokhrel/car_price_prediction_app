from django.db import models
from django.contrib.auth.models import User


class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.CharField(max_length=50)
    model_name = models.CharField(max_length=100)
    model_year = models.IntegerField()
    mileage = models.FloatField()
    fuel_type = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    accident = models.CharField(max_length=100)
    clean_title = models.CharField(max_length=20)
    engine_hp = models.FloatField()
    engine_liters = models.FloatField()
    engine_cylinders = models.FloatField()
    predicted_price_usd = models.FloatField()
    predicted_price_npr = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model_name} ({self.model_year}) - ${self.predicted_price_usd}"

    class Meta:
        ordering = ['-created_at']