#!/usr/bin/env python3
"""Offline planning report. No network, writes, schedules, or transaction authority."""
import argparse
from datetime import datetime
from decimal import Decimal, InvalidOperation
import json
import sys

PUBLIC_FIELDS = {'title': 'text', 'dates': 'text', 'itinerary': 'list'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def money(value, field):
    require(isinstance(value, (str, int)) and not isinstance(value, bool), field + ': use a decimal string or integer')
    try:
        result = Decimal(value)
    except InvalidOperation:
        raise ValueError(field + ': invalid decimal') from None
    require(result.is_finite() and result >= 0, field + ': must be finite and nonnegative')
    require(result.as_tuple().exponent >= -2, field + ': at most two decimal places supported')
    return result

def fmt(value):
    return format(value, '.2f')

def unique(items, field):
    require(isinstance(items, list), field + ': expected list')
    seen = set()
    for item in items:
        require(isinstance(item, dict), field + ': expected objects')
        ident = item.get('id')
        require(isinstance(ident, str) and ident.strip(), field + ': missing id')
        require(ident not in seen, field + ': duplicate id ' + ident)
        seen.add(ident)
    return items

def base(record):
    require(isinstance(record, dict), 'expected JSON object')
    require(type(record.get('schema_version')) is int and record['schema_version'] == 1, 'schema_version must be 1')
    require(isinstance(record.get('id'), str) and record['id'].strip(), 'id required')
    require(isinstance(record.get('title'), str) and record['title'].strip(), 'title required')
    require(isinstance(record.get('timezone'), str) and record['timezone'].strip(), 'IANA timezone required')
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
    try:
        ZoneInfo(record['timezone'])
    except (ZoneInfoNotFoundError, ValueError):
        raise ValueError('invalid or unavailable IANA timezone') from None

def budget(record):
    currency = record.get('currency')
    require(isinstance(currency, str) and len(currency) == 3 and currency.isascii() and currency.isalpha() and currency.isupper(), 'currency: uppercase three-letter code required')
    return money(record.get('budget'), 'budget')

def projection(record):
    base(record)
    public = record.get('public_summary', {})
    approved = record.get('approved_public_fields', [])
    require(isinstance(public, dict) and isinstance(approved, list), 'invalid public projection')
    require(all(isinstance(k, str) for k in approved), 'approval names must be strings')
    require(len(set(approved)) == len(approved), 'duplicate approval names')
    require(set(public) <= set(PUBLIC_FIELDS), 'unknown public field; do not copy private records')
    require(set(approved) <= set(public), 'approval references missing public field')
    for key, value in public.items():
        kind = PUBLIC_FIELDS[key]
        require((kind == 'text' and isinstance(value, str)) or (kind == 'list' and isinstance(value, list) and all(isinstance(v, str) for v in value)), 'invalid public field type: ' + key)
    # Structural allowlist, not semantic redaction, authentication, or consent proof.
    return {k: public[k] for k in sorted(approved)}

def instant(value):
    require(isinstance(value, str), 'timezone-aware ISO timestamp required')
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        raise ValueError('invalid ISO timestamp') from None
    require(dt.tzinfo is not None and dt.utcoffset() is not None, 'timestamp needs explicit UTC offset')
    return dt

def interval(obj):
    start, end = instant(obj.get('start')), instant(obj.get('end'))
    require(end > start, 'interval end must be after start')
    return start, end

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', help='one private JSON record; never embed data in shell commands')
    parser.add_argument('--share', action='store_true', help='print approved public projection only; human review still required')
    args = parser.parse_args()
    try:
        with open(args.record, encoding='utf-8') as stream:
            record = json.load(stream)
        output = projection(record) if args.share else plan(record)
        print(json.dumps(output, indent=2, ensure_ascii=False))
    except (ValueError, TypeError, KeyError, OSError) as exc:
        # Do not echo private values or file paths on failure.
        print('Invalid record or unreadable input. Check reference/data-contract.md. No changes made.', file=sys.stderr)
        return 2
    return 0

def plan(record):
    base(record)
    ceiling = budget(record)
    total = Decimal(0)
    unknown = []
    for cost in unique(record.get('costs'), 'costs'):
        require(cost.get('currency') == record['currency'], 'mixed currencies are unsupported')
        require(cost.get('unit') in ('party', 'per_person', 'per_night'), 'invalid cost unit')
        quantity = cost.get('quantity')
        require(type(quantity) is int and quantity > 0, 'quantity: positive integer required')
        require(cost['unit'] != 'party' or quantity == 1, 'party total quantity must be one')
        if cost.get('amount') is None:
            unknown.append(cost['id'])
        else:
            total += money(cost['amount'], 'amount') * quantity
    constraints = unique(record.get('constraints'), 'constraints')
    for c in constraints:
        require(type(c.get('hard')) is bool, 'hard must be boolean')
        require(c.get('status') in ('unknown', 'unverified', 'verified', 'failed'), 'invalid constraint status')
        if c['status'] == 'verified':
            require(isinstance(c.get('evidence'), str) and c['evidence'].strip(), 'verified constraint requires evidence reference')
    blockers = [c['id'] for c in constraints if c['hard'] and c['status'] != 'verified']
    return {'edition': 'planning-only', 'currency': record['currency'], 'known_party_cost': fmt(total), 'unknown_cost_ids': unknown, 'budget_complete': not unknown, 'headroom_against_known_costs': fmt(ceiling-total), 'over_budget_on_known_costs': total > ceiling, 'unresolved_hard_constraint_ids': blockers, 'readiness': 'blocked' if blockers else 'human-source-review-required', 'bookings_made': False, 'live_monitoring_enabled': False}

if __name__ == '__main__':
    sys.exit(main())
