from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship
from src.database.core import Base


class ProjectGeography(Base):
    __tablename__ = "project_geography"

    project_id = Column(
        String(10),
        ForeignKey("project.project_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
        index=True,
    )
    geography_id = Column(
        Integer,
        ForeignKey("geography.geoid", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
        index=True,
    )

    project = relationship("Project", back_populates="project_geographies")
    geography = relationship("Geography", back_populates="project_geographies")
