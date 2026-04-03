from sqlalchemy import Column, Index, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.database.core import Base
from src.models import TimeStampMixin


class Project(Base, TimeStampMixin):
    __tablename__ = "project"

    project_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        String(20),
        ForeignKey("DVRPC_PRODUCTS.TBLPUBLICATION.pub_id"),
        nullable=True,
        index=True,
    )
    external_product_id = Column(
        Integer, ForeignKey("external_product.product_id"), nullable=True, index=True
    )
    internal = Column(Boolean, nullable=False)

    product = relationship("Product")
    external_product = relationship("ExternalProduct")
    needs = relationship("Need", back_populates="projects")
    recommendations = relationship("Recommendation", back_populates="projects")

    project_geographies = relationship(
        "ProjectGeography",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    project_keywords = relationship(
        "ProjectKeyword",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (Index("ix_project_product_internal", "product_id", "internal"),)
