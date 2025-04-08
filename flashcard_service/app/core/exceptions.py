
class ApplicationException(Exception):
    """Base exception class for the application."""
    status_code = 500
    message = "An internal server error occurred."

    def __init__(self, message=None, status_code=None):
        super().__init__(message or self.message)
        if status_code is not None:
            self.status_code = status_code

class NotFoundError(ApplicationException):
    """Raised when a resource is not found."""
    status_code = 404
    message = "Resource not found."

class DeckNotFound(NotFoundError):
    """Raised when a specific deck is not found."""
    message = "Deck not found."

class CardNotFound(NotFoundError):
     """Raised when a specific card is not found."""
     message = "Card not found."

class NotAuthorizedError(ApplicationException):
    """Raised when a user is not authorized to perform an action."""
    status_code = 403
    message = "You are not authorized to perform this action."

class ValidationError(ApplicationException):
    """Raised for validation errors (e.g., invalid input)."""
    status_code = 400
    message = "Validation Error."