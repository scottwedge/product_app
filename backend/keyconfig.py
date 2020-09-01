import os


class Database:
    NAME = os.getenv('POSTGRES_DB')
    USER = os.getenv('POSTGRES_USER')
    PASSWORD = os.getenv('POSTGRES_PASSWORD')
    HOST = os.getenv('DATABASE_HOST')
    PORT = os.getenv('DATABASE_PORT')


class Secrets:
    SECRET_KEY = "SuperSecretSecretKey"

# class Secrets:
#     SECRET_KEY = '=fuk7)a+=bafxx#ms%4@5tmdov8z^%hw^+)r_6g2tusbsu!3w8'