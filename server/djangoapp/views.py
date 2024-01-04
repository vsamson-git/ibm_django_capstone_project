from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def get_dealerships(request):
    if request.method == "GET":
        url = "https://jknf8w2p09.execute-api.us-east-2.amazonaws.com/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        dealer_names = [dealer.short_name for dealer in dealerships]
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
        context = {'dealers': dealer_names}
        return render(request, 'djangoapp/index.html', context)

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    username = request.POST['username']
    psw = request.POST['password']
    user = authenticate(username=username, password=psw)
    login(request,user)
    print(user)
    return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html')
    username = request.POST['username']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    psw = request.POST['password']
    try:
        user = User.objects.get(username=username)
    except:
        user = User.objects.create_user(username=username, first_name=firstname, 
        last_name=lastname, password=psw)
    login(request,user)
    return redirect('djangoapp:index')

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    url = "https://jknf8w2p09.execute-api.us-east-2.amazonaws.com/api/review"
    reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
    reviews_only = [str(review.review) + " - " + str(review.sentiment) for review in reviews]
    return HttpResponse(reviews_only)
    #context = {'reviews': reviews_only}
    #return render(request, 'djangoapp/index.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

