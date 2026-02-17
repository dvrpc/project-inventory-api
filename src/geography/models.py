from sqlalchemy import Column, Integer, String
from src.database.core import Base

class Geography(Base):
    __tablename__ = "geography"

    geography_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    geo_type = Column(String(500), nullable=False)
    geoid = Column(String(250), nullable=True)
