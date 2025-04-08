from app.models.deck import Deck
from app.infrastructure.database import db_session

class DeckRepository:
    def add(self, deck: Deck) -> Deck:
        """إضافة باقة جديدة إلى قاعدة البيانات."""
        db_session.add(deck)
        db_session.commit()
        db_session.refresh(deck) 
        return deck

    def get_by_id(self, deck_id: int) -> Deck | None:
        """جلب باقة بواسطة الـ ID."""
        return db_session.query(Deck).filter(Deck.id == deck_id).first()

    def get_by_user_id(self, user_id: int) -> list[Deck]:
        """جلب كل الباقات لمستخدم معين."""
   
        return db_session.query(Deck).filter(Deck.user_id == user_id).all()

    def get_all(self) -> list[Deck]:
        """جلب كل الباقات (للمشرف)."""
        return db_session.query(Deck).all()

    def update(self, deck: Deck) -> Deck:
        """تحديث بيانات باقة موجودة."""
        db_session.commit()
        db_session.refresh(deck)
        return deck

    def delete(self, deck: Deck) -> None:
        """حذف باقة من قاعدة البيانات."""
        db_session.delete(deck)
        db_session.commit()