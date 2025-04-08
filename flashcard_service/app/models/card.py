# app/models/card.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Card(Base, TimestampMixin):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    deck_id = Column(Integer, ForeignKey('decks.id'), nullable=False, index=True)

    # Many-to-one relationship with the package
    deck = relationship("Deck", back_populates="cards")

    def __repr__(self):
        return f"<Card(id={self.id}, deck_id={self.deck_id}, question='{self.question[:20]}...')>"