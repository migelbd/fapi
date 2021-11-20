from fastapi import FastAPI

from app import schema
from app.database import database
from app.initializer import init

app = FastAPI(title='Some API', version='0.0.1')
init(app)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/ping', response_model=schema.PingResponse, include_in_schema=False)
async def ping():
    db_ping = await database.execute('SELECT now()')
    data = dict(
        status=True,
        db_is_online=bool(db_ping)
    )
    return schema.PingResponse.parse_obj(data)
