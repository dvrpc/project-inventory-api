from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database.core import Base


class Agency(Base):
    __tablename__ = "agency"

    agency_id = Column(Integer, primary_key=True, index=True)
    agency_group_id = Column(
        Integer,
        ForeignKey("agency_group.agency_group_id"),
        nullable=False,
        index=True,
    )
    name = Column(String(250), nullable=False)

    agency_group = relationship("AgencyGroup", back_populates="agencies")
    external_projects = relationship("ExternalProject", back_populates="agency")
