from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.database.core import Base


class ProjectKeyword(Base):
    __tablename__ = "project_keyword"

    project_id = Column(
        Integer,
        ForeignKey("project.project_id", ondelete="CASCADE"),
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

    project = relationship("Project", back_populates="project_keywords")
    keyword = relationship("Keyword", back_populates="project_keywords")
