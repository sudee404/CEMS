from datetime import datetime, timedelta
from datetime import datetime
import os
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE','core_settings.settings')

import django
# Import settings
django.setup()

import random
from index_app.models import Event,Category,Venue
from user_auth.models import MyUser
from faker import Faker
import random

fakegen = Faker()


def generate_date():
    current_date = datetime.now()
    year_from_now = current_date + timedelta(days=365)
    random_date = current_date + timedelta(days=random.randint(1, 365))
    if random_date > year_from_now:
        random_date = year_from_now
    return random_date

def get_user():
    user = MyUser.objects.all()
    return random.choice(user)


def generate_category():
    cat = Category.objects.all()
    return random.choice(cat)


def create_event(category, host):
    title = fakegen.catch_phrase()
    description = fakegen.text()
    start_date = fakegen.date_time_this_year(before_now=True, after_now=False)
    end_date = fakegen.date_time_between_dates(
        start_date, start_date + timedelta(days=365))
    guests = fakegen.random_int(min=1, max=1000)
    venue = random.choice(Venue.objects.all())
    
    obj = Event.objects.get_or_create(
        category=category,
        title=title,
        description=description,
        start_date=start_date,
        end_date=end_date,
        guests=guests,
        draft=False,
        host=host,
        venue=venue
    )[0]
    return obj

          


def populate(N=5):
    '''
    Create N Entries of events
    '''

    for entry in range(N):
        category = generate_category()
        host = get_user()
        event = create_event(category,host)
        print(f"Created {event.title}")

def get_events():
    try:
        events = int(input("Number of events : "))
    except:
        print("Can't take empty values")
        return get_events()
    else:
        return events


if __name__ == '__main__':
    events = get_events()
    print("Populating the databases...Please Wait")
    populate(events)
    print('Populating Complete')
