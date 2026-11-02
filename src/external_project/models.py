from sqlalchemy import Column, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from src.database.core import Base


class ExternalProject(Base):
    __tablename__ = "EXTERNAL_PROJECT"

    id = Column(Integer, primary_key=True)
    source_system = Column(String(50), nullable=False)
    source_key = Column(String(200), nullable=False)
    title = Column(String(500), nullable=False)
    abstract = Column(Text, nullable=True)
    status = Column(String(20), nullable=False)
    year = Column(Integer, nullable=True)
    project_link = Column(String(1000), nullable=True)
    agency = Column(String(255), nullable=True)

    external_project_geographies = relationship(
        "ExternalProjectGeography",
        back_populates="external_project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "source_system", "source_key", name="UQ_EXT_PROJECT_SOURCE"
        ),
    )
