from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from src.database.core import Base

class ProjectGeography(Base):
    __tablename__ = "project_geography"

    project_id = Column(Integer, ForeignKey("project.project_id"), nullable=False, primary_key=True)
    geography_id = Column(Integer, ForeignKey("geography.geography_id"), nullable=False, primary_key=True)
