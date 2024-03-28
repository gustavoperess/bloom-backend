import os, psycopg
from flask import g
from psycopg.rows import dict_row

#DATABASE_URL='postgresql://bloom_www8_user:XISAZAAILCfLcM8iBrBFBAUwXiPQsBXd@dpg-co2kftol6cac73bpd8pg-a.frankfurt-postgres.render.com/bloom_www8'

class DatabaseConnection:
    database_url = os.getenv("DATABASE_URL")
    print(database_url)

    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        if test_mode:
            self.database_url += "_test"

    def connect(self):
        try:
            self.connection = psycopg.connect(self.database_url, row_factory=dict_row)
        except psycopg.OperationalError:
            raise Exception(f"Couldn't connect to the database {self.database_url}! Ensure the DATABASE_URL is correctly set.")
    
    # This method seeds the database with the given SQL file.
    # We use it to set up our database ready for our tests or application.
    def seed(self, sql_filename):
        self._check_connection()
        if not os.path.exists(sql_filename):
            raise Exception(f"File {sql_filename} does not exist")
        with self.connection.cursor() as cursor:
            cursor.execute(open(sql_filename, "r").read())
            self.connection.commit()

    # This method executes an SQL query on the database.
    # It allows you to set some parameters too. You'll learn about this later.
    def execute(self, query, params=[]):
        self._check_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            if cursor.description is not None:
                result = cursor.fetchall()
            else:
                result = None
            self.connection.commit()
            return result

    CONNECTION_MESSAGE = (
        ""
        "DatabaseConnection.exec_params: Cannot run a SQL query as "
        "the connection to the database was never opened. Did you "
        "make sure to call first the method DatabaseConnection.connect` "
        "in your app.py file (or in your tests)?"
    )

    # This private method checks that we're connected to the database.
    def _check_connection(self):
        if self.connection is None:
            raise Exception(self.CONNECTION_MESSAGE)

    # This private method returns the name of the database we should use.
    def _database_name(self):
        if self.test_mode:
            return self.TEST_DATABASE_NAME
        else:
            return self.DEV_DATABASE_NAME

def get_flask_database_connection(app):
    if not hasattr(g, "flask_database_connection"):
        g.flask_database_connection = DatabaseConnection(test_mode=os.getenv("APP_ENV") == "test")
        g.flask_database_connection.connect()
    return g.flask_database_connection
