
import jwt
from functools import wraps
from flask import request, g, current_app, abort # abort to abort the request with an error code
# i will change to flask wt
def jwt_required(f):
    """
 
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]

        if not token:
            abort(401, description="Authorization token is missing.")

        try:

            secret_key = current_app.config.get('JWT_SECRET_KEY')
            if not secret_key:
                 raise ValueError("JWT_SECRET_KEY is not configured.")

            payload = jwt.decode(
                token,
                secret_key,
                algorithms=["HS256"] # تأكد من تطابق الخوارزمية مع Auth Service
            )

            # --- نقطة مهمة ---
            # تأكد من أسماء الحقول الصحيحة في الـ payload المرسل من Auth Service
            user_id = payload.get('user_id') # أو 'sub' أو أي حقل معرف للمستخدم
            role = payload.get('role')       # أو 'roles' أو اسم الحقل المستخدم للصلاحيات

            if user_id is None or role is None:
                abort(401, description="Invalid token payload.")

            # إرفاق البيانات بـ flask.g ليسهل الوصول إليها في الـ view function
            g.user_id = user_id
            g.role = role

        except jwt.ExpiredSignatureError:
            abort(401, description="Token has expired.")
        except jwt.InvalidTokenError as e:
            current_app.logger.error(f"Invalid token: {e}") # تسجيل الخطأ للمساعدة في التصحيح
            abort(401, description="Invalid token.")
        except ValueError as e:
            current_app.logger.error(f"Configuration error: {e}")
            abort(500, description="Server configuration error regarding JWT.")
        except Exception as e:
            current_app.logger.error(f"Unexpected error during JWT decoding: {e}")
            abort(500, description="Could not process token.")


        return f(*args, **kwargs)
    return decorated_function