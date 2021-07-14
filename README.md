# DRF Blog API

This is a blogging service API developed using Python/Django/Django Rest Framework(DRF)

## Overview

This service provides basic blogging functionality such as posts, comments, likes, and followers.
But all of these functions are only available after authentication, so this API implements registration with email confirmation as well as login/logout.
Also, each user has his own profile, which he can edit, for example, add contacts(links to social networks), change avatar, change status, etc.

## Other

In this project, I am using the Google Drive API to save user avatar images. I did this in order to be able to run a
project on a hosting with an ephemeral file system. Thus, you can also run this code on a hosting with an ephemeral filesystem without
worrying about files integrity.

## How to use

1. Clone this repository
2. Create a folder named "media" in the root folder of the project
3. Create a .env file with the following content

```env
# Common Django settings
SECRET_KEY= # You can enter any random string here (this is used to provide cryptographic signing)
DEBUG=1 # 1-True, 0-False
ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

# CORS configuration
# front-end server address(address from which requests will be sent to the api server)
CORS_ALLOWED_ORIGINS=localhost:3000 [::1]
CORS_ORIGIN_WHITELIST=localhost:3000 [::1]

EMAIL_CONFIRMATION_URL= # link that will be sent to the user's email after registration to activate the profile

# Send mail server configuration
EMAIL_HOST= # mail server address(e.g smtp.gmail.com)
EMAIL_HOST_USER= # mail server account(e.g example@gmail.com)
EMAIL_HOST_PASSWORD= # mail server password
EMAIL_USE_TLS=1 # whether to use TLS encryption connection(1-True, 0-False)
EMAIL_PORT= # mail server port

# Database configuration
# If you will be using docker to start the server use this configuration
DB_ENGINE=django.db.backends.postgresql # engine
DB_DATABASE=django_drf_dev_db # database name used in the database
DB_USER=django_drf_dev # database user name
DB_PASSWORD=django_drf_dev # database password
DB_HOST=db # database address
DB_PORT=5432 # database access port
```

4. Then you need to set up Google Drive
5. Install python, pip and pipenv if you haven't already
6. Create a virtual environment using the following command

```bash
> pipenv shell
```

7. Install all dependencies

```bash
> pipenv install
```

8. Enter the following command to run the migrations

```bash
> pipenv run python manage.py migrate
```

9. Create a superuser if you need one

```bash
> pipenv run python manage.py createsuperuser
```

Then start the server

```bash
> pipenv run python manage.py runserver
```

After starting the development server, the provided interface is located at http://localhost:8000/api/v1, the admin panel address is http://localhost:8000/admin

### Setting up Google Drive

1. Create new project on [Google Cloud Platform](https://cloud.google.com/)
2. Enable [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com) for this project
3. Create credentials of type "service account"
4. Create a new private key with JSON key type and download it
5. Rename the key file to "google_drive_api.json" and move it to the config/ folder

## Docker

If you want to start the server in docker follow these steps

1. Complete steps 1-4 from "How to Use"
2. Install docker and docker-compose if you haven't already
3. Build a new image and spin up two containers(django server and postgres)

```bash
> docker-compose up -d --build
```

4. Run the migrations using the following command

```bash
> docker-compose exec web python manage.py migrate
```

5. Create a superuser if you need one

```bash
> docker-compose exec web python manage.py createsuperuser
```

The provided interface is located at http://localhost:8000/api/v1, the admin panel address is http://localhost:8000/admin

## Tests

To run tests, enter the following command

```bash
> pipenv run python manage.py test
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
