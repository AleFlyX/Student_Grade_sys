import aiomysql

from config import Config


class BaseMapper:
    _pool = None

    @classmethod
    async def get_pool(cls):
        if cls._pool is None:
            cls._pool = await aiomysql.create_pool(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                db=Config.DB_NAME,
                minsize=1,
                maxsize=Config.DB_POOL_SIZE,
                autocommit=True,
                charset="utf8mb4",
            )
        return cls._pool

    @classmethod
    async def close_pool(cls):
        if cls._pool is not None:
            cls._pool.close()
            await cls._pool.wait_closed()
            cls._pool = None

    @classmethod
    async def execute_query(cls, sql, params=None):
        pool = await cls.get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(sql, params or ())
                return await cursor.fetchall()

    @classmethod
    async def execute_one(cls, sql, params=None):
        pool = await cls.get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(sql, params or ())
                return await cursor.fetchone()

    @classmethod
    async def execute_update(cls, sql, params=None):
        pool = await cls.get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                return await cursor.execute(sql, params or ())
