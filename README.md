# Itrac Django Api

## Running

Run container:

    docker-compose up --build

Make migrations:

    sudo docker-compose -f docker-compose.yml run --rm web python manage.py makemigrations

Migrate:

    sudo docker-compose -f docker-compose.yml run --rm web python manage.py migrate


## Removing

Remove Postgres container:

    sudo docker rm -f -v itracdjangoapi_postgres_1
