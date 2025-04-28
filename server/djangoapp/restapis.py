# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

# GET request to backend API
def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
    request_url = backend_url + endpoint
    if params:
        request_url += "?" + params
    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return None

# Analyze review sentiments using sentiment analyzer microservice
def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    print(f"GET Sentiment from {request_url}")
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        sentiment = response.json().get("sentiment")
        return sentiment
    except Exception as e:
        print(f"Sentiment analysis exception occurred: {e}")
        return "neutral"

# POST a review to backend API
def post_review(data_dict):
    request_url = backend_url + "/insert_review"  # 🚨 FIXED endpoint here!
    print(f"POST to {request_url} with data {data_dict}")
    try:
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Post review exception occurred: {e}")
        return None
