from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.core import Base


class ProjectTopic(Base):
    __tablename__ = "TBLPUBTOPIC"

    pub_id = Column(
        String(20),
        ForeignKey("TBLPUBLICATION.pub_id"),
        nullable=False,
        primary_key=True,
        index=True,
    )
    topic_id = Column(
        Integer,
        ForeignKey("TBLTOPICLOOKUP.topic_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
        index=True,
    )

    project = relationship("Project", back_populates="project_topics")
    topic = relationship("Topic", back_populates="project_topics")
