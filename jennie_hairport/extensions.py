import certifi
from pymongo import MongoClient
from gridfs import GridFSBucket

_client = None
_db = None
_fs_bucket = None


def init_mongo(app):
    global _client, _db, _fs_bucket

    uri = app.config["MONGO_URI"]
    if not uri:
        raise RuntimeError(
            "MONGO_URI is not set. Add your MongoDB Atlas connection string to .env "
            "(see .env.example) before running the app."
        )

    _client = MongoClient(
        uri,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=8000,
        connectTimeoutMS=8000,
    )
    _db = _client[app.config["MONGO_DB_NAME"]]
    _fs_bucket = GridFSBucket(_db)

    _db.products.create_index("slug", unique=True)
    _db.orders.create_index("reference", unique=True)


def get_db():
    if _db is None:
        raise RuntimeError("MongoDB has not been initialized yet — call init_mongo(app) first.")
    return _db


def get_fs_bucket():
    if _fs_bucket is None:
        raise RuntimeError("MongoDB has not been initialized yet — call init_mongo(app) first.")
    return _fs_bucket


def products_collection():
    return get_db().products


def orders_collection():
    return get_db().orders


def messages_collection():
    return get_db().messages
