# Homework1
## Setup
```python
python3 -m venv homework1_env --system-site-packages

source homework1_env/bin/activate

python3 -m pip install pytest
```
## Run
```python
From homework1 directory

python src/task1.py #Change Number for corresponding task

pytest #For Tests
```

# Homework2

# Movie Theater Booking

**Render Site:** https://cs4300-4u52.onrender.com/

**Admin Login:** username `admin`, password `1234` (or create your own account on the Create account page).

## Features

- Browse movie listings (public)
- Register, log in and log out
- Book a seat for a movie, with double-booking protection
- View booking history and cancel bookings (cancelling frees the seat)
- REST API for movies, seats and bookings
- Django admin for managing movies, seats and bookings

## Project structure

```
homework2/movie_theater_booking/
├── manage.py
├── requirements.txt
├── build.sh                      # Render build script
├── movie_theater_booking/        # project settings and root urls.py
├── bookings/
│   ├── models.py                 # Movie, Seat, Booking
│   ├── serializers.py            # DRF serializers + booking validation
│   ├── views.py                  # API viewsets and HTML page views
│   ├── urls.py                   # API router and page routes
│   ├── admin.py
│   ├── tests.py                  # unit and integration tests
│   ├── apps.py
│   ├── templates/
│   |    ├── bookings/             # base, movie_list, seat_booking, booking_history
│   |    └── registration/         # login, register
|   └── migrations/
└── features/                     # Behave BDD tests
    ├── booking.feature
    └── steps/booking_steps.py
```

## Local setup

```bash
python3 -m venv myenv --system-site-packages
source myenv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py seed_data          # optional: sample seats and movies
python3 manage.py createsuperuser    # optional: admin account
python3 manage.py runserver 0.0.0.0:3000
```

## API endpoints

| Endpoint | Methods | Notes |
|---|---|---|
| `/api/movies/` | GET, POST, PUT, PATCH, DELETE | Anyone can read; login required to write |
| `/api/seats/` | GET | Seat availability (read-only) |
| `/api/seats/<id>/book/` | POST | Body: `{"movie": <id>}`; login required |
| `/api/bookings/` | GET, POST | Current user's bookings only; login required |
| `/api/bookings/<id>/` | GET, DELETE | Cancelling frees the seat |
| `/api/bookings/history/` | GET | Current user's booking history |

## Running the tests

```bash
python3 manage.py test                                  # unit and integration tests
coverage run manage.py test && coverage report -m       # coverage (target: 80%+)
python3 manage.py behave                                # Behave BDD tests
```

## AI usage

Claude, DevEdu Code, and Pardot were used at varying points throughout. DevEdu Code and Pardot were used a few times to either check stuff or fix something and had no involvement past that. Claude generated the html files, test files, and build files for Behave which were implemented after being checked by me and tested before commit. Claude was also referenced or had partial generation throughout most of the other files in the program. Claude was also used for the original layout of the README.md and helped deploy to render.
