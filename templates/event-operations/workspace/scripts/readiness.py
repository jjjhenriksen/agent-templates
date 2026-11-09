"""Offline, read-only prerequisite checks for a single event day."""
import json
import re
import sys


def check(data):
    cues = data['cues']
    if not isinstance(cues, list):
        raise ValueError('cues must be a list')
    indexed = {}
    def minutes(value):
        if not isinstance(value, str) or not re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d', value):
            raise ValueError('time must be HH:MM on one event day')
        h, m = map(int, value.split(':'))
        return h * 60 + m
    for cue in cues:
        key = cue['id']
        if not isinstance(key, str) or not key or key in indexed:
            raise ValueError('nonempty unique cue IDs required')
        start, end = minutes(cue['start']), minutes(cue['end'])
        if end < start:
            raise ValueError('end before start; split overnight schedules')
        if not isinstance(cue.get('requires', []), list) or not all(isinstance(x, str) for x in cue.get('requires', [])):
            raise ValueError('requires must be a list of IDs')
        for flag in ('accepted', 'ready'):
            if flag in cue and not isinstance(cue[flag], bool):
                raise ValueError(flag + ' must be boolean')
        if not isinstance(cue.get('owner', ''), str):
            raise ValueError('owner must be text')
        indexed[key] = (cue, start, end)
    warnings, visiting, visited = [], set(), set()
    def visit(key):
        if key in visiting:
            raise ValueError('dependency cycle')
        if key in visited:
            return
        visiting.add(key)
        cue, start, _ = indexed[key]
        if not cue.get('owner', '').strip() or cue.get('accepted') is not True:
            warnings.append(key + ': no accepted owner')
        if cue.get('ready') is not True:
            warnings.append(key + ': readiness unconfirmed')
        for dep in cue.get('requires', []):
            if dep not in indexed:
                warnings.append(key + ': missing dependency ' + dep)
                continue
            visit(dep)
            prior, _, end = indexed[dep]
            if end > start:
                warnings.append(key + ': prerequisite finishes too late: ' + dep)
            if prior.get('ready') is not True:
                warnings.append(key + ': prerequisite not ready: ' + dep)
        visiting.remove(key)
        visited.add(key)
    for key in indexed:
        visit(key)
    return warnings


if __name__ == '__main__':
    try:
        with open(sys.argv[1], encoding='utf-8') as source:
            warnings = check(json.load(source))
        print('\n'.join(warnings) if warnings else 'No declared dependency warnings; not a live readiness check.')
        sys.exit(1 if warnings else 0)
    except (ValueError, KeyError, TypeError, IndexError, OSError) as exc:
        print('Invalid schedule: ' + str(exc), file=sys.stderr)
        sys.exit(2)
