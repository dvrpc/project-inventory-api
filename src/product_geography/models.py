from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from src.database.core import Base


class ProductGeography(Base):
    __tablename__ = "product_geography"

    pub_id = Column(
        String(20),
        ForeignKey("TBLPUBLICATION.pub_id"),
        nullable=False,
        primary_key=True,
        index=True,
    )
    geoid = Column(
        String(10),
        ForeignKey("geography.geoid", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
        index=True,
    )

    product = relationship("Product", back_populates="product_geographies")
    geography = relationship("Geography", back_populates="product_geographies")


# Deprecated alias - remove once services/routers are refactored to Product
ProductGeography = ProductGeography
