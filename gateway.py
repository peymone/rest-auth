from fastapi import FastAPI, HTTPException, status
import requests
import uvicorn

from models import User


app = FastAPI()


@app.post('/reg', status_code=status.HTTP_201_CREATED)
def register(user: User):
    """Register user by invoking registrations service via HTTP (RestAPI)

    Args:
        user (User): user data

    Returns:
        json (User) |  json (dict[str]): return user data or error message
    """

    # user: dict = user.model_dump()
    response = requests.post('http://localhost:8002/reg', json=user.model_dump(), timeout=10)
    response = response.json()

    if response['result'] == 1:
        # Make redirect to authentification page. Update Docks
        return user
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="transaction failed when create the User")


if __name__ == '__main__':
    # For testing only
    uvicorn.run(app, host='localhost', port=8001)
