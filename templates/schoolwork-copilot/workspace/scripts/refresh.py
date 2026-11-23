#!/usr/bin/env python3
"""Read authorized local exports; emit a brief and checkpoint. No writes or network."""
import argparse
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


def instant(value):
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.utcoffset() is None:
        raise ValueError('offset required')
    return dt.astimezone(timezone.utc)


def refresh(config, previous, now, root):
    zone = ZoneInfo(config['timezone'])
    hour, minute = map(int, config['brief_time'].split(':'))
    if not (0 <= hour < 24 and 0 <= minute < 60):
        raise ValueError('time')
    stale_hours = config['stale_hours']
    reminder_hours = config['reminder_hours']
    if type(stale_hours) is not int or stale_hours <= 0 or type(reminder_hours) is not int or reminder_hours < 0:
        raise ValueError('hours')
    if type(config['reminders']) is not bool:
        raise ValueError('reminders')
    state = json.loads(json.dumps(previous))
    state.setdefault('sources', {})
    state.setdefault('sent', [])
    coverage, changes, active = [], [], []
    ids = set()
    for source in config['sources']:
        sid = source['id']
        if not isinstance(sid, str) or not sid or sid in ids or source['authorized'] is not True:
            raise ValueError('source authorization/id')
        ids.add(sid)
        path = (root / source['path']).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError('source outside root')
        old = state['sources'].get(sid)
        try:
            raw = json.loads(path.read_text())
            observed = instant(raw['observed_at'])
            if observed > now or (old and observed < instant(old['observed_at'])):
                raise ValueError('future/regressing observation')
            rows, seen = [], set()
            for row in raw['assignments']:
                key = row['id']
                if not isinstance(key, str) or not key or key in seen:
                    raise ValueError('assignment id')
                seen.add(key)
                if row['status'] not in ('not-started', 'draft', 'submitted', 'graded'):
                    raise ValueError('status')
                due = row['due_at']
                if due is not None:
                    due = instant(due).isoformat()
                rows.append({'id': key, 'due_at': due, 'status': row['status']})
            snapshot = {'observed_at': observed.isoformat(), 'assignments': rows}
            before = {r['id']: r for r in old['assignments']} if old else {}
            after = {r['id']: r for r in rows}
            for key in sorted(before.keys() | after.keys()):
                if before.get(key) != after.get(key):
                    changes.append({'source': sid, 'id': key, 'before': before.get(key), 'after': after.get(key), 'observed_at': snapshot['observed_at']})
            state['sources'][sid] = snapshot
            status = 'stale' if now-observed > timedelta(hours=stale_hours) else 'fresh'
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            snapshot = old
            status = 'missing-or-invalid'
        coverage.append({'source': sid, 'status': status, 'observed_at': snapshot['observed_at'] if snapshot else None})
        if snapshot:
            for row in snapshot['assignments']:
                if row['status'] not in ('submitted', 'graded'):
                    active.append(dict(row, source=sid, coverage=status, observed_at=snapshot['observed_at']))
    active.sort(key=lambda r: (r['due_at'] is None, r['due_at'] or '', r['source'], r['id']))
    local = now.astimezone(zone)
    day = local.date().isoformat()
    daily_key = 'daily:' + day
    daily = (local.hour, local.minute) >= (hour, minute) and daily_key not in state['sent']
    events = []
    for change in changes:
        key = 'change:' + hashlib.sha256(json.dumps(change, sort_keys=True).encode()).hexdigest()
        events.append((key, change))
    if config['reminders']:
        for row in active:
            if row['coverage'] == 'fresh' and row['due_at'] and now <= instant(row['due_at']) <= now + timedelta(hours=reminder_hours):
                key = 'due:' + hashlib.sha256(json.dumps([row['source'], row['id'], row['due_at']]).encode()).hexdigest()
                events.append((key, row))
    notifications = [{'key': k, 'evidence': v} for k, v in events if k not in state['sent']]
    state['sent'] = sorted(set(state['sent']) | {n['key'] for n in notifications} | ({daily_key} if daily else set()))
    brief = None
    if daily:
        brief = {'date': day, 'timezone': config['timezone'], 'priorities': active[:3],
                 'unknown_deadlines': [r for r in active if r['due_at'] is None], 'coverage': coverage,
                 'note': 'Deadline ordering, not effort estimation. Missing/stale sources may hide work.'}
    return {'daily_brief': brief, 'notifications': notifications, 'coverage': coverage,
            'next_state': state, 'delivery': 'not-sent', 'submissions_made': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('config'); p.add_argument('--state'); p.add_argument('--now', required=True)
    a = p.parse_args()
    try:
        path = Path(a.config)
        config = json.loads(path.read_text())
        previous = json.loads(Path(a.state).read_text()) if a.state else {}
        print(json.dumps(refresh(config, previous, instant(a.now), path.parent), indent=2))
    except (ValueError, KeyError, TypeError, AttributeError, OSError):
        p.exit(2, 'Refresh failed; preserve checkpoint and inspect private inputs.\n')


if __name__ == '__main__':
    main()
