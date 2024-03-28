import os, psycopg
from flask import g
from psycopg.rows import dict_row

class DatabaseConnection:
    database_url = os.getenv("DATABASE_URL")

    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        if test_mode:
            self.database_url += "_test"

    def connect(self):
        try:
            self.connection = psycopg.connect(self.database_url, row_factory=dict_row)
        except psycopg.OperationalError:
            raise Exception(f"Couldn't connect to the database {self.database_url}! Ensure the DATABASE_URL is correctly set.")


def get_flask_database_connection(app):
    if not hasattr(g, "flask_database_connection"):
        g.flask_database_connection = DatabaseConnection(test_mode=os.getenv("APP_ENV") == "test")
        g.flask_database_connection.connect()
    return g.flask_database_connection
