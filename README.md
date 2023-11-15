# Bitcamp Backend
Django back of BitCamp platform.

## Local Development

Follow these steps to set up your local development environment.

### Prerequisites

- Python 3.11 or higher
- Pip (Python package manager)
- Django 4.2 or higher
- Django Rest Framework 3.14 or higher
- A Discord bot token

### Setup

1. Clone the repository

    ```bash
    git clone https://github.com/bitcamp-ge/bitcamp-backend
    ```

0. Install the dependencies

    Navigate to the project directory and run:
    
    ```bash
    pip install -r requirements.txt
    ```

0. Apply the migrations

    ```bash
    python manage.py migrate
    ```

0. Start the server

    ```bash
    python manage.py runserver localhost:8000
    ```

    The application should now be running at `http://localhost:8000`.
    The Discord bot should be running alongside Django.

## Documentation

API documentation is available at `http://localhost:8000/api/docs` when the server is running.
