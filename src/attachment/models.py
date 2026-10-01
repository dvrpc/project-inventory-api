from sqlalchemy import Column, Integer, String, LargeBinary, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.database.core import Base
from src.models import TimeStampMixin

class Attachment(Base, TimeStampMixin):
    __tablename__ = "attachment"

    attachment_id = Column(Integer, primary_key=True, index=True)
    pub_id = Column(
        String(20),
        ForeignKey("TBLPUBLICATION.pub_id"),
        nullable=True,
        index=True,
    )
    file_name = Column(String(255), nullable=False)
    mime_type = Column(String(100), nullable=True)
    file_size = Column(Integer, nullable=True)
    file_content = Column(LargeBinary, nullable=True)

    product = relationship("Product", back_populates="attachments")
