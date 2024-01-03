from django.db import models
from django.utils.timezone import now


# Create your models here.
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name + " - " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)
    car_name = models.CharField(null=False, max_length=50)
    dealer_id = models.IntegerField(null=False)
    SEDAN = "SEDAN"
    SUV = "SUV"
    WAGON = "WAGON"
    type_choices = [
        (SEDAN, 'SEDAN'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON')
    ]
    car_type = models.CharField(null=False, choices=type_choices, default=SEDAN, max_length=20)
    car_year = models.DateField(null=True)

    def __str__(self):
        return str(self.car_type) + " " + str(self.car_name) + " - " + str(self.car_make) + " " + str(self.car_year)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
