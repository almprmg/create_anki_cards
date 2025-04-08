from flask import Blueprint, request, jsonify, g, abort, current_app
from app.core.card_services import CardService
from app.api.auth import jwt_required
from app.core.exceptions import DeckNotFound, CardNotFound, NotAuthorizedError, ValidationError
from sqlalchemy.exc import SQLAlchemyError


cards_bp = Blueprint('cards_bp', __name__)

card_service = CardService()

# --- دالة مساعدة لتحويل كائن البطاقة إلى قاموس ---
def _card_to_dict(card):
    return {
        "id": card.id,
        "question": card.question,
        "answer": card.answer,
        "deck_id": card.deck_id,
        "created_at": card.created_at.isoformat() if card.created_at else None,
        "updated_at": card.updated_at.isoformat() if card.updated_at else None
    }


@cards_bp.route('/decks/<int:deck_id>/cards', methods=['POST'])
@jwt_required
def add_card_endpoint(deck_id):
    user_id = g.user_id
    role = g.role
    data = request.get_json()

    if not data or 'question' not in data or 'answer' not in data:
        abort(400, description="Missing 'question' or 'answer' in request body.")

    question = data.get('question')
    answer = data.get('answer')

    try:
        new_card = card_service.add_card_to_deck(
            deck_id=deck_id,
            user_id=user_id,
            role=role,
            question=question,
            answer=answer
        )
        return jsonify(_card_to_dict(new_card)), 201
    except (DeckNotFound, NotAuthorizedError, ValidationError) as e:
        abort(e.status_code, description=str(e))
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error adding card to deck {deck_id}: {e}")
        abort(500, description="Database error occurred.")
    except Exception as e:
        current_app.logger.error(f"Unexpected error adding card to deck {deck_id}: {e}")
        abort(500, description="An unexpected error occurred.")



@cards_bp.route('/decks/<int:deck_id>/cards', methods=['GET'])
@jwt_required
def get_cards_in_deck_endpoint(deck_id):
    user_id = g.user_id
    role = g.role

    try:
        cards = card_service.get_cards_in_deck(deck_id=deck_id, user_id=user_id, role=role)
        cards_data = [_card_to_dict(card) for card in cards]
        return jsonify(cards_data), 200
    except (DeckNotFound, NotAuthorizedError) as e:
        abort(e.status_code, description=str(e))
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error fetching cards for deck {deck_id}: {e}")
        abort(500, description="Database error occurred.")
    except Exception as e:
        current_app.logger.error(f"Unexpected error fetching cards for deck {deck_id}: {e}")
        abort(500, description="An unexpected error occurred.")



@cards_bp.route('/decks/<int:deck_id>/cards/<int:card_id>', methods=['GET'])
@jwt_required
def get_specific_card_endpoint(deck_id, card_id):
    user_id = g.user_id
    role = g.role

    try:
        card = card_service.get_card_by_id(
            card_id=card_id, deck_id=deck_id, user_id=user_id, role=role
        )
        return jsonify(_card_to_dict(card)), 200
    except (DeckNotFound, CardNotFound, NotAuthorizedError) as e:
        abort(e.status_code, description=str(e))
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error fetching card {card_id} from deck {deck_id}: {e}")
        abort(500, description="Database error occurred.")
    except Exception as e:
        current_app.logger.error(f"Unexpected error fetching card {card_id} from deck {deck_id}: {e}")
        abort(500, description="An unexpected error occurred.")



@cards_bp.route('/decks/<int:deck_id>/cards/<int:card_id>', methods=['PUT'])
@jwt_required
def update_card_endpoint(deck_id, card_id):
    user_id = g.user_id
    role = g.role
    data = request.get_json()

    if not data:
        abort(400, description="Request body cannot be empty for update.")

    allowed_updates = {}
    if 'question' in data:
        allowed_updates['question'] = data['question']
    if 'answer' in data:
        allowed_updates['answer'] = data['answer']

    if not allowed_updates:
         abort(400, description="No valid fields provided for update ('question', 'answer').")

    try:
        updated_card = card_service.update_card(
            card_id=card_id,
            deck_id=deck_id,
            user_id=user_id,
            role=role,
            data_to_update=allowed_updates
        )
        return jsonify(_card_to_dict(updated_card)), 200
    except (DeckNotFound, CardNotFound, NotAuthorizedError, ValidationError) as e:
        abort(e.status_code, description=str(e))
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error updating card {card_id} in deck {deck_id}: {e}")
        abort(500, description="Database error occurred.")
    except Exception as e:
        current_app.logger.error(f"Unexpected error updating card {card_id} in deck {deck_id}: {e}")
        abort(500, description="An unexpected error occurred.")



@cards_bp.route('/decks/<int:deck_id>/cards/<int:card_id>', methods=['DELETE'])
@jwt_required
def delete_card_endpoint(deck_id, card_id):
    user_id = g.user_id
    role = g.role

    try:
        card_service.delete_card(
            card_id=card_id, deck_id=deck_id, user_id=user_id, role=role
        )
        return '', 204 # No Content
    except (DeckNotFound, CardNotFound, NotAuthorizedError) as e:
        abort(e.status_code, description=str(e))
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error deleting card {card_id} from deck {deck_id}: {e}")
        abort(500, description="Database error occurred.")
    except Exception as e:
        current_app.logger.error(f"Unexpected error deleting card {card_id} from deck {deck_id}: {e}")
        abort(500, description="An unexpected error occurred.")