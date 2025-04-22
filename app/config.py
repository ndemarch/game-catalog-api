import os
from dotenv import load_dotenv

# centralizing environment variable loading
ENV = os.getenv("ENV", "development")
if ENV == "test":
    load_dotenv(".env.test")
else:
    load_dotenv(".env")

class Settings:
    def __init__(self):
        self.MYSQL_USER = os.getenv("MYSQL_USER", "user")
        self.MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
        self.MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "game_catalog" if ENV != "test" else "test_game_catalog")
        self.MYSQL_HOST = os.getenv("MYSQL_HOST", "db" if ENV != "test" else "test-db")
        self.DATABASE_URL = f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}/{self.MYSQL_DATABASE}"
        self.ENV = ENV

settings = Settings()

