from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import time

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('DB_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# USER = os.getenv('user')
# PASSWORD = os.getenv('password')
# HOST = os.getenv('host')
# PORT = os.getenv('port')
# DBNAME = os.getenv('dbname')


# while True:
#     try:
#         connection = psycopg2.connect(
#             user=USER,
#             password=PASSWORD,
#             host=HOST,
#             port=PORT,
#             dbname=DBNAME,
#             cursor_factory=RealDictCursor,
#         )
#         print("Connection successful!")
        
#         # Create a cursor to execute SQL queries
#         cursor = connection.cursor()
        
#         # Example query
#         # cursor.execute("SELECT NOW();")
#         # result = cursor.fetchone()
#         # print("Current Time:", result)

#         # Close the cursor and connection
#         # cursor.close()
#         # connection.close()
#         # print("Connection closed.")

#     except Exception as e:
#         print(f"Failed to connect: {e}")
#         time.sleep(2)