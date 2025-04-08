# app/models/deck.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Deck(Base, TimestampMixin):
    __tablename__ = 'decks'

    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)

    user_id = Column(Integer, nullable=False, index=True) 

# One-to-many-card relationship
# cascade="all,delete-orphan": When a card is deleted, all its cards are deleted.
    cards = relationship("Card", back_populates="deck", cascade="all, delete-orphan", lazy="dynamic")

    def __repr__(self):
        return f"<Deck(id={self.id}, title='{self.title}', user_id={self.user_id})>"