from rest_framework import serializers
from .models import Movie, Seat, Booking

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        field = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        field = '__all__'

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = booking
        field = ['id', 'moive', 'seat', 'user', 'booking_date']