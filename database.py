import random

import pymongo

from settings import DBuser, DBpass, DBurl

client = pymongo.MongoClient(f"mongodb+srv://{DBuser}:{DBpass}@{DBurl}")
db = client['ohsea']
registered = db['registered_users']
verification = db['pending_verifications']


async def addVerification(user: dict):
    # generate random auth codes
    auth_code = None
    while True:
        auth_code = random.randint(100000, 999999)

        # break out if auth code isn't taken
        if not await authCodeTaken(auth_code):
            break

    # set auth code and insert into database
    user['auth_code'] = auth_code
    verification.insert_one(user)


async def emailTaken(email: str):
    # search database for that email
    search = verification.find_one({"email": email})
    # return bool if it was found or not
    return search is not None


async def authCodeTaken(auth_code: int):
    # search database for that email
    search = verification.find_one({"auth_code": auth_code})
    # return bool if it was found or not
    return search is not None
