from faker import Faker
import random
import django
import os
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_settings.settings')

# Import settings
django.setup()

from user_auth.models import MyUser
from index_app.models import Event, Guest

fakegen = Faker()


def get_user():
    return random.choice(MyUser.objects.all())


def get_event():
    return random.choice(Event.objects.all())


def populate(N):
    '''
    Create N Entries of guests per event
    '''

    for i in range(N):
        # Create N guests for random events
        user = get_user(),
        event = get_event(),
        if user is not event.host:
                    guest_obj = Guest.objects.get_or_create(
            user=user,
            event = event,
        )


def get_value():
    try:
        parties = int(input("Number of Guests: "))
    except:
        print("Can't take empty values")
        return get_value()
    else:
        return parties


if __name__ == '__main__':
    venues = int(input("How many guests do you want : "))
    print("Adding users...Please Wait")
    populate(venues)
    print('Populating Complete')
