
from app.models.card import Card
from app.infrastructure.database import db_session
from typing import List, Optional # لاستخدام Type Hinting

class CardRepository:
    def add(self, card: Card) -> Card:
        """إضافة بطاقة جديدة إلى قاعدة البيانات."""
        db_session.add(card)
        db_session.commit()
        db_session.refresh(card)
        return card

    def get_by_id(self, card_id: int) -> Optional[Card]:
        """جلب بطاقة بواسطة الـ ID."""
        return db_session.query(Card).filter(Card.id == card_id).first()

    def get_by_deck_id(self, deck_id: int) -> List[Card]:
        """جلب كل البطاقات لباقة معينة."""
        return db_session.query(Card).filter(Card.deck_id == deck_id).all()

    def update(self, card: Card) -> Card:
        """حفظ التغييرات على بطاقة موجودة."""
        db_session.add(card) # التأكد من أن الكائن في الجلسة
        db_session.commit()
        db_session.refresh(card)
        return card

    def delete(self, card: Card) -> None:
        """حذف بطاقة من قاعدة البيانات."""
        db_session.delete(card)
        db_session.commit()