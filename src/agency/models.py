from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.core import Base
from src.models import TimeStampMixin

class Agency(Base, TimeStampMixin):
    __tablename__ = "agency"

    agency_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    address = Column(String(500), nullable=True)
    email = Column(String(250), nullable=True)
    phone = Column(String(5200), nullable=True)

    external_products = relationship("ExternalProduct", back_populates="agency")
