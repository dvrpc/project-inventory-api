from sqlalchemy import Column, Integer, String, Date
from src.database.core import Base


class ProjectWpid(Base):
    __tablename__ = "PRODUCTS_WPID"

    PRODUCTID = Column(String(20), nullable=False, primary_key=True)
    WORKPROGRAMID = Column(String(5), nullable=False, primary_key=True)
    ID = Column(Integer, nullable=False, primary_key=True)
    ADDBY = Column(String(50), nullable=True)
    ADDTIME = Column(Date, nullable=True)
