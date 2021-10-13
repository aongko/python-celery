# Python - Celery

Using Celery for our task managements.

## Requirementss

We use Python 3.7.

We use Pipenv.

```bash
PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
```

p.s. `PIPENV_VENV_IN_PROJECT` allows us to easily clean up by removing `.venv`

## Run

Run Redis and celery worker.

```bash
docker-compose up -d redis
docker-compose up -d --build worker
```

Try to schedule a task with python shell

```bash
docker-compose run --rm worker python manage.py shell
```
