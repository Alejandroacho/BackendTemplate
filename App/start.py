import os
import socket
import time
from argparse import ArgumentParser
from argparse import Namespace
from datetime import datetime
from socket import socket as Socket


"""
This is a workaround python script in order to check if
database port is open, avoiding this way docker-compose
race condition that makes django mysql connection fail.

It can be run passing one of these services : Django-app
Celery-Worker or Celery-Beat. Or you can pass custom services
calling it as:

python3 start.py --waiting-service-name database --ip database
--port 3306 --raising-service-name Django-App
--command 'python3 manage.py runserver 0.0.0.0:8000'
"""

CELERY_WORKER: str = (
    "celery --app=App.celery_worker.worker.app worker "
    + "--concurrency=1 --hostname=worker@%h --loglevel=INFO"
)
CELERY_BEAT: str = (
    "python3 -m celery --app=App.celery_worker.worker.app beat -l debug -f"
    + " /var/log/App-celery-beat.log --pidfile=/tmp/celery-beat.pid"
)
DJANGO: str = "python3 manage.py runserver 0.0.0.0:8000"


class Start:
    def __init__(self) -> None:
        description: str = (
            "Check if port is open, avoid docker-compose race condition"
        )
        parser: ArgumentParser = ArgumentParser(description=description)
        self.arguments = self.get_arguments(parser)
        service: str = str(self.arguments.service)
        self.set_service_data(service)
        self.iterate_port()

    def get_arguments(self, parser: ArgumentParser) -> Namespace:
        parser.add_argument("--service", required=False)
        parser.add_argument("--waiting-service-name", required=False)
        parser.add_argument("--ip", required=False)
        parser.add_argument("--port", required=False)
        parser.add_argument("--raising-service-name", required=False)
        parser.add_argument("--command", required=False)
        return parser.parse_args()

    def set_service_data(self, service: str) -> None:
        if service:
            self.set_service_data(service)
        else:
            self.set_custom_data()
        self.iterate_port()

    def set_service_data(self, service: str) -> None:
        self.raising_service_name = service
        self.waiting_service_name = "database"
        self.ip = "database"
        self.port = 3306
        self.command = self.get_command(service)

    def set_custom_data(self) -> None:
        self.waiting_service_name = str(self.arguments.waiting_service_name)
        self.port = int(self.arguments.port)
        self.ip = str(self.arguments.ip)
        self.raising_service_name = str(self.arguments.raising_service_name)
        self.command = str(self.arguments.command)

    def get_command(self, service: str) -> str:
        if service == "Django-App":
            command = DJANGO
        elif service == "Celery-Worker":
            command = CELERY_WORKER
        elif service == "Celery-Beat":
            command = CELERY_BEAT
        return command

    def iterate_port(self) -> None:
        while True:
            database_socket: Socket = Socket(
                socket.AF_INET, socket.SOCK_STREAM
            )
            service_result: int = database_socket.connect_ex(
                (self.ip, self.port)
            )
            if service_result == 0:
                self.run_service()
                break
            self.port_is_not_ready()

    def run_service(self) -> None:
        now: datetime = datetime.now()
        os.system(
            f'echo "{now}" [info] The service '
            f"{self.waiting_service_name} is now "
            f"running and the port is open. Now "
            f"{self.raising_service_name} will start!"
        )
        os.system(self.command)

    def port_is_not_ready(self) -> None:
        now: datetime = datetime.now()
        os.system(
            f'echo "{now}" [info] The port of '
            f"{self.waiting_service_name} is not "
            "open yet. It will be checked again soon!"
        )
        time.sleep(1)


Start()
