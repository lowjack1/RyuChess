from bs4 import BeautifulSoup
import requests
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


async def main(PG_CONFIG):
    url = 'https://www.nationsonline.org/oneworld/country_code_list.htm'
    res = requests.get(url)
    html_page = res.content

    soup = BeautifulSoup(html_page, 'html.parser')

    table = soup.find_all('table')[0]

    country_data = []

    for row in table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) != 5:
            continue
        country_record = []
        for i in range(1, len(cols)):
            country_record.append(cols[i].get_text().replace("\n", "").strip())
        
        country_record[-1] = int(country_record[-1])
        country_data.append(country_record)


    pool = await asyncpg.create_pool(PG_CONFIG['dsn'])
    async with pool.acquire() as connection:
        async with connection.transaction():
            q = "INSERT INTO country(name, alpha2, alpha3, ID) VALUES($1, $2, $3, $4)"
            await connection.executemany(q, country_data)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(PG_CONFIG))