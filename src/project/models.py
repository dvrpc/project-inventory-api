from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.database.core import Base
from src.models import TimeStampMixin

class Project(Base, TimeStampMixin):
    __tablename__ = "project"

    project_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String(20), ForeignKey("DVRPC_PRODUCTS.TBLPUBLICATION.pub_id"), nullable=True)
    external_product_id = Column(Integer, ForeignKey("external_product.product_id"), nullable=True)
    internal = Column(Boolean, nullable=False)

    product = relationship("Product")
    external_product = relationship("ExternalProduct")
    needs = relationship("Need", back_populates="projects")
    recommendations = relationship("Recommendation", back_populates="projects")

