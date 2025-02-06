ALX Travel App 0x01
Overview
The ALX Travel App 0x01 is a Django-based web application designed to manage travel listings and bookings. It includes a RESTful API built using Django REST Framework (DRF) to provide CRUD operations for listings and bookings. This app is part of the ALX Professional Development Program.

Features
Listings Management: Create, read, update, and delete travel listings.
Bookings Management: Create, read, update, and delete bookings associated with listings.
Swagger Documentation: Automated API documentation using Swagger for easy access to endpoint details.
CORS Support: Configured to allow cross-origin resource sharing (CORS).
Technologies Used
Python: Backend development language.
Django: Web framework for building the app.
Django REST Framework: Used to build the API.
drf-yasg: Automatically generates Swagger-based API documentation.
django-cors-headers: Manages CORS in the app to allow cross-origin requests.
Installation
Prerequisites
Ensure that you have Python and pip installed on your system.

Step 1: Clone the repository
bash
Copy
Edit
git clone https://github.com/your-username/alx_travel_app_0x01.git
Step 2: Navigate to the project directory
bash
Copy
Edit
cd alx_travel_app_0x01
Step 3: Set up a virtual environment
bash
Copy
Edit
python -m venv venv
Step 4: Activate the virtual environment
On Windows:

bash
Copy
Edit
.\venv\Scripts\activate
On macOS/Linux:

bash
Copy
Edit
source venv/bin/activate
Step 5: Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
Step 6: Run migrations
bash
Copy
Edit
python manage.py migrate
Step 7: Start the development server
bash
Copy
Edit
python manage.py runserver
The app should now be running at http://127.0.0.1:8000.

API Endpoints
The application provides the following endpoints:

GET /api/listings/ - Retrieve all listings.
POST /api/listings/ - Create a new listing.
PUT /api/listings/{id}/ - Update an existing listing.
DELETE /api/listings/{id}/ - Delete a listing.
GET /api/bookings/ - Retrieve all bookings.
POST /api/bookings/ - Create a new booking.
PUT /api/bookings/{id}/ - Update an existing booking.
DELETE /api/bookings/{id}/ - Delete a booking.
Documentation
Swagger-based documentation for the API is available at:

arduino
Copy
Edit
http://127.0.0.1:8000/swagger/
Contributing
If you'd like to contribute to this project, feel free to fork the repository and submit a pull request with your changes. Please ensure that your code follows the project's style and includes tests.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Django and Django REST Framework for powering the backend.
drf-yasg for automatic API documentation generation.
django-cors-headers for managing CORS in the app.