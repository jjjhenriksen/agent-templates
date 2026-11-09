"""Intentionally broken fixture: truncates decimals and accepts negatives."""
def parse_count(value):
    return int(float(value))
