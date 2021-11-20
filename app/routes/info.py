from typing import List

import ujson
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.params import Query
from starlette import status

from app import schema
from app.config import settings

from app.security import get_user_by_token

router = APIRouter()


@router.post('/', response_model=schema.StatusResponse)
def get_info(current_user: schema.User = Depends(get_user_by_token)):
    cfg = settings()

    return schema.StatusResponse(data=cfg.dict())
