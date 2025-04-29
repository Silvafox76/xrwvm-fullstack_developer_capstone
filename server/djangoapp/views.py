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
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# ----------------------------------------
# AUTH VIEWS
# ----------------------------------------

@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}
    if user is not None:
        login(request, user)
        response_data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(response_data)

@csrf_exempt
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

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


# ----------------------------------------
# REACT API — Used by React Frontend
# ----------------------------------------

@csrf_exempt
def get_dealers(request):
    """
    Returns the full list of dealers for React frontend
    """
    if request.method == "GET":
        try:
            endpoint = "/fetchDealers"
            dealers = get_request(endpoint)

            # Optional: Ensure JSON is a list
            if isinstance(dealers, dict) and "dealers" in dealers:
                dealers = dealers["dealers"]

            return JsonResponse(dealers, safe=False)
        except Exception as e:
            print(f"Error in get_dealers: {e}")
            return JsonResponse([], safe=False)


# ----------------------------------------
# DJANGO BACKEND API — Used Internally
# ----------------------------------------

def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            sentiment = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = sentiment
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


@csrf_exempt
def add_review(request):
    if request.method == "POST":
        review_data = json.loads(request.body)

        review_text = review_data.get("review")
        dealer_id = review_data.get("dealerId")
        purchase = review_data.get("purchase", False)
        purchase_date = review_data.get("purchaseDate", "")
        car_make = review_data.get("carMake", "")
        car_model = review_data.get("carModel", "")
        car_year = review_data.get("carYear", "")

        sentiment = analyze_review_sentiments(review_text)

        payload = {
            "review": review_text,
            "dealership": dealer_id,
            "purchase": purchase,
            "purchase_date": purchase_date,
            "car_make": car_make,
            "car_model": car_model,
            "car_year": car_year,
            "sentiment": sentiment
        }

        post_review(payload)

        return JsonResponse({"status": "Review posted successfully"})
    else:
        return JsonResponse({"status": "POST request required"})


def get_cars(request):
    count = CarMake.objects.count()
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
