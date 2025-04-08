
from flask import Blueprint, current_app, request, jsonify, g, abort
from app.core.deck_services import DeckService
from app.api.auth import jwt_required
from sqlalchemy.exc import SQLAlchemyError


decks_bp = Blueprint('decks_bp', __name__)

deck_service = DeckService()

@decks_bp.route('/decks', methods=['POST'])
@jwt_required # تطبيق الـ Decorator للتحقق من JWT
def create_deck_endpoint():
    """Endpoint لإنشاء باقة جديدة."""
    data = request.get_json()
    if not data or 'title' not in data:
        abort(400, description="Missing 'title' in request body.")

    title = data.get('title')
    description = data.get('description')
    user_id = g.user_id # الحصول على user_id من الـ Decorator

    try:
        new_deck = deck_service.create_deck(
            user_id=user_id,
            title=title,
            description=description
        )
        # تحويل الكائن إلى قاموس لإرجاعه كـ JSON
        deck_data = {
            "id": new_deck.id,
            "title": new_deck.title,
            "description": new_deck.description,
            "user_id": new_deck.user_id,
            "created_at": new_deck.created_at.isoformat(),
            "updated_at": new_deck.updated_at.isoformat()
        }
        return jsonify(deck_data), 201 # 201 Created
    except ValueError as e:
        abort(400, description=str(e))
    except SQLAlchemyError as e:
  
        current_app.logger.error(f"Database error on deck creation: {e}")
        abort(500, description="Database error occurred.")
    except Exception as e:
        current_app.logger.error(f"Unexpected error on deck creation: {e}")
        abort(500, description="An unexpected error occurred.")


@decks_bp.route('/decks', methods=['GET'])
@jwt_required
def get_decks_endpoint():
    """Endpoint to fetch user packages or all packages (for admin)."""
    user_id = g.user_id
    role = g.role

    try:
        if role == 'admin':

            decks = deck_service.get_all_decks(role=role)
        else:
            decks = deck_service.get_decks_by_user(user_id=user_id)

        decks_data = [
            {
                "id": deck.id,
                "title": deck.title,
                "description": deck.description,
                "user_id": deck.user_id,
                "created_at": deck.created_at.isoformat(),
                "updated_at": deck.updated_at.isoformat()
            } for deck in decks
        ]
        return jsonify(decks_data), 200
    except PermissionError as e:
         abort(403, description=str(e)) # 403 Forbidden
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error fetching decks: {e}")
        abort(500, description="Database error occurred.")
    except Exception as e:
        current_app.logger.error(f"Unexpected error fetching decks: {e}")
        abort(500, description="An unexpected error occurred.")

# --- Other Endpoints (GET by ID, PUT, DELETE) will be added here later ---