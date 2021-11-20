from typing import Optional
import requests
from fastapi import HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from starlette import status
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from app import schema
from app.database import database as db
from app.config import settings

cfg = settings()

class APIBearerKey(APIKeyHeader):

    def __init__(self, *, auto_error: bool = True):
        super().__init__(name='Authorization', scheme_name=None, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        api_key: str = request.headers.get(self.model.name)
        try:
            prefix, api_key = str(api_key).split(' ', 1)
            if str(prefix).lower() != 'bearer':
                api_key = ''
            if not api_key or len(api_key) == 0:
                if self.auto_error:
                    raise HTTPException(
                        status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                    )
                else:
                    return None
            return api_key
        except (HTTPException, ValueError):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )


api_key_header = APIBearerKey(auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)):
    return api_key


async def get_user_by_token(api_key: str = Depends(get_api_key)):
    if api_key != cfg.super_user_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return schema.User.parse_obj({
        'id': 1,
        'username': 'admin',
        'name': 'Admin'
    })
