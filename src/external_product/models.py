from sqlalchemy import Column, Integer, String
from database.core import Base
from models import TimeStampMixin

class ExternalProduct(Base, TimeStampMixin):
    __tablename__ = "external_product"

    product_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(250), nullable=False)
    link = Column(String(250), nullable=False)
    abstract = Column(String(4000), nullable=False)
