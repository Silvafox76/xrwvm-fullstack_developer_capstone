# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create a `login_user` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provided credential can be authenticated
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        response_data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(response_data)

# Create a `logout_request` view to handle sign out request
@csrf_exempt
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    if request.method == 'POST':
        user_data = json.loads(request.body)
        username = user_data.get('userName')
        password = user_data.get('password')
        first_name = user_data.get('firstName')
        last_name = user_data.get('lastName')
        email = user_data.get('email')

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Already Registered"})

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": True})
    else:
        return JsonResponse({"status": False})

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    return render(request, 'djangoapp/index.html')

# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    return render(request, 'djangoapp/dealer_details.html', {"dealer_id": dealer_id})

# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    return render(request, 'djangoapp/dealer_details.html', {"dealer_id": dealer_id})

# Create a `add_review` view to submit a review
def add_review(request):
    return render(request, 'djangoapp/add_review.html')

# Create the `get_cars` view to return the list of cars
def get_cars(request):
    count = CarMake.objects.count()
    print(count)
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })
    return JsonResponse({"CarModels": cars})
