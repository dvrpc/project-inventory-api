from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.core import Base
from src.models import TimeStampMixin

class Recommendation(Base, TimeStampMixin):
    __tablename__ = "recommendation"

    recommendation_id = Column(Integer, primary_key=True, index=True)
    pub_id = Column(
        String(20),
        ForeignKey("TBLPUBLICATION.pub_id"),
        nullable=False,
        index=True,
    )
    description = Column(String(4000), nullable=False)

    # project = relationship("Project", back_populates="recommendations")
