from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.core import Base


class ProjectKeyword(Base):
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
        ForeignKey("keyword.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
        index=True,
    )

    project = relationship("Project", back_populates="project_keywords")
    keyword = relationship("Keyword", back_populates="project_keywords")
