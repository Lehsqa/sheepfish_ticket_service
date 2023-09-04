# Getting started with Ticket Service API

## Running

1) ### `docker-compose up -d --build`
2) ### `docker-compose run web python ticket_service/manage.py migrate`
3) ### `docker-compose run web python ticket_service/manage.py createsuperuser`
4) ### `docker-compose run web python ticket_service/manage.py loaddata ticket_service/api/fixtures/printers.json`
5) ### `docker-compose up`

## Available Paths

### `http://localhost:8000/admin` - admin panel for searching DB`s

### `http://localhost:8000/api/create` - POST method for creating check

### `http://localhost:8000/api/api_key={printer.api_key}` - GET method for downloading checks from browser