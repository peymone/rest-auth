from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
import requests
import uvicorn

from models import *

# Application setting - remove from here
app = FastAPI()
REGISTRATION_SERVICE_URL = 'http://localhost:8002/reg'
AUTHENTIFICATION_SERVICE_URL = 'http://localhost:8002/auth'


@app.post('/reg', status_code=status.HTTP_201_CREATED)
def register(user: UserReg):
    """Register user by invoking specific service via HTTP (RestAPI)"""

    response = requests.post(REGISTRATION_SERVICE_URL, json=user.model_dump(), timeout=10)
    response = response.json()

    if response['result'] == 1:
        return RedirectResponse('/auth')
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="transaction failed when create the User")


@app.post('/auth')
def authentification(user: UserAuth):
    """Authentificate user by invoking specific service via HTTP(RestAPI)"""

    service_response = requests.post(AUTHENTIFICATION_SERVICE_URL, json=user.model_dump(), timeout=10)
    service_response = service_response.json()

    if service_response['result'] == 1:
        return {"operation result": "authentificated"}
    elif service_response['result'] == 0:
        return {"operation result": "incorrect password"}
    else:
        return {"operation result": "user email is invalid or not exist"}


if __name__ == '__main__':
    # For testing only
    uvicorn.run(app, host='localhost', port=8001)
