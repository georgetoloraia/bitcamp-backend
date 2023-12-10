# Bitcamp Backend
Django back of BitCamp platform.

## Local Development

Follow these steps to set up your local development environment.

### Prerequisites

- Python 3.11 or higher
- Pip (Python package manager)
- Django 4.2 or higher
- Django Rest Framework 3.14 or higher
- A Discord bot token (Set an environment variable *DISCORD_BOT_TOKEN*)

### Setup

1. Clone the repository

    ```bash
    git clone https://github.com/bitcamp-ge/bitcamp-backend
    ```

0. Build the Docker image

    Navigate to the project directory and run:
    
    ```bash
    docker-compose build
    ```

0. Start the server

    ```bash
    docker-compose up
    ```

    The application should now be running at `http://localhost:8000`.
    The Discord bot should be running alongside Django.

## Documentation

API documentation is available at `http://localhost:8000/api/docs` when the server is running.
