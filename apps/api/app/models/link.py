from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime

from app.db import Base


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    long_url = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    created_by = Column(
        String,
        nullable=True,
    )

    expires_at = Column(
        DateTime,
        nullable=True,
    )

    tags = Column(
        JSON,
        nullable=True,
    )