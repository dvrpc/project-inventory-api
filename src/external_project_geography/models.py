from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.database.core import Base


class ExternalProjectGeography(Base):
    __tablename__ = "external_project_geography"

    external_project_id = Column(
        Integer,
        ForeignKey("EXTERNAL_PROJECT.id"),
        nullable=False,
        primary_key=True,
        index=True,
    )
    geoid = Column(
        String(10),
        ForeignKey("geography.geoid", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
        index=True,
    )

    external_project = relationship(
        "ExternalProject", back_populates="external_project_geographies"
    )
    geography = relationship(
        "Geography", back_populates="external_project_geographies"
    )
