# app/core/deck_services.py
from app.models.deck import Deck
from app.infrastructure.repositories.deck_repository import DeckRepository
# استيراد الاستثناءات المخصصة
from .exceptions import DeckNotFound, NotAuthorizedError, ValidationError

class DeckService:
    def __init__(self):
        self.repository = DeckRepository()

    def create_deck(self, user_id: int, title: str, description: str | None = None) -> Deck:

        if not title or len(title.strip()) == 0:
            raise ValidationError("Deck title cannot be empty.")
        if len(title) > 150:
             raise ValidationError("Deck title cannot exceed 150 characters.")

        new_deck = Deck(
            title=title.strip(),
            description=description.strip() if description else None,
            user_id=user_id
        )
        return self.repository.add(new_deck)

    def get_decks_by_user(self, user_id: int) -> list[Deck]:
 
        return self.repository.get_by_user_id(user_id)

    def get_deck_by_id(self, deck_id: int) -> Deck:
        """جلب باقة بواسطة ID بدون التحقق من الصلاحية (للاستخدام الداخلي)."""
        deck = self.repository.get_by_id(deck_id)
        if not deck:
            raise DeckNotFound(f"Deck with ID {deck_id} not found.")
        return deck

    def _check_authorization(self, deck: Deck, user_id: int, role: str):
 
        if deck.user_id != user_id and role != 'admin':
            raise NotAuthorizedError("You do not have permission to access this deck.")

    def get_deck_by_id_for_user(self, deck_id: int, user_id: int, role: str) -> Deck:
        """جلب باقة مع التحقق من الصلاحية."""
        deck = self.get_deck_by_id(deck_id)
        self._check_authorization(deck, user_id, role)
        return deck

    def get_all_decks(self, role: str) -> list[Deck]:
        """جلب كل الباقات (للمشرف فقط)."""
        if role != 'admin':
     
            raise NotAuthorizedError("Only admins can access all decks.")
        return self.repository.get_all()

    def update_deck(self, deck_id: int, user_id: int, role: str, data_to_update: dict) -> Deck:
        """تحديث بيانات باقة موجودة."""
        deck_to_update = self.get_deck_by_id(deck_id) 
        self._check_authorization(deck_to_update, user_id, role)

        # Update only allowed fields
        if 'title' in data_to_update:
            new_title = data_to_update['title']
            if not new_title or len(new_title.strip()) == 0:
                 raise ValidationError("Deck title cannot be empty.")
            if len(new_title) > 150:
                 raise ValidationError("Deck title cannot exceed 150 characters.")
            deck_to_update.title = new_title.strip()

        if 'description' in data_to_update:
             # Allow empty description by sending "" or null/None
             new_desc = data_to_update['description']
             deck_to_update.description = new_desc.strip() if new_desc else None


        return self.repository.update(deck_to_update)

    def delete_deck(self, deck_id: int, user_id: int, role: str) -> None:
        """حذف باقة موجودة."""
        deck_to_delete = self.get_deck_by_id(deck_id)
        self._check_authorization(deck_to_delete, user_id, role) 

        self.repository.delete(deck_to_delete)
