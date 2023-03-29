DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

INSTALLED_APPS = (
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django.contrib.auth",
    "mysql_binlog",
    "tests.management",
    "tests",
)

MIDDLEWARE = []

USE_TZ = True

TIME_ZONE = "UTC"

SECRET_KEY = "foobar"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    }
]


STATIC_URL = "/static/"


# XMLTestRunner output
TEST_OUTPUT_DIR = ".xmlcoverage"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"