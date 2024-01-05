import requests
from requests.auth import HTTPBasicAuth
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from .keys import NLP_key
    

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if kwargs.get('api_key',0):
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', kwargs.get('api_key',0)))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
        raise
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST from {} ".format(url))
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
        raise
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    dealers = get_request(url, **kwargs)
    dealers = dealers['dealerships']
    if dealers:
        # For each dealer object
        for dealer in dealers:
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

'''
def get_dealers_by_state(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    dealers = get_request(url, **kwargs)
    dealers = dealers['dealerships']
    if dealers:
        # For each dealer object
        for dealer in dealers:
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results
'''

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    reviews = get_request(url, **kwargs)
    reviews = reviews['Reviews']
    if reviews:
        # For each dealer object
        for review in reviews:
            review_obj = DealerReview(dealership=review["dealership"], name=review["name"], sentiment = analyze_review_sentiments(review["review"]),
                                   purchase=review["purchase"], review=review["review"], purchase_date=review["purchase_date"],
                                   car_make=review["car_make"],
                                   car_model=review["car_model"], car_year=review["car_year"])
            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/a8cfc93a-73c8-48d5-9d41-5e68b04121b7"
    authenticator = IAMAuthenticator(NLP_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
    version="2022-04-07",
    authenticator=authenticator
)
    natural_language_understanding.set_service_url(url)
    #print('text: ', text)
    response = natural_language_understanding.analyze(
    text=text,
    language="en",
    features=Features(
        entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
        sentiment=SentimentOptions(document=True)),
    return_analyzed_text=True).get_result()
    print('response from sentiment:')
    print(response)
    label = response['sentiment']['document']['label']
    return label
  
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



