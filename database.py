from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

#db connection
db_url = "postgresql://postgres:Neha2910@localhost:5432/MyDatabase"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
