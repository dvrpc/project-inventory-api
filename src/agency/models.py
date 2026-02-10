from sqlalchemy import Column, Integer, String
from database.core import Base
from models import TimeStampMixin

class Agency(Base, TimeStampMixin):
    __tablename__ = "agency"

    agency_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    address = Column(String(500), nullable=True)
    email = Column(String(250), nullable=True)
    phone = Column(String(5200), nullable=True)
