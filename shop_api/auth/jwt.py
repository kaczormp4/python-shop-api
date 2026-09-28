from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from shop.infrastructure.security.jwt import decode_access_token
from shop_api.routes.public import get_users_service

security = HTTPBearer()


def get_current_user(
    service: Generator = Depends(get_users_service),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    token = credentials.credentials

    decoded_token = decode_access_token(token)

    if decoded_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = service.get_user_by_id(decoded_token["sub"])

    if user in None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return decoded_token


# curl -X GET \
#   "http://127.0.0.1:8000/private/me" \
#   -H "Authorization: Bearer TWOJ_TOKEN"

# {
#     "sub": "6698ef0b-9dcb-47df-9806-fc4d81db1acf",
#     "user_id": "6698ef0b-9dcb-47df-9806-fc4d81db1acf",
#     "email": "bartek@s.pl",
#     "exp": 1789400000
# }
