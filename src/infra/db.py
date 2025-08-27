from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

def get_engine(sqlite_path: str) -> Engine:
    # SQLite for demo; swap out with SAP HANA / others in production
    return create_engine(f"sqlite:///{sqlite_path}", future=True)
