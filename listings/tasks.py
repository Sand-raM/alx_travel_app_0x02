from celery import shared_task
from .models import Booking
from django.contrib.auth.models import User
from django.core.mail import send_mail

@shared_task
def send_booking_confirmation_email(booking_id, user_email):
    subject = "Booking Confirmation"
    message = f"Your booking with ID {booking_id} has been confirmed!"
    send_mail(subject, message, "admin@alxtravel.com", [user_email])
    return f"Booking confirmation email sent to {user_email}"

@shared_task
def send_payment_confirmation(payment_id, user_email):
    subject = "Payment Confirmation"
    message = f"Your payment with ID {payment_id} has been received!"
    send_mail(subject, message, "admin@alxtravel.com", [user_email])
    return f"Payment confirmation email sent to {user_email}"