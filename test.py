from requests import get
import json

from pprint import pprint

ids = set()


def download():
    for i in range(1, 1000000000):
        response = get(f'https://goldapple.ru/web_scripts/discover/category/products?cat=59&page={i}').json()
        print(i)

        products = response.get('products', [])
        for pr in products:
            if pr.get('id') in ids:
                return

            result = {
                'price': pr.get('price'),
                'brand': pr.get('brand'),
                'category': pr.get('category_type'),
                'country': pr.get('country'),
                'sex': pr.get('gender'),
                'product_id': pr.get('id'),
                'images': pr.get('images'),
                'is_saleable': pr.get('is_saleable'),
                'product_name': pr.get('name'),
                'old_price': pr.get('old_price'),
                'url': pr.get('url'),
                'stores': []
            }
            ids.add(pr.get('id'))

            response = get(
                f'https://goldapple.ru/rest/V1/offlinestock/stock/product?fias_id=0c5b2444-70a0-4932-980c-b4dc0d3f02b5&product_id={pr.get("id")}').json()
            stores = response.get('stores', [])
            for store in stores:
                st = {
                    'address': store.get('name'),
                    'name': store.get('molls_name'),
                    'lat': store.get('latitude'),
                    'lon': store.get('longitude'),
                    'schedule': store.get('schedule'),
                    'metro': store.get('station'),
                    'stock_status': 'В наличии' if store.get('stock_status') == 1 else 'Нет в наличии' if store.get(
                        'stock_status') == 0 else 'Осталось менее {} штук'.format(store.get('min_qty_limit', 0))
                }
                result['stores'].append(st)

            with open('result.dat', 'a', encoding='utf-8') as f:
                f.write(json.dumps(result, ensure_ascii=False) + '\n')

            # return result


download()
