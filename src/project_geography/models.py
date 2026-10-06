from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from src.database.core import Base


class ProjectGeography(Base):
    __tablename__ = "product_geography"

    pub_id = Column(
        String(20),
        ForeignKey("TBLPUBLICATION.pub_id"),
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

    project = relationship("Project", back_populates="project_geographies")
    geography = relationship("Geography", back_populates="project_geographies")
