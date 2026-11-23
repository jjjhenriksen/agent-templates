#!/usr/bin/env python3
"""Offline/read-only whole-plan shopping arithmetic; no conversions or provider calls."""
import argparse
from decimal import Decimal, InvalidOperation
import json
import sys

def amount(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 64:
        raise ValueError('decimal string required')
    try:
        n = Decimal(value)
    except InvalidOperation:
        raise ValueError('invalid decimal') from None
    if not n.is_finite() or n < 0 or n > Decimal('1000000000') or n.as_tuple().exponent < -6:
        raise ValueError('quantity outside supported range')
    return n

def key(row):
    if not isinstance(row, dict):
        raise ValueError('row object required')
    values = (row.get('id'), row.get('unit'))
    if any(not isinstance(x, str) or not x.strip() or x != x.strip() or len(x) > 128 for x in values):
        raise ValueError('canonical ingredient id and unit required')
    return values

def shopping(record):
    if not isinstance(record, dict) or not isinstance(record.get('ingredients'), list) or not isinstance(record.get('pantry'), list):
        raise ValueError('ingredients and pantry lists required')
    if len(record['ingredients']) > 10000 or len(record['pantry']) > 10000:
        raise ValueError('too many rows')
    stock = {}
    for row in record['pantry']:
        k = key(row)
        if k in stock:
            raise ValueError('duplicate pantry key')
        available = amount(row.get('available'))
        reserved = amount(row.get('reserved', '0'))
        if reserved > available:
            raise ValueError('reservation exceeds stock')
        stock[k] = available - reserved
    groups = {}
    for row in record['ingredients']:
        k = key(row)
        if 'need' not in row:
            raise ValueError('need required; null means unknown')
        g = groups.setdefault(k, {'need': Decimal(0), 'unknown': False})
        if row['need'] is None:
            g['unknown'] = True
        else:
            g['need'] += amount(row['need'])
    result = []
    for (ingredient, unit), g in sorted(groups.items()):
        usable = stock.get((ingredient, unit), Decimal(0))
        lower = max(Decimal(0), g['need'] - usable)
        result.append({'id': ingredient, 'unit': unit, 'known_need': str(g['need']),
                       'usable_pantry': str(usable), 'buy': None if g['unknown'] else str(lower),
                       'buy_lower_bound': str(lower), 'complete': not g['unknown']})
    return {'edition': 'offline-shopping-only', 'complete': all(x['complete'] for x in result), 'items': result}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('record')
    args = p.parse_args()
    try:
        with open(args.record, encoding='utf-8') as f:
            record = json.load(f)
        result = shopping(record)
    except (OSError, ValueError, TypeError, KeyError, InvalidOperation):
        print('Invalid shopping record; check the documented input contract.', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
