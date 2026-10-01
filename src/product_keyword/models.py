from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.core import Base


class ProductKeyword(Base):
    __tablename__ = "product_keyword"

    pub_id = Column(
        String(20),
        ForeignKey("TBLPUBLICATION.pub_id"),
        nullable=False,
        primary_key=True,
        index=True,
    )
    keyword_id = Column(
        Integer,
        ForeignKey("keyword.keyword_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
        index=True,
    )

    product = relationship("Product", back_populates="product_keywords")
    keyword = relationship("Keyword", back_populates="product_keywords")


# Deprecated alias - remove once services/routers are refactored to Product
ProductKeyword = ProductKeyword
