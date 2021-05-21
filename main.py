from fastapi import FastAPI, HTTPException
from models import User, Verification
from database import addVerification, emailTaken, authCodeTaken, verify

app = FastAPI()


@app.post('/verification')
async def post_verification(user: User):
    # checks if email is already taken
    if await emailTaken(user.dict()['email']):
        # raises error if taken
        raise HTTPException(status_code=400, detail='Email already used.')

    # adds to verification database
    await addVerification(user.dict())
    # return a success
    return {'message': 'success'}


@app.post('/verify')
async def post_verify(user: Verification):
    # check if auth code exists
    if not await authCodeTaken(user.dict()['auth_code']):
        # raises error if it doesn't exist
        raise HTTPException(status_code=400, detail='Not a valid code.')

    # verifies user in the database
    await verify(user.dict()['id'], user.dict()['auth_code'])
    # return a success
    return {'message': 'success'}
