from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.core import Base

class Geography(Base):
    __tablename__ = "geography"

    geography_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    geo_type = Column(String(500), nullable=False)
    geoid = Column(String(250), nullable=True)

    projects = relationship("Project", secondary="project_geography", back_populates="geographies")
    project_geographies = relationship("ProjectGeography", back_populates="geography")
