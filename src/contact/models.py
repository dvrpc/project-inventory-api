from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from src.database.core import Base
from src.models import TimeStampMixin

class Contact(Base, TimeStampMixin):
    __tablename__ = "contact"

    contact_id = Column(Integer, primary_key=True, index=True)
    agency_id = Column(Integer, ForeignKey("agency.agency_id"), nullable=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(250), nullable=False)
    phone = Column(String(20), nullable=True)
    job_title = Column(String(100), nullable=True)
    verified = Column(Boolean, default=False, nullable=True)
