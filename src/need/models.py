from sqlalchemy import Column, Integer, String, ForeignKey
from database.core import Base
from models import TimeStampMixin

class Need(Base, TimeStampMixin):
    __tablename__ = "need"

    need_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.project_id"), nullable=False)
    description = Column(String(4000), nullable=False)
