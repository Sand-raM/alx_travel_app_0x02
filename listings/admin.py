from django.contrib import admin
from .models import Payment

admin.site.register(Payment)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'amount', 'transaction_id', 'status')  # Customize display
    search_fields = ('transaction_id', 'booking_reference')  # Enable search
    list_filter = ('status',)  # Filter by status

# Alternative if @admin.register doesn't work:
# admin.site.register(Payment, PaymentAdmin)
