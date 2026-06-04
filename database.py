from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
address = "postgresql://postgres:postgre123@localhost/expense-api"
engine = create_engine(address)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        











    