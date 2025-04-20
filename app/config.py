import os
from dotenv import load_dotenv
# loading environment variables locally
if not os.getenv("ENV"):
    load_dotenv()
ENV = os.getenv("ENV", "development")

class Settings:
    def __init__(self):
        if ENV == "test":
            self.MYSQL_USER = os.getenv("TEST_MYSQL_USER", "root")
            self.MYSQL_PASSWORD = os.getenv("TEST_MYSQL_PASSWORD", "password")
            self.MYSQL_DATABASE = os.getenv("TEST_MYSQL_DATABASE", "test_game_catalog")
            self.MYSQL_HOST = os.getenv("TEST_MYSQL_HOST", "test-db")
        else:
            self.MYSQL_USER = os.getenv("MYSQL_USER", "root")
            self.MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
            self.MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "game_catalog")
            self.MYSQL_HOST = os.getenv("MYSQL_HOST", "db")

        self.DATABASE_URL = f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}/{self.MYSQL_DATABASE}"
        self.ENV = ENV

settings = Settings()
