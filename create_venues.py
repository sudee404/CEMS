import os
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE','core_settings.settings')

import django
# Import settings
django.setup()

import random
from index_app.models import Location,Venue
from faker import Faker
import random

fakegen = Faker()

cities = ['Kisumu', ' Nairobi', 'Nakuru', 'Mombasa', 'Malindi', 'Kakamega','Busia','Bungoma']

def get_location():
    return random.choice(cities)

def populate(N):
    '''
    Create N Entries of location
    '''

    for city in cities:
        # Now create location object
        loc_obj = Location.objects.get_or_create(city=city,country='Kenya')[0]

        # then create N venues per location
        for i in range(N):
            venue_name = fakegen.company()
            ven_obj = Venue.objects.get_or_create(
                name=venue_name, location=loc_obj)[0]
            print(f"created {venue_name}")
            

def get_value():
    try:
        parties = int(input("Number of Venues in each location: "))
    except:
        print("Can't take empty values")
        return get_value()
    else:
        return parties
        
if __name__ == '__main__':
    venues = int(input("How many Venues do you want : "))
    print("Adding Venues...Please Wait")
    populate(venues)
    print('Populating Complete')
