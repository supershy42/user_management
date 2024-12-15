import redis.asyncio as redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

ONLINE_USERS_KEY = 'online_users'
USER_CHANNELS_KEY_PREFIX = 'user_channels:'

async def add_user_to_online_users(user_id, channel_name):
    await redis_client.sadd(ONLINE_USERS_KEY, user_id)
    await redis_client.hset("user_channels", user_id, channel_name)

async def remove_user_from_online_users(user_id):
    await redis_client.srem(ONLINE_USERS_KEY, user_id)
    await redis_client.hdel("user_channels", user_id)