from django.urls import include, path
from rest_framework.routers import DefaultRouter
 
from . import web_views
from .views import BookingViewSet, MovieViewSet, SeatViewSet
 
router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"seats", SeatViewSet, basename="seat")
router.register(r"bookings", BookingViewSet, basename="booking")
 
urlpatterns = [
    # REST API: /api/movies/, /api/seats/, /api/bookings/
    path("api/", include(router.urls)),
    # HTML pages
    path("", web_views.movie_list, name="movie_list"),
    path("movies/<int:movie_id>/book/", web_views.book_seat, name="book_seat"),
    path("history/", web_views.booking_history, name="booking_history"),
    path("history/<int:booking_id>/cancel/", web_views.cancel_booking_view, name="cancel_booking"),
    path("register/", web_views.register, name="register"),
]