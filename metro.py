import requests
import pandas as pd
import json
from bs4 import BeautifulSoup
from time import sleep


template_url = 'https://online.metro-cc.ru'


def parse_product_brand(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        brand = soup.find('meta', {'itemprop': 'brand'}).get('content')
        sleep(2)
        return brand
    return ''
        

def parse_metro_block(product_block):
    product_id = product_block.get('id')
    name = product_block.find('a', {'class': 'product-card-name reset-link catalog-2-level-product-card__name style--catalog-2-level-product-card'}).get('title')
    url = product_block.find('a', {'class': 'product-card-photo__link reset-link'}).get('href')
    discount = product_block.find('div', {'class': 'product-card-photo__discount'})
    if discount:
        prices_blocks = product_block.find_all('span', {'class': 'product-price__sum-rubles'})
        regular_price = float(prices_blocks[0].text.replace('\xa0', '.'))
        promo_price = float(prices_blocks[1].text.replace('\xa0', '.'))
    else:
        prices_blocks = product_block.find_all('span', {'class': 'product-price__sum-rubles'})
        regular_price = float(prices_blocks[0].text.replace('\xa0', '.'))
        promo_price = None

    brand = parse_product_brand(f'{template_url}{url}')

    return {
        'id': product_id,
        'name': name,
        'url': f'{template_url}{url}',
        'regular_price': regular_price,
        'promo_price': promo_price if promo_price is not None else '',
        'brand': brand
    }


def parse_metro():
    products_data = list()
    
    for i in range(1, 6):
        print("Записывается инорфмация со страницы:", i)
        url=f'{template_url}/category/molochnye-prodkuty-syry-i-yayca/syry/?page={i}'
        response = requests.get(url)
        if response.status_code == 200:
            
            soup = BeautifulSoup(response.text, 'html.parser')
            product_blocks = soup.find_all('div', class_='catalog-2-level-product-card product-card subcategory-or-type__products-item with-prices-drop')
            for product_block in product_blocks:
                products_data.append(parse_metro_block(product_block))

            df = pd.DataFrame(products_data)
            df.to_csv('products.csv', index=False, encoding='utf-8', sep=';')
                
            with open('products.json', mode='w', encoding='utf-8') as json_file:
                json.dump(products_data, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    parse_metro()