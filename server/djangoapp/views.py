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
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request

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
    if request.method == 'GET':
        url = "https://jknf8w2p09.execute-api.us-east-2.amazonaws.com/api/review"
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        reviews_only = [str(review.review) + " - " + str(review.sentiment) for review in reviews]
        return HttpResponse(reviews_only)
        #context = {'reviews': reviews_only}
        #return render(request, 'djangoapp/index.html', context)
    else:
        if request.user.is_authenticated:
            url = "https://jknf8w2p09.execute-api.us-east-2.amazonaws.com/api/review"
            try:
                review = dict()
                review["name"] = request.user.username
                review["dealership"] = dealer_id
                review["review"] = request.POST['review']
                review["purchase"] = request.POST.get('purchase', False)
                if review["purchase"]:
                    review["purchase"] = True
                    review["purchase_date"] = datetime.strptime(request.POST['purchase_date'], '%m-%d-%Y').date()
                    review["car_make"] = request.POST['car_make']
                    review["car_model"] = request.POST['car_model']
                    review["car_year"] = request.POST['car_year']
                check_review = post_request(url, review)['result']
                if check_review:
                    return HttpResponse(f"Review '{check_review}' was added successfully")
                return HttpResponse("There was an error while trying to load the review")
            except:
                return HttpResponse("Not Enough Data for a review")
        else:
            return HttpResponse("You MUST authenticate first!")

        