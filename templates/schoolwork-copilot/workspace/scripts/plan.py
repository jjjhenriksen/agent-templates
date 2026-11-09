#!/usr/bin/env python3
"""Read-only deadline ordering for assignment aliases; not an LMS integration."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

def plan(record):
    if type(record.get('schema_version')) is not int or record['schema_version'] != 1:
        raise ValueError('schema')
    rows = record['assignments']
    if not isinstance(rows, list):
        raise ValueError('assignments')
    seen, known, unknown = set(), [], []
    for row in rows:
        key, status, due = row['id'], row['status'], row['due_at']
        if not isinstance(key, str) or not key.strip() or key in seen:
            raise ValueError('id')
        seen.add(key)
        if status not in ('not-started', 'draft', 'submitted', 'graded'):
            raise ValueError('status')
        instant = None
        if due is not None:
            if not isinstance(due, str):
                raise ValueError('deadline')
            instant = datetime.fromisoformat(due.replace('Z', '+00:00'))
            if instant.utcoffset() is None:
                raise ValueError('timezone')
            instant = instant.astimezone(timezone.utc)
        if status in ('submitted', 'graded'):
            continue
        if instant is None:
            unknown.append(key)
        else:
            known.append((instant, key))
    return {'edition': 'planning-only', 'deadline_order': [key for _, key in sorted(known)],
            'unknown_deadline_ids': sorted(unknown), 'submissions_made': False,
            'live_monitoring_enabled': False}

if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise ValueError('arguments')
        result = plan(json.loads(Path(sys.argv[1]).read_text()))
        print(json.dumps(result, indent=2))
    except (ValueError, TypeError, KeyError, AttributeError, OSError, OverflowError):
        print('Invalid assignment input.', file=sys.stderr)
        sys.exit(2)
