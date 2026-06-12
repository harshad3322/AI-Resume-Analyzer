from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship

from datetime import datetime

from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    reports = relationship(
        "Report",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Report(Base):
    __tablename__ = "reports"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    target_role = Column(
        String(100),
        nullable=False
    )

    ats_score = Column(
        Integer,
        default=0,
        nullable=False
    )

    resume_text = Column(
        Text,
        nullable=False
    )

    result = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="reports"
    )