from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Booking, Movie, Seat

User = get_user_model()


def make_movie(title="Test Movie"):
    return Movie.objects.create(
        title=title, description="Desc", release_date=date(2025, 1, 1), duration=100
    )


class ModelTests(TestCase):
    def test_str_methods(self):
        user = User.objects.create_user("ann", password="pw12345!")
        movie, seat = make_movie(), Seat.objects.create(seat_number="A1")
        booking = Booking.objects.create(movie=movie, seat=seat, user=user)
        self.assertEqual(str(movie), "Test Movie")
        self.assertEqual(str(seat), "A1")
        self.assertIn("A1", str(booking))

    def test_seat_defaults_to_available(self):
        self.assertFalse(Seat.objects.create(seat_number="B1").booking_status)


class MovieApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("ann", password="pw12345!")
        self.movie = make_movie()

    def test_anyone_can_list_movies(self):
        res = self.client.get("/api/movies/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()[0]["title"], "Test Movie")

    def test_anonymous_cannot_create_movie(self):
        res = self.client.post("/api/movies/", {})
        self.assertIn(res.status_code, (401, 403))

    def test_authenticated_can_create_movie(self):
        self.client.force_authenticate(self.user)
        res = self.client.post("/api/movies/", {
            "title": "New", "description": "d", "release_date": "2025-05-05", "duration": 90,
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_invalid_movie_rejected(self):
        self.client.force_authenticate(self.user)
        res = self.client.post("/api/movies/", {"title": "No duration"})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class SeatAndBookingApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("ann", password="pw12345!")
        self.other = User.objects.create_user("bob", password="pw12345!")
        self.movie = make_movie()
        self.seat = Seat.objects.create(seat_number="A1")

    def test_seats_are_read_only(self):
        self.client.force_authenticate(self.user)
        res = self.client.post("/api/seats/", {"seat_number": "Z9"})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_book_requires_login(self):
        res = self.client.post(f"/api/seats/{self.seat.id}/book/", {"movie": self.movie.id})
        self.assertIn(res.status_code, (401, 403))

    def test_book_seat_success_marks_seat_booked(self):
        self.client.force_authenticate(self.user)
        res = self.client.post(f"/api/seats/{self.seat.id}/book/", {"movie": self.movie.id})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.booking_status)
        self.assertEqual(Booking.objects.get().user, self.user)

    def test_book_requires_movie(self):
        self.client.force_authenticate(self.user)
        res = self.client.post(f"/api/seats/{self.seat.id}/book/", {})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_unknown_seat_returns_400_or_404(self):
        self.client.force_authenticate(self.user)
        res = self.client.post("/api/seats/9999/book/", {"movie": self.movie.id})
        self.assertIn(res.status_code, (400, 404))

    def test_double_booking_blocked(self):
        self.client.force_authenticate(self.user)
        self.client.post(f"/api/seats/{self.seat.id}/book/", {"movie": self.movie.id})
        self.client.force_authenticate(self.other)
        res = self.client.post(f"/api/seats/{self.seat.id}/book/", {"movie": self.movie.id})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Booking.objects.count(), 1)

    def test_create_booking_via_bookings_endpoint_marks_seat(self):
        self.client.force_authenticate(self.user)
        res = self.client.post("/api/bookings/", {"movie": self.movie.id, "seat": self.seat.id})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.booking_status)

    def test_bookings_require_login(self):
        self.assertIn(self.client.get("/api/bookings/").status_code, (401, 403))

    def test_history_only_shows_own_bookings(self):
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.other)
        self.client.force_authenticate(self.user)
        res = self.client.get("/api/bookings/history/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), [])

    def test_cancel_booking_frees_seat(self):
        self.client.force_authenticate(self.user)
        res = self.client.post(f"/api/seats/{self.seat.id}/book/", {"movie": self.movie.id})
        res = self.client.delete(f"/api/bookings/{res.json()['id']}/")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.seat.refresh_from_db()
        self.assertFalse(self.seat.booking_status)

    def test_cannot_cancel_someone_elses_booking(self):
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.other)
        self.client.force_authenticate(self.user)
        res = self.client.delete(f"/api/bookings/{booking.id}/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_bookings_cannot_be_edited(self):
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.client.force_authenticate(self.user)
        res = self.client.patch(f"/api/bookings/{booking.id}/", {"seat": self.seat.id})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class WebViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("ann", password="pw12345!")
        self.movie = make_movie()
        self.seat = Seat.objects.create(seat_number="A1")

    def test_movie_list_is_public(self):
        res = self.client.get(reverse("movie_list"))
        self.assertContains(res, "Test Movie")

    def test_movie_list_empty_state(self):
        Movie.objects.all().delete()
        self.assertContains(self.client.get(reverse("movie_list")), "No movies are showing yet")

    def test_book_page_redirects_anonymous_to_login(self):
        res = self.client.get(reverse("book_seat", args=[self.movie.id]))
        self.assertEqual(res.status_code, 302)
        self.assertIn("/accounts/login/", res["Location"])

    def test_book_page_shows_seats(self):
        self.client.login(username="ann", password="pw12345!")
        res = self.client.get(reverse("book_seat", args=[self.movie.id]))
        self.assertContains(res, "A1")

    def test_book_page_404_for_unknown_movie(self):
        self.client.login(username="ann", password="pw12345!")
        self.assertEqual(self.client.get(reverse("book_seat", args=[999])).status_code, 404)

    def test_booking_flow_and_history(self):
        self.client.login(username="ann", password="pw12345!")
        res = self.client.post(reverse("book_seat", args=[self.movie.id]), {"seat": self.seat.id})
        self.assertRedirects(res, reverse("booking_history"))
        self.assertContains(self.client.get(reverse("booking_history")), "Test Movie")

    def test_booking_taken_seat_shows_error(self):
        self.seat.booking_status = True
        self.seat.save()
        self.client.login(username="ann", password="pw12345!")
        res = self.client.post(reverse("book_seat", args=[self.movie.id]), {"seat": self.seat.id})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)

    def test_booking_without_seat_shows_error(self):
        self.client.login(username="ann", password="pw12345!")
        res = self.client.post(reverse("book_seat", args=[self.movie.id]), {})
        self.assertEqual(res.status_code, 200)

    def test_history_empty_state(self):
        self.client.login(username="ann", password="pw12345!")
        self.assertContains(self.client.get(reverse("booking_history")), "haven't booked anything")

    def test_cancel_booking_frees_seat(self):
        self.seat.booking_status = True
        self.seat.save()
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.client.login(username="ann", password="pw12345!")
        self.client.post(reverse("cancel_booking", args=[booking.id]))
        self.seat.refresh_from_db()
        self.assertFalse(self.seat.booking_status)
        self.assertEqual(Booking.objects.count(), 0)

    def test_cancel_requires_post(self):
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.client.login(username="ann", password="pw12345!")
        res = self.client.get(reverse("cancel_booking", args=[booking.id]))
        self.assertEqual(res.status_code, 405)

    def test_register_creates_user_and_logs_in(self):
        res = self.client.post(reverse("register"), {
            "username": "newbie", "password1": "S3cure-pass-77", "password2": "S3cure-pass-77",
        })
        self.assertRedirects(res, reverse("movie_list"))
        self.assertTrue(User.objects.filter(username="newbie").exists())

    def test_register_page_renders(self):
        self.assertEqual(self.client.get(reverse("register")).status_code, 200)