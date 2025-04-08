# app/api/decks.py
from flask import Blueprint, request, jsonify, g, abort, current_app # استيراد current_app لتسجيل الأخطاء
from app.core.deck_services import DeckService
from app.api.auth import jwt_required

from app.core.exceptions import DeckNotFound, NotAuthorizedError, ValidationError
from sqlalchemy.exc import SQLAlchemyError

decks_bp = Blueprint('decks_bp', __name__)
deck_service = DeckService()

def _deck_to_dict(deck):
    return {
        "id": deck.id,
        "title": deck.title,
        "description": deck.description,
        "user_id": deck.user_id,
        "created_at": deck.created_at.isoformat() if deck.created_at else None,
        "updated_at": deck.updated_at.isoformat() if deck.updated_at else None
    }

@decks_bp.route('/decks', methods=['POST'])
@jwt_required
def create_deck_endpoint():
    data = request.get_json()
    if not data or 'title' not in data:
        abort(400, description="Missing 'title' in request body.")

    title = data.get('title')
    description = data.get('description')
    user_id = g.user_id

    try:
        # --- Logic to determine whether to fetch all or just the user ---
        # Example: Allow the admin to fetch all via query parameter ?all=true
        new_deck = deck_service.create_deck(
            user_id=user_id, title=title, description=description
        )
        return jsonify(_deck_to_dict(new_deck)), 201
    except ValidationError as e:
        abort(e.status_code, description=str(e))
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error on deck creation: {e}")
        abort(500, description="Database error occurred.")
    except Exception as e:
        current_app.logger.error(f"Unexpected error on deck creation: {e}")
        abort(500, description="An unexpected error occurred.")

@decks_bp.route('/decks', methods=['GET'])
@jwt_required
def get_decks_endpoint():
    user_id = g.user_id
    role = g.role

    try:
        # --- منطق تحديد ما إذا كان يجب جلب الكل أم فقط للمستخدم ---
        # مثال: السماح للمشرف بجلب الكل عبر query parameter ?all=true
        fetch_all = request.args.get('all', 'false').lower() == 'true'

        if fetch_all and role == 'admin':
             decks = deck_service.get_all_decks(role=role)
        else:
            # المستخدم العادي أو المشرف بدون ?all=true يحصل على باقاته فقط
            decks = deck_service.get_decks_by_user(user_id=user_id)

        decks_data = [_deck_to_dict(deck) for deck in decks]
        return jsonify(decks_data), 200
    except NotAuthorizedError as e:
         abort(e.status_code, description=str(e))
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error fetching decks: {e}")
        abort(500, description="Database error occurred.")
    except Exception as e:
        current_app.logger.error(f"Unexpected error fetching decks: {e}")
        abort(500, description="An unexpected error occurred.")

@decks_bp.route('/decks/<int:deck_id>', methods=['GET'])
@jwt_required
def get_deck_by_id_endpoint(deck_id):
    user_id = g.user_id
    role = g.role

    try:
        deck = deck_service.get_deck_by_id_for_user(
            deck_id=deck_id, user_id=user_id, role=role
        )
        return jsonify(_deck_to_dict(deck)), 200
    except DeckNotFound as e:
        abort(e.status_code, description=str(e))
    except NotAuthorizedError as e:
        abort(e.status_code, description=str(e))
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error fetching deck {deck_id}: {e}")
        abort(500, description="Database error occurred.")
    except Exception as e:
        current_app.logger.error(f"Unexpected error fetching deck {deck_id}: {e}")
        abort(500, description="An unexpected error occurred.")


@decks_bp.route('/decks/<int:deck_id>', methods=['PUT'])
@jwt_required
def update_deck_endpoint(deck_id):
    user_id = g.user_id
    role = g.role
    data = request.get_json()

    if not data:
        abort(400, description="Request body cannot be empty for update.")

    # تحديد الحقول المسموح بتحديثها (لتجنب تحديث user_id مثلاً)
    allowed_updates = {}
    if 'title' in data:
        allowed_updates['title'] = data['title']
    if 'description' in data:
        allowed_updates['description'] = data['description']

    if not allowed_updates:
         abort(400, description="No valid fields provided for update ('title', 'description').")

    try:
        updated_deck = deck_service.update_deck(
            deck_id=deck_id,
            user_id=user_id,
            role=role,
            data_to_update=allowed_updates
        )
        return jsonify(_deck_to_dict(updated_deck)), 200
    except (DeckNotFound, NotAuthorizedError, ValidationError) as e:
        abort(e.status_code, description=str(e))
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error updating deck {deck_id}: {e}")
        abort(500, description="Database error occurred.")
    except Exception as e:
        current_app.logger.error(f"Unexpected error updating deck {deck_id}: {e}")
        abort(500, description="An unexpected error occurred.")



@decks_bp.route('/decks/<int:deck_id>', methods=['DELETE'])
@jwt_required
def delete_deck_endpoint(deck_id):
    user_id = g.user_id
    role = g.role

    try:
        deck_service.delete_deck(deck_id=deck_id, user_id=user_id, role=role)
        # لا يوجد محتوى لإرجاعه عند الحذف بنجاح
        return '', 204 # 204 No Content
    except (DeckNotFound, NotAuthorizedError) as e:
        abort(e.status_code, description=str(e))
    except SQLAlchemyError as e:
        # التعامل مع حالة خاصة: إذا كان هناك بطاقات مرتبطة ولم يتم حذفها بسبب مشكلة في الـ cascade
        # أو إذا كان هناك foreign key constraint آخر.
        current_app.logger.error(f"Database error deleting deck {deck_id}: {e}")
        # قد يكون من الأفضل إرجاع خطأ 409 Conflict إذا كان السبب هو الاعتماديات
        if "violates foreign key constraint" in str(e).lower():
             abort(409, description="Cannot delete deck because it still has associated resources (e.g., cards). Ensure cascade delete is configured correctly.")
        else:
            abort(500, description="Database error occurred during deletion.")
    except Exception as e:
        current_app.logger.error(f"Unexpected error deleting deck {deck_id}: {e}")
        abort(500, description="An unexpected error occurred.")