import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    ENVIRONMENT=(str, "development"),
)
environ.Env.read_env()


SECRET_KEY_FROM_ENV = env("SECRET_KEY")
DEBUG_FROM_ENV = env("DEBUG")

LOG_LEVEL = env("LOG_LEVEL")
POSTGRES_DB_NAME = env("POSTGRES_DB_NAME")
POSTGRES_USER_NAME = env("POSTGRES_USER_NAME")
POSTGRES_PASSWORD = env("POSTGRES_PASSWORD")
POSTGRES_HOST = ""
POSTGRES_PORT = -1

ENVIRONMENT = env("ENVIRONMENT")

if ENVIRONMENT == "development":
    POSTGRES_HOST = env("POSTGRES_HOST_DEV")
    POSTGRES_PORT = env("POSTGRES_PORT_DEV")
elif ENVIRONMENT == "production":
    POSTGRES_HOST = env("POSTGRES_HOST_PROD")
    POSTGRES_PORT = env("POSTGRES_PORT_PROD")
