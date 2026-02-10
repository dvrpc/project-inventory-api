from sqlalchemy import Column, Integer, String, LargeBinary, Date, ForeignKey
from database.core import Base
from models import TimeStampMixin

class Attachment(Base, TimeStampMixin):
    __tablename__ = "attachment"

    attachment_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.project_id"), nullable=True)
    file_name = Column(String(255), nullable=False)
    mime_type = Column(String(100), nullable=True)
    file_size = Column(Integer, nullable=True)
    file_content = Column(LargeBinary, nullable=True)
