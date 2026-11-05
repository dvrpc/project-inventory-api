from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.core import Base


class AgencyGroup(Base):
    __tablename__ = "agency_group"

    agency_group_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False, unique=True)

    agencies = relationship("Agency", back_populates="agency_group")
