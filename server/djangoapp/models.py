# Uncomment the following imports before adding the Model code

from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

# Car Make model
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    country = models.CharField(max_length=50, default="Unknown")  # Added a little personalization: country of make
    established_year = models.IntegerField(
        default=1900,
        validators=[
            MinValueValidator(1886),  # First car invented 1886
            MaxValueValidator(2023)
        ]
    )

    def __str__(self):
        return f"{self.name} ({self.country})"


# Car Model model
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  # Many-To-One relationship
    name = models.CharField(max_length=100)

    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('TRUCK', 'Truck'),
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible')
    ]
    type = models.CharField(max_length=20, choices=CAR_TYPES, default='SEDAN')

    year = models.IntegerField(
        default=now().year,
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(2023)
        ]
    )

    dealer_id = models.IntegerField()
    color = models.CharField(max_length=30, default="Unpainted")  # Optional touch: color of the car
    price = models.DecimalField(max_digits=10, decimal_places=2, default=30000.00)  # Optional: price in dollars

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
