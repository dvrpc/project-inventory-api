from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.core import Base
from src.models import TimeStampMixin

class Recommendation(Base, TimeStampMixin):
    __tablename__ = "recommendation"

    recommendation_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.project_id"), nullable=False)
    description = Column(String(4000), nullable=False)

    projects = relationship("Project", back_populates="recommendations")
