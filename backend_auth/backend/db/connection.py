import asyncpg

class connection:
    __connection = None

    @classmethod
    async def make_connection(cls):
        if cls.__connection is None:
            print("Creating new DB connection")
            cls.__connection = await asyncpg.create_pool(
                min_size=1,
                max_size=10,
                database='prac_gpt',
                user='postgres',
                host='localhost',
                password='anas123',
                port=5432
            )
        else:
            print("Using existing DB connection")
        return cls.__connection

async def get_db_connection():
    return await connection.make_connection()
