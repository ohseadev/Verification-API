from fastapi import FastAPI, HTTPException
from models import User
from database import addVerification, emailTaken

app = FastAPI()


@app.post('/verification')
async def post_verification(user: User):
    # checks if email is already taken
    if await emailTaken(user.dict()['email']):
        # raises error if taken
        raise HTTPException(status_code=409, detail='Email already used.')

    # adds to verification database
    await addVerification(user.dict())
    # return verified object
    return user.dict()
