from sqlalchemy import Column, Integer, String, Date, Numeric
from sqlalchemy.orm import relationship
from src.database.core import Base


class Project(Base):
    __tablename__ = "TBLPUBLICATION"

    pub_id = Column(String(20), nullable=False, unique=True, index=True)
    typecode = Column(String(5), nullable=False, primary_key=True)
    pub_num = Column(String(10), nullable=False, primary_key=True)
    title = Column(String(250), nullable=True)
    subtitle = Column(String(250), nullable=True)
    # keywords = Column(String(4000), nullable=True)
    abstract = Column(String(4000), nullable=True)
    createdate = Column(Date, nullable=True)
    livedate = Column(Date, nullable=True)
    lastupdatedate = Column(Date, nullable=True)
    pub_date = Column(Date, nullable=True)
    s1 = Column(String(50), nullable=True)
    s1_id = Column(String(50), nullable=True)
    status = Column(String(30), nullable=True)

    wpids = relationship(
        "ProjectWpid",
        primaryjoin="and_(Project.pub_id == ProjectWpid.PRODUCTID)",
        foreign_keys="[ProjectWpid.PRODUCTID]",
    )
    # needs = relationship(
    #     "Need", back_populates="project", cascade="all, delete-orphan"
    # )
    # recommendations = relationship(
    #     "Recommendation", back_populates="project", cascade="all, delete-orphan"
    # )
    # attachments = relationship(
    #     "Attachment", back_populates="project", cascade="all, delete-orphan"
    # )
    project_geographies = relationship(
        "ProjectGeography",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    project_keywords = relationship(
        "ProjectKeyword",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    project_topics = relationship(
        "ProjectTopic",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
