from django.shortcuts import render
from django.db import transaction

from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

class MovieViewSet(viewsets.ModelViewSet):
"""CRUD for movies. Anyone can read; only logged-in users can write."""

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class SeatViewSet(viewsets.ModelViewSet):
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
        with transaction.atomic():
            seat = instance.seat
            instance.delete()
            seat.booking_status = False
            seat.save(update_fields=["booking_status"])

    @action(detail=False, methods=["get"])
    def history(self, request):
        """GET /api/bookings/history/"""
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)