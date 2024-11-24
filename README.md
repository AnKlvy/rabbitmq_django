![Static Badge](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white) ![Static Badge](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
# Dockerize Django

## Description
-----------
This is a mini tutorial for containerising (Dockerize) Django.

## Steps to Run
1. Clone the repo
2. Build the docker images: `docker compose build`
3. Run the containers: `docker compose up -d`
4. (For 1st time) Create a superuser: `docker-compose exec django python manage.py createsuperuser`
5. Open Browser and goto: `http://localhost:8000`
7. Shut down docker containers: `docker compose down`


## Additional commands
#### Collect static

```bash
docker compose exec django python manage.py collectstatic
```

#### Create Migrations

```bash
docker compose exec djano python manage.py makemigrations
```

#### Migrate DB

```bash
docker compose exec django python manage.py migrate
```
