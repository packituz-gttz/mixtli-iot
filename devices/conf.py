import os

postgres_url = "postgresql+psycopg2://postgers:postgres@localhost/devices"


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', postgres_url)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ELEMENTS_PER_PAGE = 50
