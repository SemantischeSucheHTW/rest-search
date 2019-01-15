import os

from indexdao.ortsIndexdao import OrtsIndexDao
from indexdao.zeitIndexdao import ZeitIndexDao
from indexdao.mongodbwortindexdao import MongoDBWortIndexDao
from pagedetailsdao.mongodbdao import MongoDBPageDetailsDao

import app

def env(key):
    value = os.environ.get(key)
    if not value:
        raise Exception(f"environment variable {key} not set!")
    return value

debug = env("DEBUG")

app.ortdao = OrtsIndexDao({
    'host': env("MONGODB_HOST"),
    'port': int(env("MONGODB_PORT")),
    'db': env("MONGODB_DB"),
    'ortsindex_collection': env("MONGODB_ORTSINDEX_COLLECTION"),
    "username": env("MONGODB_USERNAME"),
    "password": env("MONGODB_PASSWORD"),
    "authSource": env("MONGODB_DB")
})

app.zeitdao = ZeitIndexDao({
    'host': env("MONGODB_HOST"),
    'port': int(env("MONGODB_PORT")),
    'db': env("MONGODB_DB"),
    'zeitindex_collection': env("MONGODB_ZEITINDEX_COLLECTION"),
    "username": env("MONGODB_USERNAME"),
    "password": env("MONGODB_PASSWORD"),
    "authSource": env("MONGODB_DB")
})

app.pagedetailsdao = MongoDBPageDetailsDao({
    'host': env("MONGODB_HOST"),
    'port': int(env("MONGODB_PORT")),
    'db': env("MONGODB_DB"),
    'pagedetails_collection': env("MONGODB_PAGEDETAILS_COLLECTION"),
    "username": env("MONGODB_USERNAME"),
    "password": env("MONGODB_PASSWORD"),
    "authSource": env("MONGODB_DB")
})

app.wortdao = MongoDBWortIndexDao({
    'host': env("MONGODB_HOST"),
    'port': int(env("MONGODB_PORT")),
    'db': env("MONGODB_DB"),
    'wordindex_collection': env("MONGODB_WORDINDEX_COLLECTION"),
    "username": env("MONGODB_USERNAME"),
    "password": env("MONGODB_PASSWORD"),
    "authSource": env("MONGODB_DB")
})

app.app.run(host=env("FLASK_HOST"), port=int(env("FLASK_PORT")))
