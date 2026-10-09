"""Step definitions for booking.feature.

behave-django gives every scenario a clean test database and exposes a
Django test case as `context.test`, whose `.client` acts like a browser.
"""
from datetime import date

from behave import given, then, when
from django.contrib.auth import get_user_model
from django.urls import reverse

from bookings.models import Booking, Movie, Seat

User = get_user_model()
PASSWORD = "pw12345!"


# ---------------------------------------------------------------- givens
@given('a movie called "{title}"')
def step_movie(context, title):
    Movie.objects.create(
        title=title, description="A test movie.",
        release_date=date(2025, 1, 1), duration=100,
    )


@given('a seat "{number}"')
def step_seat(context, number):
    Seat.objects.create(seat_number=number)


@given('a registered user "{username}"')
def step_user(context, username):
    User.objects.create_user(username, password=PASSWORD)


@given("I am not logged in")
def step_anonymous(context):
    context.test.client.logout()


@given('I am logged in as "{username}"')
def step_login(context, username):
    assert context.test.client.login(username=username, password=PASSWORD)


@given('seat "{number}" is already booked by "{username}" for "{title}"')
def step_existing_booking(context, number, username, title):
    seat = Seat.objects.get(seat_number=number)
    seat.booking_status = True
    seat.save()
    Booking.objects.create(
        movie=Movie.objects.get(title=title), seat=seat,
        user=User.objects.get(username=username),
    )


# ----------------------------------------------------------------- whens
@when("I visit the movie list")
def step_visit_list(context):
    context.response = context.test.client.get(reverse("movie_list"))


@when('I open the booking page for "{title}"')
def step_open_booking_page(context, title):
    movie = Movie.objects.get(title=title)
    context.response = context.test.client.get(reverse("book_seat", args=[movie.id]))

@given('I book seat "{number}" for "{title}"')
@when('I book seat "{number}" for "{title}"')
def step_book(context, number, title):
    movie = Movie.objects.get(title=title)
    seat = Seat.objects.get(seat_number=number)
    context.response = context.test.client.post(
        reverse("book_seat", args=[movie.id]), {"seat": seat.id}, follow=True
    )


@when("I open my booking history")
def step_history(context):
    context.response = context.test.client.get(reverse("booking_history"))


@when('I cancel my booking for seat "{number}"')
def step_cancel(context, number):
    booking = Booking.objects.get(seat__seat_number=number)
    context.response = context.test.client.post(
        reverse("cancel_booking", args=[booking.id]), follow=True
    )


# ----------------------------------------------------------------- thens
@then('I should see "{text}"')
def step_see_text(context, text):
    context.test.assertContains(context.response, text)


@then("I should be redirected to the login page")
def step_login_redirect(context):
    context.test.assertEqual(context.response.status_code, 302)
    context.test.assertTrue(context.response["Location"].startswith("/accounts/login/"))


@then('seat "{number}" should be unavailable')
def step_unavailable(context, number):
    context.test.assertTrue(Seat.objects.get(seat_number=number).booking_status)


@then('seat "{number}" should be available')
def step_available(context, number):
    context.test.assertFalse(Seat.objects.get(seat_number=number).booking_status)


@then('"{username}" should have {count:d} booking')
@then('"{username}" should have {count:d} bookings')
def step_booking_count(context, username, count):
    context.test.assertEqual(Booking.objects.filter(user__username=username).count(), count)