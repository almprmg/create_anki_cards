# app/infrastructure/repositories/deck_repository.py
# (نضيف فقط الاستيرادات ونعدل التعليقات قليلاً، الدوال موجودة)
from app.models.deck import Deck
from app.infrastructure.database import db_session

class DeckRepository:
    def add(self, deck: Deck) -> Deck:
       
        db_session.add(deck)
        db_session.commit()
        db_session.refresh(deck)
        return deck

    def get_by_id(self, deck_id: int) -> Deck | None:
    
        # Use with_for_update() if there is a possibility of concurrent updates (optional)
        return db_session.query(Deck).filter(Deck.id == deck_id).first()

    def get_by_user_id(self, user_id: int) -> list[Deck]:

        return db_session.query(Deck).filter(Deck.user_id == user_id).all()

    def get_all(self) -> list[Deck]:

        return db_session.query(Deck).all()

    def update(self, deck: Deck) -> Deck:


        db_session.add(deck) 
        db_session.commit()
        db_session.refresh(deck)
        return deck

    def delete(self, deck: Deck) -> None:

        db_session.delete(deck)
        db_session.commit()