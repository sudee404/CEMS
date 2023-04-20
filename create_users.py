from faker import Faker
import django
import os

# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_settings.settings')

# Import settings
django.setup()

from user_auth.models import MyUser

fakegen = Faker()


def populate(N):
    '''
    Create N Entries of Users
    '''

    for i in range(N):
        # Create fake user data
        username = fakegen.user_name()
        email = fakegen.email()
        password = fakegen.password()

        # Create new user object
        user_obj = MyUser.objects.get_or_create(
            first_name=fakegen.name().split()[0],
            last_name=fakegen.name().split()[-1],
            username=username,
            email=email,
            password=password,
        )


def get_value():
    try:
        num_users = int(input("Number of Users to create: "))
    except:
        print("Can't take empty values")
        return get_value()
    else:
        return num_users


if __name__ == '__main__':
    num_users = get_value()
    print("Adding users...Please Wait")
    populate(num_users)
    print('Populating Complete')
