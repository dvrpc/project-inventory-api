from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from src.database.core import Base

class ProjectGeography(Base):
    __tablename__ = "project_geography"

    project_id = Column(Integer, ForeignKey("project.project_id", ondelete="CASCADE"), nullable=False, primary_key=True)
    geography_id = Column(Integer, ForeignKey("geography.geoid", ondelete="CASCADE"), nullable=False, primary_key=True)

    project = relationship("Project", back_populates="project_geographies")
    geography = relationship("Geography", back_populates="project_geographies")
