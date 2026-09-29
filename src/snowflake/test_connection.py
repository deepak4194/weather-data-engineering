from connection import get_snowflake_connection


connection = get_snowflake_connection()

cursor = connection.cursor()

try:
    cursor.execute("SELECT CURRENT_USER(), CURRENT_DATABASE(), CURRENT_SCHEMA()")

    result = cursor.fetchone()

    print("Snowflake connection successful!")
    print("User:", result[0])
    print("Database:", result[1])
    print("Schema:", result[2])

finally:
    cursor.close()
    connection.close()