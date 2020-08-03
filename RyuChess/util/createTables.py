users_info = '''
CREATE TABLE users_info (
    ID SERIAL NOT NULL,
    user_name VARCHAR(255) UNIQUE NOT NULL,
    user_pass VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) UNIQUE NOT NULL,
    user_country country_id NOT NULL,
    date_created TIMESTAMP WITH TIME ZONE DEFAULT (now() AT TIME ZONE 'UTC') NOT NULL,
    access_level NUMERIC(1) NOT NULL DEFAULT 9,
    PRIMARY KEY (ID),
);
'''

user_login_session = '''
CREATE TABLE user_login_session (
    ID SERIAL NOT NULL,
    user_id INTEGER NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    access_level NUMERIC(1) NOT NULL,
    token VARCHAR(255) NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (user_id) REFERENCES users_info(ID)
);
'''

Country = '''
CREATE TABLE country(
    ID INTEGER UNIQUE,
    name VARCHAR(255) NOT NULL,
    alpha2 VARCHAR(2) NOT NULL,
    alpha3 VARCHAR(3) NOT NULL,
    PRIMARY KEY(ID)
);
'''

async def addDatabaseTables(pool):
    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(track_work)


async def main(PG_CONFIG):
    pool = await asyncpg.create_pool(PG_CONFIG['dsn'])
    await addDatabaseTables(pool)

import asyncio
import asyncpg
from dotenv import load_dotenv
from os import getenv
from os.path import dirname, join, exists

import aiohttp
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

PG_CONFIG = {
    'user': getenv('DB_USER'),
    'pass': getenv('DB_PASS'),
    'host': getenv('DB_HOST'),
    'database': getenv('DB_NAME'),
    'port': getenv('DB_PORT')
}
PG_CONFIG['dsn'] = "postgres://%s:%s@%s:%s/%s" % (PG_CONFIG['user'], PG_CONFIG['pass'],
                                                PG_CONFIG['host'], PG_CONFIG['port'], PG_CONFIG['database'])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(PG_CONFIG))
