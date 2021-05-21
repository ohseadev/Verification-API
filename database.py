import pymongo

from settings import DBuser, DBpass, DBurl

client = pymongo.MongoClient(f"mongodb+src://{DBuser}:{DBpass}@{DBurl}")
