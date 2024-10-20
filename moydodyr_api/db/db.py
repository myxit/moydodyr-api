import logging
import peewee

logger = logging.getLogger(__name__)

# Define the SQLite database
db = peewee.SqliteDatabase('my_database.db')

# Define a model class
class BaseModel(peewee.Model):
    class Meta:
        database = db

def connect():
    db.connect()


def disconnect():
    try:
        db.close()
    except Exception as ex:
        logger.warning(f"Could not close database connection. Error: " + str(ex))
