from django.db import transaction
from rest_framework import serializers
from .models import Movie, Seat, Booking

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['id', 'movie', 'seat', 'user', 'booking_date']
        read_only_fields = [ "user", "booking_date", ]

    def validate_seat(self, seat): 
        """ Prevent users from booking a seat that is already booked. """ 
        
        if seat.booking_status: 
            raise serializers.ValidationError( "This seat is already booked." ) 
        
        return seat

    def create(self, validated_data):
        """Re-check under a row lock, mark the seat booked, then create the booking."""
        with transaction.atomic():
            seat = Seat.objects.select_for_update().get(pk=validated_data["seat"].pk)
            if seat.booking_status:
                raise serializers.ValidationError({"seat": "This seat is already booked."})
            seat.booking_status = True
            seat.save(update_fields=["booking_status"])
            validated_data["seat"] = seat
            return super().create(validated_data)