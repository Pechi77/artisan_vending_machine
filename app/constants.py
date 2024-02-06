
import os
from dotenv import load_dotenv
load_dotenv()

USERNAME = os.getenv("USERNAME").lower()
PASSWORD = os.getenv("PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
DATABASE = os.getenv("DATABASE")
print("Username:", os.getenv("USERNAME"))
print("Password:", os.getenv("PASSWORD"))
print("Host:", os.getenv("MYSQL_HOST"))
print("Database:", os.getenv("DATABASE"))


MYSQL_DATABASE_URL = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{MYSQL_HOST}/{DATABASE}"
