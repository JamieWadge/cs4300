from django.urls import include, path
from rest_framework.routers import DefaultRouter
 
from . import views
 
router = DefaultRouter()
router.register(r"movies", views.MovieViewSet, basename="movie")
router.register(r"seats", views.SeatViewSet, basename="seat")
router.register(r"bookings", views.BookingViewSet, basename="booking")
 
urlpatterns = [
    # REST API: /api/movies/, /api/seats/, /api/bookings/
    path("api/", include(router.urls)),
    # HTML pages
    path("", views.movie_list, name="movie_list"),
    path("movies/<int:movie_id>/book/", views.book_seat, name="book_seat"),
    path("history/", views.booking_history, name="booking_history"),
    path("history/<int:booking_id>/cancel/", views.cancel_booking_view, name="cancel_booking"),
    path("register/", views.register, name="register"),
]