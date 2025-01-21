from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_URL

engine = create_engine(DB_URL, pool_pre_ping=True, pool_size=20, max_overflow=10)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()
