import re
from collections import defaultdict


# For poe.ninja
def get_name_by_regex(regex, string, stop_symbol, list):
    for find_info in re.finditer(regex, string):
        name = []
        end_index = find_info.regs[0][1]
        while string[end_index] != stop_symbol:
            name.append(string[end_index])
            end_index += 1
        list.append(''.join(name))
    return list


# For poe.ninja
def get_price_by_regex(regex, string, stop_symbol, list):
    for find_info in re.finditer(regex, string):
        price = []
        start_index = find_info.regs[0][0] - 1
        while string[start_index] != stop_symbol:
            price.append(string[start_index])
            start_index -= 1
        price.reverse()
        list.append(float(''.join(price)))
    return list


# Filter items by price and saving as dictionary
def filter_by_price(names, prices, price_filters):
    print('{} == {}'.format(len(names), len(prices)))
    assert len(names) == len(prices)

    dictionary = {}
    for i in range(len(names)):
        dictionary[names[i]] = prices[i]

    max_price = price_filters[0]
    min_price = price_filters[1]

    filter_divs = defaultdict(int)
    for name, price in dictionary.items():
        if max_price > price > min_price:
            if filter_divs[name] > 0:
                old_price = filter_divs[name]
                if old_price > price:
                    filter_divs[name] = old_price
            else:
                filter_divs[name] = price

    return filter_divs


# For poe.ninja
def divination_format_html(filename, price_filters):
    with open(filename) as file:
        data = file.read()
    names = get_name_by_regex('<img src="[^"]+".><.span>',
                              data,
                              '<',
                              [])
    prices = get_price_by_regex(' x <img src="[^"]+".title="Chaos Orb"',
                                data,
                                '>',
                                [])

    return filter_by_price(names=names,
                           prices=prices,
                           price_filters=price_filters)


# For poe.ninja
def weapons_format_html(filename, price_filters):
    with open(filename) as file:
        data = file.read()
    names = get_name_by_regex('<img src="[^"]+".><.span>(<span>|<span class="relic-text">)',
                              data,
                              '<',
                              [])
    prices = get_price_by_regex(' x <img src="[^"]+".title="Chaos Orb"',
                                data,
                                '>',
                                [])

    return filter_by_price(names=names,
                           prices=prices,
                           price_filters=price_filters)


# For poe.ninja
def armors_format_html(filename, price_filters):
    with open(filename) as file:
        data = file.read()
    names = get_name_by_regex('<img src="[^"]+".><.span>(<span>|<span class="relic-text">)',
                              data,
                              '<',
                              [])
    prices = get_price_by_regex(' x <img src="[^"]+".title="Chaos Orb"',
                                data,
                                '>',
                                [])

    return filter_by_price(names=names,
                           prices=prices,
                           price_filters=price_filters)


# For poe.ninja
def flasks_format_html(filename, price_filters):
    with open(filename) as file:
        data = file.read()
    names = get_name_by_regex('<img src="[^"]+".><.span>(<span>|<span class="relic-text">)',
                              data,
                              '<',
                              [])
    prices = get_price_by_regex(' x <img src="[^"]+".title="Chaos Orb"',
                                data,
                                '>',
                                [])

    return filter_by_price(names=names,
                           prices=prices,
                           price_filters=price_filters)


# For poe.ninja
def accessories_format_html(filename, price_filters):
    with open(filename) as file:
        data = file.read()
    names = get_name_by_regex('<img src="[^"]+".><.span>(<span>|<span class="relic-text">)',
                              data,
                              '<',
                              [])
    prices = get_price_by_regex(' x <img src="[^"]+".title="Chaos Orb"',
                                data,
                                '>',
                                [])

    return filter_by_price(names=names,
                           prices=prices,
                           price_filters=price_filters)


# For poe.ninja
def jewels_format_html(filename, price_filters):
    with open(filename) as file:
        data = file.read()
    names = get_name_by_regex('<img src="[^"]+".><.span>(|<span class="relic-text">)',
                              data,
                              '<',
                              [])
    prices = get_price_by_regex(' x <img src="[^"]+".title="Chaos Orb"',
                                data,
                                '>',
                                [])

    return filter_by_price(names=names,
                           prices=prices,
                           price_filters=price_filters)


# For poe.ninja
def maps_format_html(filename, price_filters):
    with open(filename) as file:
        data = file.read()
    names = get_name_by_regex('<img src="[^"]+".><.span><span>',
                              data,
                              '<',
                              [])
    prices = get_price_by_regex(' x <img src="[^"]+".title="Chaos Orb"',
                                data,
                                '>',
                                [])

    return filter_by_price(names=names,
                           prices=prices,
                           price_filters=price_filters)
