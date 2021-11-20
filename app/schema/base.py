from typing import Union, Optional

from pydantic import BaseModel


class StatusResponse(BaseModel):
    status: bool = True
    data: Optional[Union[dict, list]]


class PingResponse(BaseModel):
    status: bool
    db_is_online: bool