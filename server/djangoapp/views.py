# djangoapp/views.py
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import (
    analyze_review_sentiments,
    get_request,
    post_review,
    searchcars_request,
)

logger = logging.getLogger(__name__)

# ──────────────── Auth views ────────────────
@csrf_exempt
def login_user(request):
    """Log a user in and return JSON indicating status."""
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})

    return JsonResponse({"userName": username, "status": "Failed"})


def logout_request(request):
    """Front-end expects an empty username on logout."""
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    """Create a new Django user."""
    data = json.loads(request.body)
    username, password = data["userName"], data["password"]

    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {"userName": username, "error": "Already Registered"}, status=409
        )

    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=data["firstName"],
        last_name=data["lastName"],
        email=data["email"],
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


# ──────────────── Inventory stub ────────────────
def get_inventory(request):
    """
    TEMPORARY stub so /djangoapp/inventory/ resolves.
    Swap this out when you have a real inventory model or API.
    """
    sample = [
        {"id": 1, "name": "Widget", "qty": 42},
        {"id": 2, "name": "Gadget", "qty": 13},
    ]
    return JsonResponse({"inventory": sample})


# ──────────────── Car data views ────────────────
def get_cars(request):
    """Return all car makes + models (populate once on first call)."""
    if not CarMake.objects.exists():
        initiate()

    cars = [
        {"CarModel": cm.name, "CarMake": cm.car_make.name}
        for cm in CarModel.objects.select_related("car_make")
    ]
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state: str = "All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id: int):
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    reviews = get_request(f"/fetchReviews/dealer/{dealer_id}")
    for r in reviews:
        r["sentiment"] = analyze_review_sentiments(r["review"]).get("sentiment")
    return JsonResponse({"status": 200, "reviews": reviews})


def get_dealer_details(request, dealer_id: int):
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    dealer = get_request(f"/fetchDealer/{dealer_id}")
    return JsonResponse({"status": 200, "dealer": dealer})


@csrf_exempt
def add_review(request):
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

    data = json.loads(request.body)
    try:
        post_review(data)
        return JsonResponse({"status": 200})
    except Exception as exc:  # noqa: BLE001
        logger.exception("Error posting review: %s", exc)
        return JsonResponse({"status": 500, "message": "Error in posting review"})
