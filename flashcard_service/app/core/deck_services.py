
from app.models.deck import Deck
from app.infrastructure.repositories.deck_repository import DeckRepository


class DeckService:
    def __init__(self):
        self.repository = DeckRepository()

    def create_deck(self, user_id: int, title: str, description: str | None = None) -> Deck:
        """إنشاء باقة جديدة."""
        if not title:
            raise ValueError("Deck title cannot be empty") # مثال بسيط للتحقق

        new_deck = Deck(
            title=title,
            description=description,
            user_id=user_id # تأكد من أن النوع متوافق
        )
        return self.repository.add(new_deck)

    def get_decks_by_user(self, user_id: int) -> list[Deck]:
        """جلب باقات المستخدم."""
        return self.repository.get_by_user_id(user_id)

    def get_deck_by_id_for_user(self, deck_id: int, user_id: int, role: str) -> Deck | None:
        """جلب باقة مع التحقق من الصلاحية."""
        deck = self.repository.get_by_id(deck_id)
        if not deck:
            return None # أو أثر استثناء DeckNotFound

        # التحقق من الصلاحية
        if deck.user_id == user_id or role == 'admin':
            return deck
        else:
            # أثر استثناء NotAuthorized أو أرجع None حسب المنطق المفضل
            raise PermissionError("User not authorized to access this deck")

    def get_all_decks(self, role: str) -> list[Deck]:
        """جلب كل الباقات (للمشرف فقط)."""
        if role != 'admin':
            raise PermissionError("Only admins can access all decks")
        return self.repository.get_all()

    # --- دوال التعديل والحذف ستضاف لاحقًا ---