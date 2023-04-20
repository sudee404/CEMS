from faker import Faker
import django
import os

# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_settings.settings')

# Import settings
django.setup()

from index_app.models import Category

fakegen = Faker()


def populate(N):
    '''
    Create N Entries of Categories
    '''

    for i in range(N):
        # Create fake category data
        name = fakegen.word()
        image = 'images/default.png'
        description = fakegen.text()

        # Create new category object
        category_obj = Category.objects.get_or_create(
            name=name,
            image=image,
            description=description,
        )


def get_value():
    try:
        num_categories = int(input("Number of Categories to create: "))
    except:
        print("Can't take empty values")
        return get_value()
    else:
        return num_categories


if __name__ == '__main__':
    num_categories = get_value()
    print("Adding categories...Please Wait")
    populate(num_categories)
    print('Populating Complete')
