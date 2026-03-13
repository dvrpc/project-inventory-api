from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.core import Base
from src.models import TimeStampMixin

class Keyword(Base):
    __tablename__ = "keyword"

    keyword_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    project_keywords = relationship("ProjectKeyword", back_populates="keyword", passive_deletes=True)
