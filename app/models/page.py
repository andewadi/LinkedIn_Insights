from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(String(255), unique=True, nullable=False, index=True)

    name = Column(String(255), nullable=False)
    url = Column(String(500))
    profile_picture = Column(String(500))

    description = Column(Text)
    website = Column(String(255))
    industry = Column(String(255))

    followers = Column(Integer, default=0)
    headcount = Column(Integer)

    specialities = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    posts = relationship("Post", back_populates="page", cascade="all, delete")
    employees = relationship("Employee", back_populates="page", cascade="all, delete")
