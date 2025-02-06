# ALX Travel App

## Project Overview
The ALX Travel App is a travel listing application built with Django. It allows users to browse, book, and review travel listings, as well as handle payments using the Chapa API. The app includes models for Listings, Bookings, Reviews, and Payments, and has APIs to interact with these models. This app is designed to manage travel-related data efficiently, allowing users to explore various destinations, book trips, leave reviews, and make secure payments.

## Features
- **Listings**: View and browse travel destinations with detailed descriptions, prices, and locations.
- **Bookings**: Make a reservation for a listing by specifying a start and end date.
- **Reviews**: Leave reviews for listings with a rating and comment.
- **Payments**: Integrate the Chapa API for processing secure payments.
- **Admin Interface**: Manage listings, bookings, and payments via the Django admin panel.

## Models

### Listing
- **name**: Title of the listing.
- **description**: Description of the listing.
- **price_per_night**: Price per night for the listing.
- **location**: Location of the listing.
- **created_at**: Timestamp of when the listing was created.

### Booking
- **listing**: Foreign key to the Listing model.
- **user**: Foreign key to the User model.
- **start_date**: Start date of the booking.
- **end_date**: End date of the booking.
- **total_price**: Total price for the booking.
- **created_at**: Timestamp of when the booking was created.

### Review
- **listing**: Foreign key to the Listing model.
- **user**: Foreign key to the User model.
- **rating**: Rating out of 5.
- **comment**: Review comment.
- **created_at**: Timestamp of when the review was created.

### Payment
- **payment_status**: Status of the payment (pending, completed, failed).
- **amount**: The total transaction amount.
- **transaction_id**: Unique identifier for the transaction.
- **user**: Foreign key to the User model.
- **created_at**: Timestamp when the payment was created.

## Setup and Installation

### Prerequisites
- Python 3.x
- Django 3.x or higher
- A working Chapa API key for payment integration

### Steps to Run the Project
1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/alx_travel_app.git
    ```

2. **Navigate to the project directory:**
    ```bash
    cd alx_travel_app
    ```

3. **Install the project dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up Chapa API credentials:**

    In `settings.py`, add your Chapa secret key:
    ```python
    CHAPA_SECRET_KEY = 'your_chapa_secret_key'
    ```

5. **Run migrations:**

    Apply migrations to set up the database schema:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Seed the database with sample data:**

    Run the management command to populate the database:
    ```bash
    python manage.py seed
    ```

7. **Start the development server:**
    ```bash
    python manage.py runserver
    ```

## Usage

### API Endpoints

- **Listings**: View available travel destinations.
    - `GET /listings/`
  
- **Bookings**: Book a listing for a specific date range.
    - `POST /bookings/`
  
- **Reviews**: Leave and view reviews for listings.
    - `POST /reviews/`
  
- **Payments**: Initiate and verify payments through the Chapa API.
    - `POST /payment/initiate/`
    - `GET /payment/verify/`

### Testing the Seeder
To populate the database with sample data for testing purposes, run:
```bash
python manage.py seed
