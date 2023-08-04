from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel
from .restapis import get_dealers_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            # redirect to course list page
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)
def get_dealerships(request):
    if request.method == "GET":
        url = "https://au-syd.functions.appdomain.cloud/api/v1/web/c01ad1b8-f8ce-418a-8abf-5722a3a29abe/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://au-syd.functions.appdomain.cloud/api/v1/web/c01ad1b8-f8ce-418a-8abf-5722a3a29abe/dealership-package/get-review"
        # Get dealers from the URL
        dealers = get_dealer_reviews_from_cf(url, dealer_id)
        print('Dealers', dealers)
        # Concat all dealer's short name
        reviews = ' '.join([dealer.review for dealer in dealers])
        sentiments = ' '.join([dealer.sentiment for dealer in dealers])
        # Return a list of dealer short name
        return HttpResponse(reviews + ' ' + sentiments)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "POST":
        user = request.user
        if user.is_authenticated:
            params = request.params
            car = CarModel.objects.get(id = params.car)
            # review = {
            #     "dealership": dealer_id,
            #     "name": params.name,
            #     "review": params.review,
            #     "purchase": params.purchase,
            #     "purchase_date": params.purchase_date,
            #     "car_make": car.make.name,
            #     "car_model": car.name,
            #     "car_year": car.year.strftime("%Y")
            # }
            review = {
                "dealership": dealer_id,
                "name": "Upkar Lidder",
                "review": "Great service!",
                "purchase": False,
                "purchase_date": "02/16/2021",
                "car_make": "Audi",
                "car_model": "Car",
                "car_year": 2021
            }
            json_payload = {
                "review": review
            }
            # Post dealers review
            url = "https://au-syd.functions.appdomain.cloud/api/v1/web/c01ad1b8-f8ce-418a-8abf-5722a3a29abe/dealership-package/post-review"
            post_review = post_request(url, json_payload, dealerId=dealer_id)
            print('Post review response', post_review)
            return post_review
