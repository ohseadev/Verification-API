import aioredis
import uvicorn

from fastapi import FastAPI, HTTPException, Depends
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from models import User, Verification
from database import addVerification, emailTaken, authCodeTaken, verify, \
    idTaken

app = FastAPI()


# Setup Rate Limiter
@app.on_event('startup')
async def startup():
    redis = await aioredis.create_redis_pool("redis://localhost")
    await FastAPILimiter.init(redis)


@app.post('/verification',
          dependencies=[Depends(RateLimiter(times=5, seconds=5))])
async def post_verification(user: User):
    # checks if email is already taken
    if await emailTaken(user.dict()['email']):
        # raises error if taken
        raise HTTPException(status_code=400, detail='Email already used.')

    # adds to verification database
    await addVerification(user.dict())
    # return a success
    return {'message': 'success'}


@app.post('/verify',
          dependencies=[Depends(RateLimiter(times=5, seconds=5))])
async def post_verify(user: Verification):
    # check if auth code exists
    if not await authCodeTaken(user.dict()['auth_code']):
        # raises error if it doesn't exist
        raise HTTPException(status_code=400, detail='Not a valid code.')
    # check if user id is already taken
    elif await idTaken(user.dict()['id']):
        # raises error if it doesn't exist
        raise HTTPException(status_code=403, detail='ID is already used.')

    # verifies user in the database
    await verify(user.dict()['id'], user.dict()['auth_code'])
    # return a success
    return {'message': 'success'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
