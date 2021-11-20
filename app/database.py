import databases
import sqlalchemy

from app.config import settings

cfg = settings()
# SQLAlchemy specific code, as with any other app
# DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(cfg.db_connection_string())

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    cfg.db_connection_string(), connect_args={"check_same_thread": False}
)