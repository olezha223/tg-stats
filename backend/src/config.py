import os
from dotenv import load_dotenv
from dataclasses import dataclass

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


@dataclass
class NGINXConfig:
    APP_PREFIX: str = os.getenv("APP_NGINX_PREFIX")


@dataclass
class MongoDBConfig:
    host: str = os.getenv("MONGODB_HOST")
    port: str = os.getenv("MONGODB_PORT")
    database: str = os.getenv("DATABASE")
    users: str = os.getenv("USERS")
    url: str = f"mongodb://{host}:{port}"


app_config = {
    'title': "olezha223",
    'description': "telegram chats analysis app",
    'version': "1.0",
    'root_path': NGINXConfig.APP_PREFIX
}