# django-es

## Overview
This project implements a composite application utilizing Docker and docker-compose, which includes a Django REST Framework endpoint and an Elasticsearch service.

1. **Authentication Mechanism**: Custom authentication method that mimics JWT using base64 encoding of the username.
2. **Search Endpoint**: An endpoint that queries Elasticsearch using a structured format and returns data in a JSON response.
3. **Register Endpoint**: Enpoint that registers users (basic)
4. **Swagger**: Please for endpoint documentation go to localhost:8000/swagger after running the app



## Technologies Used
- **Django REST Framework**: For building the API.
- **Elasticsearch**: For storing and querying data.
- **Celery**: For background task processing.
- **Redis**: For message brokering with Celery.
- **PostgreSQL**: For database storage.
- **Docker & Docker Compose**: For containerization and orchestration.
- **Poetry**: For dependency management and packaging.

## Features

### 1. Authentication

I wrote a custom authentication you can check from AuthMixin class in the project
Authorization: Octoxlabs <token>

### 2. Search Endpoint
The application provides a search endpoint that processes a query and translates it into an Elasticsearch-compatible format. For example, a query like:

POST /search
{
    "query": "Hostname = octoxlabs*"
}
is translated into an Elasticsearch query and returns the corresponding data stored in Elasticsearch.

### 3. Management Commands
different custom managements commands are added in order to deploy the app

### 4. Celery & Redis
I imitated live data with celery where celery populates the elastic search for data.

### 5. PostgreSQL
The application uses PostgreSQL as the database for Django.

## How to Run the Project
To run the project, you need Docker and Docker Compose installed.
docker-compose up --build
Once the application is running, you can access it on http://localhost:8000.

## Endpoints
Please check the detailed documentation on swagger http://localhost:8000/swagger

POST /api/auth/token/: Login endpoint for generating the authentication token.

POST /api/auth/register/: Register endpoint for creating a new user.

POST /api/search: Search endpoint to query Elasticsearch.

GET /search: Search endpoint to query Elasticsearch.

## Debugging
The application is set up to run in development mode with the debugger exposed on port 5678. This allows you to debug the application directly using VSCode or any other debugger that supports remote debugging.

## Testing
Unit tests have been implemented using Django's testing framework. You can run the tests using the following command:
docker-compose exec web python manage.py test
I added tests to entrypoint of my app in order to show tests to you

## Code Quality
Code quality tools and linting are set up for the project to ensure best practices.

Docker Compose Services
web: Django application running on port 8000.

postgres: PostgreSQL database for Django.

redis: Redis service for Celery.

elasticsearch: Elasticsearch service for data storage and querying.

celery: Celery worker for background tasks.

celerybeat: Celery Beat for managing periodic tasks.


