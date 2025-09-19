import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session

# URL de conexão ao banco de dados padrão
SCHEMA_NAME = "socorro_tb"
DATABASE_URL = f"postgresql+psycopg://u_grupo02:grupo02@200.144.245.12:45432/db_grupo02"


# Crie o engine com o schema padrão 'api'
engine = create_engine(DATABASE_URL, connect_args={"options": f"-csearch_path={SCHEMA_NAME}"})


SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()