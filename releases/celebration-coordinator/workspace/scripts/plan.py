#!/usr/bin/env python3
"""Offline planning report. No network, writes, schedules, or transaction authority."""
import argparse
from datetime import datetime
from decimal import Decimal, InvalidOperation
import json
import sys

PUBLIC_FIELDS = {'title': 'text', 'date': 'text', 'location': 'text', 'contributions': 'list'}

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
    actual = Decimal(0)
    unpaid = Decimal(0)
    estimates = Decimal(0)
    unknown = []
    for cost in unique(record.get('costs'), 'costs'):
        require(cost.get('currency') == record['currency'], 'mixed currencies are unsupported')
        paid = money(cost.get('actual'), 'actual')
        committed = cost.get('committed')
        estimate = cost.get('estimate')
        actual += paid
        if committed is not None:
            total = money(committed, 'committed')
            require(total >= paid, 'committed total cannot be below paid actual')
            unpaid += total - paid
        else:
            require(paid == 0, 'paid costs require committed total')
            if estimate is None:
                unknown.append(cost['id'])
            else:
                estimates += money(estimate, 'estimate')
    tasks = unique(record.get('tasks'), 'tasks')
    ids = {t['id'] for t in tasks}
    graph = {}
    for task in tasks:
        deps = task.get('dependencies', [])
        require(isinstance(deps, list) and all(isinstance(d, str) for d in deps), 'dependencies: list of IDs required')
        require(set(deps) <= ids and task['id'] not in deps, 'unknown/self dependency')
        require(type(task.get('accepted')) is bool, 'accepted must be boolean')
        require(not task['accepted'] or bool(task.get('owner')), 'accepted task needs owner')
        require(task.get('status') in ('proposed', 'accepted', 'completed', 'cancelled'), 'invalid task status')
        require(task['status'] not in ('accepted', 'completed') or task['accepted'], 'status requires explicit acceptance')
        if task.get('due') is not None:
            instant(task['due'])
        graph[task['id']] = deps
    visiting, done = set(), set()
    def visit(node):
        require(node not in visiting, 'dependency cycle')
        if node in done:
            return
        visiting.add(node)
        for child in graph[node]:
            visit(child)
        visiting.remove(node)
        done.add(node)
    for node in graph:
        visit(node)
    total = actual + unpaid + estimates
    return {'edition': 'planning-only', 'currency': record['currency'], 'actual_paid': fmt(actual), 'unpaid_commitments': fmt(unpaid), 'uncommitted_estimates': fmt(estimates), 'known_forecast': fmt(total), 'unknown_cost_ids': unknown, 'forecast_complete': not unknown, 'headroom_against_known_costs': fmt(ceiling-total), 'over_budget_on_known_costs': total > ceiling, 'unaccepted_task_ids': [t['id'] for t in tasks if not t['accepted'] and t['status'] != 'cancelled'], 'reminders_created': False}

if __name__ == '__main__':
    sys.exit(main())
