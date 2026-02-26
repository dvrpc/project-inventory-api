from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from src.database.core import Base
from src.models import TimeStampMixin

class ExternalProduct(Base, TimeStampMixin):
    __tablename__ = "external_product"

    product_id = Column(Integer, primary_key=True, index=True)
    agency_id = Column(Integer, ForeignKey("agency.agency_id"), nullable = False)
    title = Column(String(250), nullable=False)
    link = Column(String(250), nullable=False)
    abstract = Column(String(4000), nullable=False)

    agency = relationship("Agency", back_populates="external_products")
