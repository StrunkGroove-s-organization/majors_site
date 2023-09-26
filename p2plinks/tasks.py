import requests

from django.db import connections
from django.core.cache import cache
from myproject.celery import app

from psycopg2.extensions import AsIs

TIME_CACHE = 200
BUY_SELL = [
    'BUY',
    'SELL',
]
CRYPTO = [
    'USDT',
    'BTC',
    'ETH',
    'BUSD',
    'BNB',
    'DOGE',
    'TRX',
    'USDD',
    'USDC',
    'RUB',
    'HT',
    'EOS',
    'XRP',
    'LTC',
    'GMT',
    'TON',
    'XMR',
    'DAI',
    'TUSD',
]

@app.task
def main():
    def get_data_db(buy_sell):
        def get_query(ex, buy_sell, pay):
            sort_direction = "ASC" if buy_sell == "BUY" else "DESC"
            query = f"""
                (
                    SELECT
                        name, order_q, order_p, price, 
                        lim_min, lim_max, fiat, token, 
                        buy_sell, exchange, adv_no, 
                        '{pay}' as best_payment, available
                    FROM public.{AsIs(ex)}
                    WHERE price = (
                        SELECT {'MIN' if sort_direction == 'ASC' else 'MAX'}(price)
                        FROM public.{AsIs(ex)}
                        WHERE 
                        token = %s
                        AND buy_sell = %s
                        AND '{pay}' IN (SELECT value::text FROM jsonb_array_elements_text(payments))
                    )
                    LIMIT 1
                )
            """
            return query

        info = [
            {
                'exchange_name': 'exchange_huobi',
                'crypto': [
                    'BTC', 'USDT', 'ETH', 'USDD', 'HT', 'TRX', 'EOS', 'XRP', 'LTC',
                ],
                'pay': [
                    'Tinkoff', 'Sber', 'MTS-Bank', 'Raiffeisenbank', 'ЮMmoney'
                ],
            },
            {
                'exchange_name': 'exchange_mexc',
                'crypto': [
                    'USDT', 'BTC', 'ETH', 'USDC',
                ],
                'pay': [
                    'Sber', 'Tinkoff',
                ],
            },
            {
                'exchange_name': 'exchange_gateio',
                'crypto': [
                    'USDT', 'BTC', 'ETH', 'DOGE',
                ],
                'pay': [
                    'Raiffeisenbank', 'QIWI',
                ],
            },
            {
                'exchange_name': 'exchange_hodlhodl',
                'crypto': [
                    'Tinkoff', 'Sber',
                ],
                'pay': [
                    'Tinkoff', 'Sber',
                ],
            },
            {
                'exchange_name': 'exchange_bybit',
                'crypto': [
                    'USDT', 'BTC', 'ETH', 'USDC',
                ],
                'pay': [
                    'Tinkoff', 'Sber', 'MTS-Bank', 'Raiffeisenbank', 'ЮMmoney'
                ],
            },
            {
                'exchange_name': 'exchange_kucoin',
                'crypto': [
                    'USDT', 'BTC', 'ETH', 'USDC',
                ],
                'pay': [
                    'SBP',
                ],
            },
            {
                'exchange_name': 'exchange_garantex',
                'crypto': [
                    'USDT', 'BTC', 'ETH', 'USDC', 'DAI',
                ],
                'pay': [
                    'SBP',
                ],
            },
            {
                'exchange_name': 'exchange_beribit',
                'crypto': [
                    'USDT',
                ],
                'pay': [
                    'Tinkoff', 'Sber',
                ],
            },
            {
                'exchange_name': 'exchange_totalcoin',
                'crypto': [
                    'USDT', 'BTC', 'ETH', 'LTC',
                ],
                'pay': [
                    'Tinkoff', 'Sber', 'ЮMmoney', 'MTS-Bank', 'Raiffeisenbank',
                ],
            },
            {
                'exchange_name': 'exchange_bitpapa',
                'crypto': [
                    'BTC', 'USDT', 'ETH', 'USDC',
                ],
                'pay': [
                    'Tinkoff', 'Sber', 'ЮMmoney', 'MTS-Bank', 'Raiffeisenbank',
                ],
            },
        ]

        params = []
        union_queries = []

        for i in info:
            ex = i['exchange_name']
            crypto = i['crypto']
            payments = i['pay']

            for currency in crypto:
                for pay in payments:
                    query = get_query(ex, buy_sell, pay)
                    params.extend([currency, buy_sell])
                    union_queries.append(query)

        full_query = " UNION ".join(union_queries)

        with connections['parsing_db'].cursor() as cursor:
            cursor.execute(full_query, params)
            result = cursor.fetchall()

        return result

    def group_data(data, crypto_data):
        for ad in data:
            currency = ad[7]
            if currency in crypto_data:
                if ad not in crypto_data[currency]:
                    crypto_data[currency].append(ad)

    def count_2_actions(crypto_data_f, crypto_data_s, trade_type):
        num = 0
        for currency in CRYPTO:
            data_f = crypto_data_f[currency]
            data_s = crypto_data_s[currency]

            items = []
            for ad_f in data_f:
                price_f = ad_f[3]

                for ad_s in data_s:
                    price_s = ad_s[3]

                    spread = round(((price_s / price_f) - 1) * 100, 2)
                    if 0.01 < spread:
                        num += 1
                        item = {
                            'spread': spread,
                            '1': ad_f,
                            '2': ad_s,
                        }
                        items.append(item)

            if len(items) != 0:
                key = f'{trade_type}--{currency}'
                # print(f'{key}--{items}')
                cache.set(key, items, TIME_CACHE)
        return num

    def count_3_actions(crypto_data_f, crypto_data_s, trade_type):
        def get_key(fiat):
            if fiat == 'BTC':
                return 'BTCUSDT'
            elif fiat == 'GMT':
                return 'GMTUSDT'
            elif fiat == 'XMR':
                return 'XMRUSDT'
            elif fiat == 'DOGE':
                return 'DOGEUSDT'
            elif fiat == 'TRX':
                return 'TRXUSDT'
            elif fiat == 'EOS':
                return 'EOSUSDT'
            elif fiat == 'XRP':
                return 'XRPUSDT'
            elif fiat == 'LTC':
                return 'LTCUSDT'
            elif fiat == 'BUSD':
                return 'BUSDUSDT'
            elif fiat == 'BNB':
                return 'BNBUSDT'
            elif fiat == 'ETH':
                return 'ETHUSDT'
            elif fiat == 'RUB':
                return 'USDTRUB'
            elif fiat == 'SHIB':
                return 'SHIBUSDT'
            elif fiat == 'USDC':  
                return 'USDCUSDT' 
            elif fiat == 'TON':
                return 'TON_USDT'
            elif fiat == 'HT':
                return 'HT_USDT'
            else:
                return fiat

        def get_price_by_symbol(crypto_list, target_crypto):
            for crypto_obj in crypto_list:
                if crypto_obj == target_crypto:
                    return float(crypto_list[target_crypto])
            return None

        def calculate_spread(price_s, price_f, spot_price):
            spread = ((price_s / (price_f * spot_price)) - 1) * 100
            spread_r = round(spread, 2)
            return spread_r
        
        num = 0
        items = []
        for ad_f in crypto_data_f:
            price_f = ad_f[3]
            token_f = ad_f[7]
            
            for ad_s in crypto_data_s:
                price_s = ad_s[3]
                token_s = ad_s[7]
                
                if token_f == 'USDT' and token_s != 'USDT':
                    key = get_key(token_s)
                    spot_price = get_price_by_symbol(spot, key)
                    if spot_price == None: continue
                    spread = calculate_spread(price_s, price_f, spot_price)

                    if 0.01 < spread:
                        num += 1
                        item = {
                            'spread': spread,
                            'spot': spot_price,
                            '1': ad_f,
                            '2': ad_s,
                        }
                        items.append(item)

                elif token_f != 'USDT' and token_s == 'USDT':
                    key = get_key(token_f)
                    spot_price = get_price_by_symbol(spot, key)
                    if spot_price == None: continue
                    spot_price = 1 / spot_price
                    spread = calculate_spread(price_s, price_f, spot_price)

                    if 0.01 < spread:
                        num += 1
                        item = {
                            'spread': spread,
                            'spot': spot_price,
                            '1': ad_f,
                            '2': ad_s,
                        }
                        items.append(item)

        if len(items) != 0:
            key = f'{trade_type}'
            # print(f'{key}--{items}')
            cache.set(key, items, TIME_CACHE)

        return num

    def binance_spot():
        url = "https://api.binance.com/api/v3/ticker/price"
        response = requests.get(url)
        data = response.json()
        
        spot_prices = {}
        for token_info in data:
            symbol = token_info['symbol']
            price = token_info['price']
            spot_prices[symbol] = price
        return spot_prices

    crypto_data_buy = {currency: [] for currency in CRYPTO}
    crypto_data_sell = {currency: [] for currency in CRYPTO}

    data_buy = get_data_db('BUY')
    data_sell = get_data_db('SELL')

    group_data(data_buy, crypto_data_buy)
    group_data(data_sell, crypto_data_sell)

    num12 = count_2_actions(crypto_data_buy, crypto_data_buy, 'BUY-BUY')
    num22 = count_2_actions(crypto_data_buy, crypto_data_sell, 'BUY-SELL')
    num32 = count_2_actions(crypto_data_sell, crypto_data_buy, 'SELL-BUY')
    num42 = count_2_actions(crypto_data_sell, crypto_data_sell, 'SELL-SELL')

    spot = binance_spot()
    num13 = count_3_actions(data_buy, data_buy, 'BUY_BUY')
    num23 = count_3_actions(data_buy, data_sell, 'BUY_SELL')
    num33 = count_3_actions(data_sell, data_buy, 'SELL_BUY')
    num43 = count_3_actions(data_sell, data_sell, 'SELL_SELL')

    return num12, num22, num32, num42, num13, num23, num33, num43