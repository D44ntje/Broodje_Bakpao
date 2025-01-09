import psycopg2
from contextlib import contextmanager

class DatabaseHelper:
    def __init__(self, db_config):
        self.db_config = db_config

    @contextmanager
    def connect(self):
        """
        Manager for database connection.
        """
        connection = psycopg2.connect(**self.db_config)
        cursor = connection.cursor()
        try:
            yield cursor
            connection.commit()
        except Exception as e:
            print(f"Database error: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()