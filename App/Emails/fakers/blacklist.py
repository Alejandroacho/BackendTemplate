from Emails.factories.blacklist import BlackListFactory


class BlackListTestFaker(BlackListFactory):
    email: str = "emailinblacklist@test.com"
