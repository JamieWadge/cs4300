from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Booking, Movie, Seat
from .serializers import BookingSerializer, MovieSerializer, SeatSerializer


def cancel_booking(booking):
    """Delete a booking and free its seat in a single transaction.
    Used by both the API and the HTML cancel button."""
    with transaction.atomic():
        seat = booking.seat
        booking.delete()
        seat.booking_status = False
        seat.save(update_fields=["booking_status"])



# ---------------------------------------------------------------------------
# REST API viewsets
# ---------------------------------------------------------------------------

class MovieViewSet(viewsets.ModelViewSet):
    """CRUD for movies. Anyone can read; only logged-in users can write."""
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    """Seat availability, plus a `book` action. Manage seats via the admin."""
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def book(self, request, pk=None):
        """POST /api/seats/<id>/book/  body: {"movie": <id>}"""
        serializer = BookingSerializer(
            data={"movie": request.data.get("movie"), "seat": pk},
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Create, list, view, and cancel the current user's bookings."""
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        """Cancelling a booking frees the seat."""
        cancel_booking(instance)

    @action(detail=False, methods=["get"])
    def history(self, request):
        """GET /api/bookings/history/"""
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


# ---------------------------------------------------------------------------
# HTML (template) views
# ---------------------------------------------------------------------------

def movie_list(request):
    """Public list of all movies."""
    return render(request, "bookings/movie_list.html", {"movies": Movie.objects.all()})


@login_required
def book_seat(request, movie_id):
    """Show the seat map for a movie (GET) and book the chosen seat (POST)."""
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == "POST":
        serializer = BookingSerializer(
            data={"movie": movie.pk, "seat": request.POST.get("seat")}
        )
        if serializer.is_valid():
            try:
                booking = serializer.save(user=request.user)
            except ValidationError:
                messages.error(request, "Someone just took that seat. Pick another.")
            else:
                messages.success(
                    request, f"Seat {booking.seat} booked for {movie.title}."
                )
                return redirect("booking_history")
        else:
            messages.error(request, "Choose an available seat to continue.")

    seats = Seat.objects.order_by("seat_number")
    return render(request, "bookings/seat_booking.html", {"movie": movie, "seats": seats})


@login_required
def booking_history(request):
    """The logged-in user's bookings, newest first."""
    bookings = (
        Booking.objects.filter(user=request.user)
        .select_related("movie", "seat")
        .order_by("-booking_date")
    )
    return render(request, "bookings/booking_history.html", {"bookings": bookings})


@login_required
@require_POST
def cancel_booking_view(request, booking_id):
    """Cancel one of the user's own bookings and free the seat."""
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    cancel_booking(booking)
    messages.success(request, "Booking cancelled. The seat is available again.")
    return redirect("booking_history")


def register(request):
    """Simple sign-up so people can create an account and log in."""
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save())
        return redirect("movie_list")
    return render(request, "registration/register.html", {"form": form})