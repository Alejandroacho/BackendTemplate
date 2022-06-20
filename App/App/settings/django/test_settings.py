from App.settings.django.local_settings import *


ENVIRONMENT_NAME: str = "test"

STATICFILES_DIRS: tuple = ()
STATIC_ROOT: str = os.path.join(BASE_DIR, "Static")
