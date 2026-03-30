from sqlalchemy import Column, Integer, String, Date, Numeric
from sqlalchemy.orm import relationship
from src.database.core import Base


class Product(Base):
    __tablename__ = "TBLPUBLICATION"
    __table_args__ = {"schema": "DVRPC_PRODUCTS"}

    pub_id = Column(String(20), nullable=False)
    typecode = Column(String(5), nullable=False, primary_key=True)
    pub_num = Column(String(10), nullable=False, primary_key=True)
    title = Column(String(250), nullable=True)
    subtitle = Column(String(250), nullable=True)
    keywords = Column(String(4000), nullable=True)
    abstract = Column(String(4000), nullable=True)
    createdate = Column(Date, nullable=True)
    livedate = Column(Date, nullable=True)
    lastupdatedate = Column(Date, nullable=True)
    pub_date = Column(Date, nullable=True)
    createby = Column(String(50), nullable=True)
    status = Column(String(30), nullable=True)

    wpids = relationship(
        "ProductWpid",
        primaryjoin="and_(Product.pub_id == ProductWpid.PRODUCTID)",
        foreign_keys="[ProductWpid.PRODUCTID]",
    )
