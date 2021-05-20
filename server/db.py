import mysql.connector
import os


def db_connection():
    """
    Connects to the MySQL database.
    Return the cursor
    """
    global cursor
    global db 

    db = mysql.connector.connect(
        host="database",
        port=3306,
        user="root",
        password=os.environ["MYSQL_ROOT_PASSWORD"],
        database="api"
    )

    cursor = db.cursor()
    return cursor
