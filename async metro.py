import aiohttp
import asyncio
import pandas as pd
import json
from bs4 import BeautifulSoup


template_url = 'https://online.metro-cc.ru'


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def parse_product_brand(session, url):
    html = await fetch(session, url)
    soup = BeautifulSoup(html, 'html.parser')
    brand = soup.find('meta', {'itemprop': 'brand'}).get('content')
    return brand


async def parse_metro_block(session, product_block):
    product_id = product_block.get('id')
    name = product_block.find('a', {'class': 'product-card-name'}).get('title')
    url = product_block.find('a', {'class': 'product-card-photo__link'}).get('href')
    discount = product_block.find('div', {'class': 'product-card-photo__discount'})
    
    if discount:
        prices_blocks = product_block.find_all('span', {'class': 'product-price__sum-rubles'})
        regular_price = float(prices_blocks[1].text.replace('\xa0', '.'))
        promo_price = float(prices_blocks[0].text.replace('\xa0', '.'))
    else:
        prices_blocks = product_block.find_all('span', {'class': 'product-price__sum-rubles'})
        regular_price = float(prices_blocks[0].text.replace('\xa0', '.'))
        promo_price = None

    brand = await parse_product_brand(session, f'{template_url}{url}')

    return {
        'id': product_id,
        'name': name,
        'url': url,
        'regular_price': regular_price,
        'promo_price': promo_price if promo_price is not None else '',
        'brand': brand
    }


async def parse_metro():
    products_data = list()
    
    async with aiohttp.ClientSession() as session:
        for i in range(1, 6):
            print("Записывается информация со страницы:", i)
            url = f'{template_url}/category/molochnye-prodkuty-syry-i-yayca/syry/?page={i}'
            html = await fetch(session, url)
            soup = BeautifulSoup(html, 'html.parser')
            product_blocks = soup.find_all('div', class_='catalog-2-level-product-card')
            data = [parse_metro_block(session, product_block) for product_block in product_blocks]
            products_data.extend(await asyncio.gather(*data))

    df = pd.DataFrame(products_data)
    df.to_csv('products.csv', index=False, encoding='utf-8', sep=';')
    
    with open('products.json', mode='w', encoding='utf-8') as json_file:
        json.dump(products_data, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    asyncio.run(parse_metro())