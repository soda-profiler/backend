import os

SETTINGS = dict(
    DB_NAME = os.getenv("DATABASE_NAME"),
    DB_USER = os.getenv("DATABASE_USER"),
    DB_PASSWORD = os.getenv("DATABASE_PASSWORD"),
    DB_HOST = os.getenv("DATABASE_HOST"),
    DB_PORT = os.getenv("DATABASE_PORT"),
    JWT_SECRET = 'Zp93aeJYrZtdpAb7kHh32fxoGpV6FRfy',
    JWT_ALGORITHM = 'HS256',
    JWT_EXP_DELTA_SECONDS = 259200,
    TEST = False
)
    