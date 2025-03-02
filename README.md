
# CEMS - Campus Event Management System

CEMS is a web-based event management system designed for use by universities and colleges. It allows event organizers to easily create and manage events, track attendance, and generate reports.


## Features

- Create and manage events
- Track attendance
- Send email notifications to attendees


## Installation and Setup

1. Clone the Repository and navigate into it

```bash
  git clone https://github.com/sudee404/CEMS.git
  cd CEMS/
```
    
2. Create a virtual environment for the python modules and activate it.

```bash
python -m venv env
source env/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create a .env file in the root of the project and add the following environment variables:

```bash
SECRET_KEY=yoursecretkey
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser
```bash
python manage.py createsuperuser
```

7. Start the development server
```bash
python manage.py runserver
```

## Usage

1. Create an event
- Click on the "Create Event" button on the dashboard
- Fill out the form and click "Save"

2. Manage attendees
- Click on the "Manage Attendees" button on the dashboard
- Add or remove attendees as needed


## Technical Details and Stack

- Built with Django
- Uses SQLite database
- Utilizes a custom user application for authentication

***Stack***

**Client:** HTML, CSS, Javascript, Bootstrap

**Server:** Python



## License
CEMS is licensed under the MIT License.
[MIT](https://choosealicense.com/licenses/mit/)

