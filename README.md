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

0. Build and start the server

    Navigate to the project directory and run:
    
    ```bash
    docker-compose up --build
    ```

    The application should now be running at `http://0.0.0.0/`.
    The Discord bot should be running alongside Django.

## Documentation

API documentation is available at `http://0.0.0.0/api/docs` when the server is running.
