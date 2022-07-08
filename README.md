<h1 align="center">
  <b>Backend App Template</b>
</h1>

<h3 align="center">
  <b><i> Django + Docker + MySQL + Celery + RabbitMQ + Flower + Grafana + Prometheus </i></b>
</h3>

* * *
The goal of this project is to enable an easy-to-use and implement template in order to start developing a web app as quickly and conveniently as possible.

The environment we are looking to build is one that uses Django as a python framework for web development with MySQL as a database. Also will be setted up the DjangoRESTFramework to build an API if needed; Celery with RabbitMQ for managing asynchronous tasks, and Flower for monitoring those tasks.

All we be in one Docker container that will be already setted up to just start coding the project.

## Table of Contents
1. [Requirements](#requirements)
2. [Nice to have](#nicetohave)
3. [Before starting](#beforestarting)
4. [Instructions](#instructions)
5. [Observations](#observations)
6. [Interaction](#interaction)
7. [Versions used](#versions)
8. [Useful guides](#usefullguides)

      8.1. [Custum user model](#customusermodel)

<a name="requirements"/>

## Requirements
  - Docker
  - Docker-Compose

<a name="nicetohave"/>

## Nice to have
  - Python3
  - Django

<a name="nicetohave"/>

## Nice to take a look to
- [Docker documentation.](https://docs.celeryproject.org/en/stable/index.html#)
- [Django documentation.](https://www.djangoproject.com/)
- [DjangoREST documentation.](https://www.django-rest-framework.org/)
- [Django Jazzmin documentation.](https://django-jazzmin.readthedocs.io/)
- [Celery documentation.](https://docs.celeryproject.org/)
- [RabbitMQ documentation.](https://www.rabbitmq.com/)
- [Flower documentation.](https://flower.readthedocs.io/en/latest/)
- [Grafana documentation.](https://grafana.com/docs/)
- [Prometheus documentation.](https://prometheus.io/docs/introduction/overview/)
- [OpenApi (swagger) documentation.](https://swagger.io/specification/)
- [ReDoc documentation.](https://redoc.ly/docs)

<a name="beforestarting"/>

## Before starting
Feel free to set your environment variables as you want on ```env.env``` file.

You can change the container name by changing the main folder name.

You can change project name to your actual app name, just take in mind that you will need to change folders name, docker-compose.yml content, Dockerfile content and some django settings in order to the container work correctly.

<a name="instructions"/>

## Instructions

1. Go to root content folder.
2. Bring up the docker container running:
    ```make up```

4. That's all!

    Django admin will be available on: [http://localhost:8000/admin](http://localhost:8000/admin)

    Django app will be available on: [http://localhost:8000/](http://localhost:8000/)

    Flower task monitor will be available on: [http://localhost:5555](http://localhost:5555)

    Grafana monitor will be available on: [http://localhost:3000](http://localhost:3000)

    Prometheus dashboard will be available on: [http://localhost:9090](http://localhost:9090)

    Documentation served by Openapi (Swagger) will be available on: [http://localhost:8000/doc/swagger](http://localhost:8000/doc/swagger/)

    You can also check the documentation server by Redoc on: [http://localhost:8000/doc/redoc](http://localhost:8000/doc/redoc/)

<a name="observations"/>

## Observations

To actual interact with django admin for the first time, you will need to run:

    make migrate
    make createsuperuser

Or acces into the bash (you can do it running ```make bash```) and run:

    python manage.py migrate
    python manage.py createsuperuser


Then you can create and app ([app vs project](https://docs.djangoproject.com/en/3.2/intro/tutorial01/#creating-the-polls-app)) running:

    APP=<app-name> make create-app

Or in the container bash:

    python manage.py create-app <app-name>


To test your django applications you must run:

    make test

Or in the conteiner bash:

    python manage.py test

The first time you run a test, you probably will get an error message saying that your user does not have permissions to interact with the database.
To fix that, you must enter you database mysql container as a root running something like this:

    USER=root PASSWORD=password make database

Or:

    docker-compose exec database mysql -uroot -ppassword

Then you must grant your user the privileges making the following query:

    GRANT ALL PRIVILEGES ON *.* TO 'user'@'%' WITH GRANT OPTION;
    FLUSH PRIVILEGES;

Now you will be able to run your tests.


Grafana Credentials will be user: ```admin``` and password: ```admin```. You will be able to change them once you get logged in.

Notice that Django admin is customizable due the use of [Django-Jazzmin](https://django-jazzmin.readthedocs.io/) that implements [Adminlte](https://adminlte.io/) + [Bootstrap](https://getbootstrap.com/).


<a name="interaction"/>

## Interaction
All the interaction goes through ```makefile```, but you can interact with the containers runing the commands as usual, for example, running manually the comands in the ```makefile```.

You can see docker logs just running ```docker-compose up```, but this will attach the console directly to the container process so if you close it, you will set down the docker container too. To avoid this you can run the container detached to console running:

    make up -d

To see container logs run:

    make logs

To access container bash to interact directly with the container run:

    make bash

To access container shell to interact directly with django run:

    make shell

To run the tests run:

    make test

To access MySQL database run:

    make database USER=user PASSWORD=password

<a name="versions"/>

## Versions used
* * *
Versions that will use the project. Take in mind that python sub versions may change because it will depend on the one used on [python dockerhub image.](https://hub.docker.com/_/python), it will be the same with [RabbitMQ](https://hub.docker.com/_/rabbitmq), and [MySQL](https://hub.docker.com/_/mysql). Even so, the python version in docker container (reviewed on 2022/01/04) is ```3.9.7```.

* Docker compose schema version:  3.8
* Python image:  3
* RabbitMQ image: 3
* MySQL image:  5.6
* Django version:  4.0.0
* DjangoRESTFramework version:  3.12.4
* Celery version:  5.1.2


<a name="usefullguides"/>

<h1 align="center">
  <b>Useful guides</b>
</h1>

These are useful guides to customize our django apps, modifying the default User model.

<a name="customusermodel"/>

### Use custom django user model

You can check the guide in the [medium](https://medium.com/@alex521e2/create-a-custom-user-model-in-django-4-0-a5fd7386b3e0) or [linkedin](https://www.linkedin.com/pulse/create-custom-user-model-django-40-alejandro-acho-mart%25C3%25ADnez/?trackingId=lFj6aKZmHN5pIKDnlOTykQ%3D%3D) post.
