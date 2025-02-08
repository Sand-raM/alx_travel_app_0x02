import os
import requests
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Booking, Listing, Payment
from .serializers import BookingSerializer, ListingSerializer
from .tasks import send_booking_confirmation_email, send_payment_confirmation
from django.http import JsonResponse
from .services.chapa import initiate_payment, verify_payment  # Importing the Chapa functions

# Booking ViewSet to handle booking-related API requests
class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        subject = "Booking Confirmation"
        message = f"Dear {booking.customer_name}, your booking (ID: {booking.id}) has been confirmed."
        recipient_list = [booking.customer_email]
        send_booking_confirmation_email.delay(subject, message, recipient_list)

# Listings API endpoint
@api_view(['GET'])
def get_listings(request):
    listings = Listing.objects.all()
    serializer = ListingSerializer(listings, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_booking(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        booking = serializer.save()
        return Response({"message": "Booking created!", "booking_id": booking.id})
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def initiate_booking_payment(request):
    """
    Initiates a payment request to Chapa and returns the checkout URL.
    """
    booking_id = request.data.get("booking_id")
    amount = request.data.get("amount")
    
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Initiating payment using the function from chapa.py
    checkout_url = initiate_payment(booking, amount)
    
    if checkout_url:
        payment = Payment.objects.create(booking=booking, transaction_id=f"booking_{booking_id}", status="Pending", amount=amount)
        return Response({"message": "Payment initiated", "checkout_url": checkout_url})
    
    return Response({"error": "Failed to initiate payment"}, status=400)


@api_view(['GET'])
def verify_payment_view(request, transaction_id):
    """
    Verifies a payment transaction with Chapa and updates payment status.
    """
    if not transaction_id:
        return Response({"error": "Transaction reference missing"}, status=400)

    # Verifying payment using the function from chapa.py
    payment_status = verify_payment(transaction_id)

    if payment_status:
        payment = Payment.objects.get(transaction_id=transaction_id)
        payment.status = "Completed"
        payment.save()

        # Triggering the email notification for successful payment
        send_payment_confirmation.delay(payment.booking.user_email)
        return Response({"message": "Payment successful"})

    return Response({"error": "Payment failed"}, status=400)
