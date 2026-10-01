from sqlalchemy import Column, Index, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.database.core import Base
from src.models import TimeStampMixin


# DEPRECATED: Project is being removed in favor of Product (TBLPUBLICATION.pub_id)
# as the central object. Child tables (need, recommendation, attachment,
# product_geography, product_keyword) now FK directly to Product.
# This model is kept temporarily so existing service imports don't break.
# Delete this file once services/routers are refactored.
class Project(Base, TimeStampMixin):
    __tablename__ = "project"

    project_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        String(20),
        ForeignKey("TBLPUBLICATION.pub_id"),
        nullable=True,
        index=True,
    )
    external_product_id = Column(
        Integer, ForeignKey("external_product.product_id"), nullable=True, index=True
    )
    internal = Column(Boolean, nullable=False)

    product = relationship("Product")
    external_product = relationship("ExternalProduct")

    __table_args__ = (Index("ix_project_product_internal", "product_id", "internal"),)
