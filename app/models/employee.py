from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("pages.id"), nullable=False)

    name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    page = relationship("Page", back_populates="employees")
