from Emails.factories.blacklist import BlackListFactory
from Users.fakers.user import UserFaker
from Users.models import User


class BlackListTestFaker(BlackListFactory):
    affairs: str = "PROMOTION"
