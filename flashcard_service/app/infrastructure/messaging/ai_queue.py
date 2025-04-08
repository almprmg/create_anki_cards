# app/infrastructure/messaging/ai_queue.py
import redis
import json
from flask import current_app # للوصول إلى إعدادات التطبيق


redis_client = None

def get_redis_client():
    """الحصول على كائن اتصال Redis."""
    global redis_client
    if redis_client is None:
        try:
            redis_url = current_app.config['REDIS_URL']
            # decode_responses=True يجعل النتائج تعود كنصوص (strings) بدلاً من bytes
            redis_client = redis.from_url(redis_url, decode_responses=True)
            # التحقق من الاتصال
            redis_client.ping()
            current_app.logger.info(f"Successfully connected to Redis at {redis_url}")
        except redis.exceptions.ConnectionError as e:
            current_app.logger.error(f"Failed to connect to Redis at {redis_url}: {e}")
            # يمكنك هنا إثارة خطأ أو التعامل معه حسب الحاجة
            redis_client = None # تعيينه None مرة أخرى ليشير إلى فشل الاتصال
            raise ConnectionError(f"Could not connect to Redis: {e}")
        except Exception as e:
             current_app.logger.error(f"An unexpected error occurred during Redis connection: {e}")
             redis_client = None
             raise ConnectionError(f"Unexpected error connecting to Redis: {e}")

    return redis_client

def publish_generation_request(message_data: dict):
    """نشر رسالة طلب توليد بطاقات إلى قناة Redis."""
    try:
        client = get_redis_client()
        if not client:
      
             raise ConnectionError("Redis client is not available.")

        channel = current_app.config['REDIS_AI_REQUEST_CHANNEL']

        message_json = json.dumps(message_data)

      
        num_subscribers = client.publish(channel, message_json)
        current_app.logger.info(f"Published message to channel '{channel}'. Payload: {message_json}. Notified {num_subscribers} subscribers.")
        return num_subscribers
    except ConnectionError as e:

         current_app.logger.error(f"Redis connection error during publish: {e}")
         raise e 
    except Exception as e:
        current_app.logger.error(f"Failed to publish message to Redis channel '{channel}': {e}")
  
        raise RuntimeError(f"Failed to publish to Redis: {e}")

# يمكنك إضافة دالة للاشتراك هنا إذا كان العامل جزءًا من نفس الكود
# لكن من الأفضل أن يكون العامل عملية منفصلة