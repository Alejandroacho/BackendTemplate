from Project.settings.django.local_settings import *


ENVIRONMENT_NAME: str = "test"

STATICFILES_DIRS: tuple = ()
PROJECT_DIR: str = Path(__file__).resolve().parent.parent.parent
STATIC_ROOT: str = os.path.join(PROJECT_DIR, "media")
