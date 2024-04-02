import os

CORS_ORIGINS = os.environ.get("CORS_ORIGINS")
TOKEN_EXPIRE_MINUTE = os.environ.get("TOKEN_EXPIRE_MINUTE")

# db
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

# mongodb
MONGO_INITDB_ROOT_USERNAME = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
MONGO_INITDB_ROOT_PASSWORD = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
MONGODB_NAME = os.environ.get("MONGODB_NAME")
CLUSTER_NAME = os.environ.get("CLUSTER_NAME")
