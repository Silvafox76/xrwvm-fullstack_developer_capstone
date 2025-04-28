import random
from .models import CarMake, CarModel

def initiate():
    car_make_data = [
        {"name": "Audi", "description": "Premium German engineering and design"},
        {"name": "BMW", "description": "Ultimate Driving Machine from Germany"},
        {"name": "Porsche", "description": "High-performance German sports cars"},
    ]

    # Create CarMake instances
    car_make_instances = []
    for data in car_make_data:
        car_make = CarMake.objects.create(
            name=data['name'],
            description=data['description']
        )
        car_make_instances.append(car_make)

    # Create CarModel instances
    car_model_data = [
        # Audi Models
        {"name": "A8", "type": "Sedan", "year": 2025, "car_make": car_make_instances[0]},
        {"name": "Q8", "type": "SUV", "year": 2025, "car_make": car_make_instances[0]},
        {"name": "e-tron GT", "type": "Sedan", "year": 2025, "car_make": car_make_instances[0]},
        
        # BMW Models
        {"name": "7 Series", "type": "Sedan", "year": 2025, "car_make": car_make_instances[1]},
        {"name": "X7", "type": "SUV", "year": 2025, "car_make": car_make_instances[1]},
        {"name": "iX", "type": "SUV", "year": 2025, "car_make": car_make_instances[1]},
        
        # Porsche Models
        {"name": "911 Turbo S", "type": "Sedan", "year": 2025, "car_make": car_make_instances[2]},
        {"name": "Cayenne Turbo", "type": "SUV", "year": 2025, "car_make": car_make_instances[2]},
        {"name": "Taycan", "type": "Sedan", "year": 2025, "car_make": car_make_instances[2]},
    ]

    for data in car_model_data:
        CarModel.objects.create(
            name=data['name'],
            car_make=data['car_make'],
            type=data['type'],
            year=data['year'],
            dealer_id=random.randint(10, 50)  # Random dealer_id between 10 and 50
        )
