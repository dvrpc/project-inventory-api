from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.core import Base

class Geography(Base):
    __tablename__ = "geography"

    geoid = Column(String(10), primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    geo_type = Column(String(500), nullable=False)
    fips = Column(String(5), nullable=True)
    dvrpc_reg = Column(Boolean(create_constraint=True), nullable=False, default=False)


    projects = relationship("Project", secondary="project_geography", back_populates="geographies")
    project_geographies = relationship("ProjectGeography", back_populates="geography", passive_deletes=True)
