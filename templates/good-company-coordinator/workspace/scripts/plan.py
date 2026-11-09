#!/usr/bin/env python3
"""Offline planning report. No network, writes, schedules, or transaction authority."""
import argparse
from datetime import datetime
from decimal import Decimal, InvalidOperation
import json
import sys

PUBLIC_FIELDS = {'title': 'text', 'event': 'text', 'accepted_assignments': 'list'}

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

def level(value):
    require(type(value) is int and 0 <= value <= 3, 'skill level must be integer 0..3')
    return value

def string_list(value):
    require(isinstance(value, list) and all(isinstance(x, str) for x in value), 'string list required')
    return value

def plan(record):
    base(record)
    people = unique(record.get('people'), 'people')
    tasks = unique(record.get('tasks'), 'tasks')
    unique(record.get('sources'), 'sources')
    counts, busy = {}, {}
    for p in people:
        require(type(p.get('opt_in')) is bool, 'opt_in must be boolean')
        string_list(p.get('roles'))
        string_list(p.get('avoid_categories'))
        require(isinstance(p.get('skills'), dict), 'skills mapping required')
        for rating in p['skills'].values():
            level(rating)
        require(type(p.get('max_open_tasks')) is int and p['max_open_tasks'] >= 0, 'invalid task limit')
        require(type(p.get('open_tasks')) is int and p['open_tasks'] >= 0, 'invalid workload')
        require(isinstance(p.get('availability'), list) and isinstance(p.get('busy', []), list), 'availability/busy lists required')
        for w in p['availability']:
            interval(w)
        busy[p['id']] = [interval(w) for w in p.get('busy', [])]
        counts[p['id']] = p['open_tasks']
    output = []
    for task in tasks:
        start, end = interval(task)
        require(task.get('status') == 'proposed', 'helper accepts only unassigned proposed tasks')
        require(isinstance(task.get('category'), str), 'task category required')
        roles = string_list(task.get('required_roles'))
        require(isinstance(task.get('required_skills'), dict), 'required skills mapping required')
        for rating in task['required_skills'].values():
            level(rating)
        candidates = []
        for person in people:
            pid = person['id']
            if not person['opt_in'] or counts[pid] >= person['max_open_tasks']:
                continue
            if task['category'] in person['avoid_categories'] or not set(roles) <= set(person['roles']):
                continue
            if any(k not in person['skills'] or person['skills'][k] < v for k, v in task['required_skills'].items()):
                continue
            if not any(a <= start and end <= b for a,b in map(interval, person['availability'])):
                continue
            if any(start < b and a < end for a,b in busy[pid]):
                continue
            candidates.append(pid)
        candidates.sort(key=lambda pid: (counts[pid], pid))
        chosen = candidates[0] if candidates else None
        if chosen:
            counts[chosen] += 1
            busy[chosen].append((start, end))
        output.append({'task_id': task['id'], 'candidate_ids': candidates, 'suggested_person_id': chosen, 'status': 'proposed' if chosen else 'unresolved'})
    return {'edition': 'planning-only', 'proposals': output, 'assignments_accepted': False, 'messages_sent': False, 'note': 'Greedy screening of supplied facts only; not qualification, consent or source verification. No state written.'}

if __name__ == '__main__':
    sys.exit(main())
