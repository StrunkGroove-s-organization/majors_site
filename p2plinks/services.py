from django.core.cache import caches


def p2plinks_3(validated_data):
    def get_data():
        trade_type = validated_data['trade_type']
        trade_type = trade_type.split('_')[1]
        token = validated_data['crypto']

        key = f'{trade_type}--{token}--{3}'

        cache = caches['p2p_server']
        values = cache.get(key)
        try:
            values.sort(key=lambda item: item['spread'], reverse=True)
        except:
            values = False
        return values

    data = get_data()
    if not data:
        return 'Error'

    return data

def p2plinks_2(validated_data):
    def get_data():
        trade_type = validated_data['trade_type']
        trade_type = trade_type.split('_')[1]
        token = validated_data['crypto']

        key = f'{trade_type}--{token}--{2}'

        cache = caches['p2p_server']
        values = cache.get(key)
        try:
            values.sort(key=lambda item: item['spread'], reverse=True)
        except:
            values = False
        return values

    def filter_required(data, available, item):
        ad = data[index]
        first_item = ad['1'][item]
        second_item = ad['2'][item]
        if first_item not in available or second_item not in available:
            data.pop(index)

    def filter_required_ex(data, available, item):
        ex = {
            'Bybit': 'exchange_bybit',
            'huobi': 'exchange_huobi',
            'Garantex': 'exchange_garantex',
            'Bitpapa': 'exchange_bitpapa',
            'Beribit': 'exchange_beribit',
            'Hodl Hodl': 'exchange_hodlhodl',
            'mexc': 'exchange_mexc',
            'kucoin': 'exchange_kucoin',
            'Gate.io': 'exchange_gateio',
            'TotalCoin': 'exchange_totalcoin',
        }
        ad = data[index]
        first_item = ex[ad['1'][item]]
        second_item = ex[ad['2'][item]]
        if first_item not in available or second_item not in available:
            data.pop(index)

    def filter_spread(data, spread_max):
        spread = data[index]['spread']
        if spread >= spread_max:
            data.pop(index)

    def first_filter_lim(data, lim):
        ad = data[index]
        first_lim_min = ad['1']['lim_min']
        first_lim_max = ad['1']['lim_max']
        if first_lim_min >= lim or lim >= first_lim_max:
            data.pop(index)

    def second_filter_lim(data, lim):
        ad = data[index]
        second_lim_min = ad['2']['lim_min']
        second_lim_max = ad['2']['lim_max']
        if second_lim_min >= lim or lim >= second_lim_max:
            data.pop(index)

    def filter_ord_q(data, ord_q):
        ad = data[index]
        first_order_q = ad['1']['order_q']
        second_order_q = ad['2']['order_q']
        if ord_q >= first_order_q or ord_q >= second_order_q:
            data.pop(index)

    def filter_ord_p(data, ord_p):
        ad = data[index]
        first_order_p = ad['1']['order_p']
        second_order_p = ad['2']['order_p']
        if ord_p >= first_order_p or ord_p >= second_order_p:
            data.pop(index)

    def filter_first_available(data, available):
        ad = data[index]
        first_available = ad['1']['available']
        second_available = ad['2']['available']
        if available <= first_available or available <= second_available:
            data.pop(index)

    def filter_second_available(data, available):
        ad = data[index]
        first_available = ad['1']['available']
        second_available = ad['2']['available']
        if available <= first_available or available <= second_available:
            data.pop(index)

    data = get_data()
    if not data:
        return 'Error'

    payment_methods = validated_data['payment_methods']
    for index in range(len(data.copy()) - 1, -1, -1):
        filter_required(data, payment_methods, 'best_payment')

    exchanges = validated_data['exchanges']
    for index in range(len(data.copy()) - 1, -1, -1):
        filter_required_ex(data, exchanges, 'exchange')

    spread_max = validated_data.get('spread_max', False)
    if spread_max:
        for index in range(len(data.copy()) - 1, -1, -1):
            filter_spread(data, spread_max)

    lim_first = validated_data.get('lim_first', False)
    if lim_first:
        for index in range(len(data.copy()) - 1, -1, -1):
            first_filter_lim(data, lim_first)

    lim_second = validated_data.get('lim_second', False)
    if lim_second:
        for index in range(len(data.copy()) - 1, -1, -1):
            second_filter_lim(data, lim_second)

    ord_q = validated_data.get('ord_q', False)
    if ord_q:
        for index in range(len(data.copy()) - 1, -1, -1):
            filter_ord_q(data, ord_q)

    ord_p = validated_data.get('ord_p', False)
    if ord_p:
        for index in range(len(data.copy()) - 1, -1, -1):
            filter_ord_p(data, ord_p)

    first_available = validated_data.get('available_first', False)
    if ord_p:
        for index in range(len(data.copy()) - 1, -1, -1):
            filter_first_available(data, first_available)

    second_available = validated_data.get('available_second', False)
    if ord_p:
        for index in range(len(data.copy()) - 1, -1, -1):
            filter_second_available(data, second_available)

    return data