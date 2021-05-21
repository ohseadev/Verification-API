from fastapi import FastAPI, HTTPException
from models import Verification
from database import addVerification, emailTaken

app = FastAPI()


@app.post('/verification')
async def post_verification(verification: Verification):
    # checks if email is already taken
    if await emailTaken(verification.dict()['email']):
        # raises error if taken
        raise HTTPException(status_code=409, detail='Email already used.')

    # adds to verification database
    await addVerification(verification.dict())
    # return verified object
    return verification.dict()
