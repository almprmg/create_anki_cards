# app/core/card_services.py
from app.models.card import Card
from app.infrastructure.repositories.card_repository import CardRepository

from app.core.deck_services import DeckService
from app.infrastructure.messaging.ai_queue import publish_generation_request, ConnectionError as RedisConnectionError
from .exceptions import DeckNotFound, CardNotFound, NotAuthorizedError, ValidationError

class CardService:
    def __init__(self):
        self.card_repository = CardRepository()
        # إنشاء كائن من خدمة الباقات للوصول إلى وظائفها
        self.deck_service = DeckService()

    def add_card_to_deck(self, deck_id: int, user_id: int, role: str, question: str, answer: str) -> Card:
        """إضافة بطاقة جديدة إلى باقة."""
        # 1. التحقق من وجود الباقة وصلاحية المستخدم عليها
        try:
            # نستخدم دالة جلب الباقة مع التحقق من الصلاحية
            deck = self.deck_service.get_deck_by_id_for_user(deck_id, user_id, role)
        except DeckNotFound:
             raise DeckNotFound(f"Cannot add card. Deck with ID {deck_id} not found.")
        except NotAuthorizedError:
             raise NotAuthorizedError(f"You are not authorized to add cards to deck {deck_id}.")

        # 2. التحقق من صحة بيانات البطاقة
        if not question or len(question.strip()) == 0:
            raise ValidationError("Card question cannot be empty.")
        if not answer or len(answer.strip()) == 0:
            raise ValidationError("Card answer cannot be empty.")

        # 3. إنشاء كائن البطاقة وإضافته
        new_card = Card(
            question=question.strip(),
            answer=answer.strip(),
            deck_id=deck.id # استخدام deck.id للتأكيد
        )
        return self.card_repository.add(new_card)

    def get_cards_in_deck(self, deck_id: int, user_id: int, role: str) -> list[Card]:
        """جلب كل البطاقات الموجودة في باقة معينة."""
        # 1. التحقق من وجود الباقة وصلاحية المستخدم عليها
        try:
            # يكفي التحقق من أن المستخدم يمكنه الوصول للباقة
            self.deck_service.get_deck_by_id_for_user(deck_id, user_id, role)
        except DeckNotFound:
            raise DeckNotFound(f"Cannot get cards. Deck with ID {deck_id} not found.")
        except NotAuthorizedError:
            raise NotAuthorizedError(f"You are not authorized to view cards in deck {deck_id}.")

        # 2. جلب البطاقات من المستودع
        return self.card_repository.get_by_deck_id(deck_id)

    def get_card_by_id(self, card_id: int, deck_id: int, user_id: int, role: str) -> Card:
         """جلب بطاقة محددة مع التحقق من الصلاحية والانتماء للباقة."""
         # 1. التحقق من صلاحية الوصول للباقة الأم
         try:
             self.deck_service.get_deck_by_id_for_user(deck_id, user_id, role)
         except DeckNotFound:
             raise DeckNotFound(f"Cannot access card. Parent deck {deck_id} not found.")
         except NotAuthorizedError:
             raise NotAuthorizedError(f"You are not authorized to access resources in deck {deck_id}.")

         # 2. جلب البطاقة نفسها
         card = self.card_repository.get_by_id(card_id)
         if not card:
             raise CardNotFound(f"Card with ID {card_id} not found.")

         # 3. التأكد من أن البطاقة تنتمي فعلاً للباقة المطلوبة
         if card.deck_id != deck_id:
             # هذا يجب ألا يحدث إذا كانت الـ URL صحيحة، لكنه فحص أمان إضافي
             raise NotAuthorizedError(f"Card {card_id} does not belong to deck {deck_id}.")

         return card

    def update_card(self, card_id: int, deck_id: int, user_id: int, role: str, data_to_update: dict) -> Card:
        """تحديث بيانات بطاقة موجودة."""
        # 1. جلب البطاقة مع التحقق من الصلاحية والانتماء للباقة
        # دالة get_card_by_id تقوم بكل التحققات اللازمة (وجود الباقة، صلاحية المستخدم، وجود البطاقة، انتماء البطاقة للباقة)
        card_to_update = self.get_card_by_id(card_id, deck_id, user_id, role)

        # 2. التحقق من صحة البيانات وتحديث الحقول
        updated = False
        if 'question' in data_to_update:
            new_question = data_to_update['question']
            if not new_question or len(new_question.strip()) == 0:
                raise ValidationError("Card question cannot be empty.")
            card_to_update.question = new_question.strip()
            updated = True

        if 'answer' in data_to_update:
            new_answer = data_to_update['answer']
            if not new_answer or len(new_answer.strip()) == 0:
                raise ValidationError("Card answer cannot be empty.")
            card_to_update.answer = new_answer.strip()
            updated = True

        if not updated:
             raise ValidationError("No valid fields provided for update ('question', 'answer').")

        # 3. حفظ التغييرات
        return self.card_repository.update(card_to_update)

    def delete_card(self, card_id: int, deck_id: int, user_id: int, role: str) -> None:
        """حذف بطاقة موجودة."""

        card_to_delete = self.get_card_by_id(card_id, deck_id, user_id, role)

        self.card_repository.delete(card_to_delete)
    def request_ai_card_generation(self, deck_id: int, user_id: int, role: str, generation_params: dict) -> None:
        """طلب توليد بطاقات باستخدام AI Service عبر Redis."""
        # 1. التحقق من وجود الباقة وصلاحية المستخدم عليها
        try:
            # يكفي التأكد من أن المستخدم يمكنه الوصول إلى الباقة
            self.deck_service.get_deck_by_id_for_user(deck_id, user_id, role)
        except DeckNotFound:
            raise DeckNotFound(f"Cannot request AI generation. Deck with ID {deck_id} not found.")
        except NotAuthorizedError:
            raise NotAuthorizedError(f"You are not authorized to modify deck {deck_id}.")

        # 2. التحقق من معايير التوليد (مثال بسيط)
        topic = generation_params.get('topic')
        num_cards = generation_params.get('num_cards', 5) # عدد افتراضي 5
        if not topic or len(topic.strip()) == 0:
            raise ValidationError("Generation topic cannot be empty.")
        if not isinstance(num_cards, int) or num_cards <= 0 or num_cards > 20: # تحديد حد أقصى
             raise ValidationError("Number of cards must be a positive integer (max 20).")

        # 3. بناء رسالة الطلب
        message_payload = {
            "deck_id": deck_id,
            "user_id": user_id, # قد تحتاج AI Service لمعرفة من طلب التوليد
            "topic": topic.strip(),
            "num_cards": num_cards,
            # يمكن إضافة معايير أخرى مثل مستوى الصعوبة، اللغة، إلخ.
            "generation_options": generation_params.get("options", {})
        }

        # 4. نشر الرسالة إلى Redis
        try:
            publish_generation_request(message_payload)
            # لا يوجد شيء لإرجاعه هنا لأن العملية غير متزامنة
        except RedisConnectionError as e:
             # التعامل مع خطأ اتصال Redis - قد تحتاج لإعادة المحاولة أو تسجيل الخطأ
             # أو إرجاع خطأ 503 Service Unavailable للمستخدم
             raise ConnectionError(f"Could not queue AI request due to messaging system issue: {e}")
        except Exception as e:
            # التعامل مع أخطاء النشر الأخرى
            raise RuntimeError(f"Failed to queue AI request: {e}")