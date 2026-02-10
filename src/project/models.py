from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database.core import Base
from models import TimeStampMixin

class Project(Base, TimeStampMixin):
    __tablename__ = "project"

    project_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String(20), ForeignKey("product.pub_id"), nullable=True)
    external_product_id = Column(Integer, ForeignKey("external_product.product_id"), nullable=True)
    internal = Column(Boolean, nullable=False)
