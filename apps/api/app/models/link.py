from sqlalchemy import Column, Integer, String, DateTime
from app.db import Base
import datetime


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String, unique=True, index=True, nullable=False)

    long_url = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    expires_at = Column(DateTime, nullable=True)