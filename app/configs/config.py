import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ENVIRONMENT: str = os.getenv("ENVIRONMENT")
    PORT: int = int(os.getenv("PORT"))
    DB_HOST: str = os.getenv("DB_HOST")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
    LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
    LINKEDIN_CLIENT_SECRET = ("LINKEDIN_CLIENT_SECRET")
    NEWS_RSS_BASE = os.getenv("NEWS_RSS_BASE", "https://news.google.com/rss/search?q=")


settings = Settings()