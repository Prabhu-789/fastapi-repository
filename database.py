# from sqlalchemy.orm import declarative_base,sessionmaker
# from sqlalchemy import create_engine
# engine = create_engine("postgresql://postgres:Teja%401234@localhost/User",echo=True)

# Base= declarative_base()
# SessionLocal=sessionmaker(bind=engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://postgres:Teja%401234@db/User"

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
