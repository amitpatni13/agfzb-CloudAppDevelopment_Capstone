from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField(default=0)
    type = models.CharField(max_length=100)
    year = models.DateField(null=True)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Dealer Id: " + str(self.dealer_id) + "," + \
               "Type: " + self.type + "," + \
               "Year: " + str(self.year)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, lat, long, short_name, st, state, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state short
        self.st = st
        # Dealer state name
        self.state = state
        # Dealer zip
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, id, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment):
        # Review Id
        self.id = id
        # Dealer Id
        self.dealership = dealership
        # User name
        self.name = name
        # Purchased True or False
        self.purchase = purchase
        # User Review
        self.review = review
        # Purchase Date
        self.purchase_date = purchase_date
        # Car Maker
        self.car_make = car_make
        # Car Model
        self.car_model = car_model
        # Car Year
        self.car_year = car_year
        # User Sentiment, determined by Watson NLU service. It could be positive, neutral, or negative.
        self.sentiment = sentiment
    def __str__(self):
        return "User name: " + self.name