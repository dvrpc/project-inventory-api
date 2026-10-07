from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.core import Base


class Topic(Base):
    __tablename__ = "TBLTOPICLOOKUP"

    topic_id = Column(Integer, primary_key=True, index=True)
    topic_name = Column(String(100), nullable=False)

    project_topics = relationship(
        "ProjectTopic", back_populates="topic", passive_deletes=True
    )
