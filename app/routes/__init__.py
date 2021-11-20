from fastapi import Depends

from .info import router as info_router


from ..schema.internal import TypedAPIRouter
from ..security import get_user_by_token

info_router = TypedAPIRouter(
    router=info_router,
    prefix='/test',
    tags=['test'],
    dependencies=[Depends(get_user_by_token)]
)

