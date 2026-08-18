from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import declarative_base


# Base class for all SQLAlchemy models
Base = declarative_base()


class ReviewPrediction(Base):
    """
    Database table for storing sentiment predictions.
    """

    __tablename__ = "review_predictions"

    id = Column(Integer, primary_key=True, index=True)

    review = Column(Text, nullable=False)

    sentiment = Column(String(20), nullable=False)

    confidence = Column(Float, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
