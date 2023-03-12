# Asynchronous Chat App

This is a Asynchronous chat application built using Django, Django Channels, and WebSockets. The application allows users to send and receive messages in real-time with other connected users.

## Installation

```bash
1.Clone this repository using git "clone https://github.com/implicitdefcncdragneel/1-1AsyncChatApp_JWT.git"
2.Install the dependencies using "pip install -r requirements.txt"
3.Make sure to comment out daphne and gunicorn if python version of local enviroment is greater than "3.10"
4.Set up your database by running "python manage.py migrate"
5.Create a superuser using "python manage.py createsuperuser"
6.Run the development server using "python manage.py runserver"
7.Make sure Redis is up and running on port "6379"
```

## Makefile

This Makefile provides convenience commands for running a Docker Compose based development environment for this Chat App.

### Prerequisites

    1. Docker
    2. Docker Compose

#### Usage

    To build and start the development environment, run:
    1. make build

    To start the development environment without rebuilding, run:
    2. make up

    To stop and remove the development environment, run:
    3. make down

    To show the logs for the development environment, run:
    4. make show_logs

    To run Django database migrations, run:
    5. make migrate

Note: All the above commands should be executed in the same directory as the Makefile.

## Demo
