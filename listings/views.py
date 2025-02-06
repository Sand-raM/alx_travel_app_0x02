from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Booking, Listing, Payment
from .serializers import BookingSerializer, ListingSerializer
from .tasks import send_booking_confirmation_email, send_payment_confirmation
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.http import JsonResponse
from django.conf import settings

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

# Chapa API configuration
CHAPA_API_URL = "https://api.chapa.co/v1/transaction/initialize"
CHAPA_SECRET_KEY = settings.CHAPA_SECRET_KEY  # Get API key from settings

# Payment verification endpoint
@csrf_exempt
def verify_payment(request):
    if request.method == "GET":
        transaction_id = request.GET.get("transaction_id")
        verify_url = f"https://api.chapa.co/v1/transaction/verify/{transaction_id}"
        
        headers = {
            "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.get(verify_url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            status = response_data["data"]["status"]  # Chapa returns payment status
            
            # Update Payment Model
            payment = Payment.objects.filter(transaction_id=transaction_id).first()
            if payment:
                payment.status = "Completed" if status == "success" else "Failed"
                payment.save()

                # Trigger the Celery task if payment is successful
                if payment.status == "Completed":
                    send_payment_confirmation.delay(payment.user.email)

            return JsonResponse({"status": status}, status=200)
        else:
            return JsonResponse({"error": "Failed to verify payment"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

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
def initiate_payment(request):
    booking_id = request.data.get("booking_id")
    amount = request.data.get("amount")

    booking = get_object_or_404(Booking, id=booking_id)
    chapa_url = "https://api.chapa.co/v1/transaction/initialize"
    headers = {"Authorization": f"Bearer {os.getenv('CHAPA_SECRET_KEY')}"}
    payload = {
        "amount": amount,
        "currency": "ETB",
        "email": booking.user_email,
        "tx_ref": f"booking_{booking_id}",
        "callback_url": "http://127.0.0.1:8000/verify_payment/"
    }

    response = requests.post(chapa_url, json=payload, headers=headers)
    data = response.json()

    if response.status_code == 200:
        payment = Payment.objects.create(booking=booking, transaction_id=data["data"]["tx_ref"], status="Pending", amount=amount)
        return Response({"message": "Payment initiated", "checkout_url": data["data"]["checkout_url"]})
    return Response({"error": "Failed to initiate payment"}, status=400)

@api_view(['GET'])
def verify_payment(request):
    tx_ref = request.GET.get("tx_ref")
    chapa_url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
    headers = {"Authorization": f"Bearer {os.getenv('CHAPA_SECRET_KEY')}"}
    
    response = requests.get(chapa_url, headers=headers)
    data = response.json()

    if response.status_code == 200 and data["status"] == "success":
        payment = Payment.objects.get(transaction_id=tx_ref)
        payment.status = "Completed"
        payment.save()
        return Response({"message": "Payment successful"})
    
    return Response({"error": "Payment failed"}, status=400)