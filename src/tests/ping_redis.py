import redis

try:
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    redis_client.set("test_key", "Hello, This is Redis, and I am wokring now.")
    print("Connection successful:", redis_client.get("test_key"))
except redis.ConnectionError as e:
    print("Connection failed:", e)
