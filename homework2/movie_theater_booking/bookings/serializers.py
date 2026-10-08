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
        model = booking
        fields = ['id', 'moive', 'seat', 'user', 'booking_date']
    
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user

        seat = validated_data["seat"]

        if seat.is_booked:
            raise serializers.ValidationError(
                {"seat": "This seat is already booked."}
            )

        seat.is_booked = True
        seat.save()

        return Booking.objects.create(**validated_data)