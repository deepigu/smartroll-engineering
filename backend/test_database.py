
from database import get_connection

try:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database()")
            result = cursor.fetchone()

            print("Database connection successful!")
            print("Connected database:", result[0])

except Exception as error:
    print("Database connection failed.")
    print("Error type:", type(error).__name__)
