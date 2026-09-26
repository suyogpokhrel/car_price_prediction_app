from django import forms

FUEL_CHOICES = [
    ('Diesel', 'Diesel'),
    ('E85 Flex Fuel', 'E85 Flex Fuel'),
    ('Gasoline', 'Gasoline'),
    ('Hybrid', 'Hybrid'),
    ('Plug-In Hybrid', 'Plug-In Hybrid'),
    ('Unknown', 'Unknown'),
]

TRANSMISSION_CHOICES = [
    ('Automatic', 'Automatic'),
    ('Automatic (Dual-Clutch)', 'Automatic (Dual-Clutch)'),
    ('CVT', 'CVT'),
    ('Manual', 'Manual'),
    ('Unknown', 'Unknown'),
]

ACCIDENT_CHOICES = [
    ('None reported', 'None reported'),
    ('At least 1 accident or damage reported', 'At least 1 accident or damage reported'),
    ('Unknown', 'Unknown'),
]

CLEAN_TITLE_CHOICES = [
    ('Yes', 'Yes'),
    ('Unknown', 'Unknown'),
]

BRAND_CHOICES = [(b, b) for b in [
    'Acura', 'Alfa', 'Aston', 'Audi', 'BMW', 'Bentley', 'Bugatti', 'Buick', 'Cadillac',
    'Chevrolet', 'Chrysler', 'Dodge', 'FIAT', 'Ferrari', 'Ford', 'GMC', 'Genesis', 'Honda',
    'Hummer', 'Hyundai', 'INFINITI', 'Jaguar', 'Jeep', 'Karma', 'Kia', 'Lamborghini', 'Land',
    'Lexus', 'Lincoln', 'Lotus', 'Lucid', 'MINI', 'Maserati', 'Maybach', 'Mazda', 'McLaren',
    'Mercedes-Benz', 'Mercury', 'Mitsubishi', 'Nissan', 'Plymouth', 'Polestar', 'Pontiac',
    'Porsche', 'RAM', 'Rivian', 'Rolls-Royce', 'Saab', 'Saturn', 'Scion', 'Subaru', 'Suzuki',
    'Tesla', 'Toyota', 'Volkswagen', 'Volvo', 'smart',
]]


class CarPredictionForm(forms.Form):
    brand = forms.ChoiceField(choices=BRAND_CHOICES)
    model = forms.CharField(max_length=100, help_text="e.g. 3 Series, Civic, Model 3")
    fuel_type = forms.ChoiceField(choices=FUEL_CHOICES)
    transmission = forms.ChoiceField(choices=TRANSMISSION_CHOICES)
    accident = forms.ChoiceField(choices=ACCIDENT_CHOICES)
    clean_title = forms.ChoiceField(choices=CLEAN_TITLE_CHOICES)
    model_year = forms.IntegerField(min_value=1980, max_value=2026)
    mileage = forms.FloatField(min_value=0)
    engine_hp = forms.FloatField(min_value=0)
    engine_liters = forms.FloatField(min_value=0)
    engine_cylinders = forms.FloatField(min_value=0)