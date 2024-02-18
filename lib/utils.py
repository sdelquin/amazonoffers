import re


def str2num(text: str, cast=float) -> float | int:
    if m := re.search(r'(\d+)(?=[.,](\d+))?[€$]?', text):
        int_part, dec_part = m.groups()
        num = float(f'{int_part}.{dec_part or 0}')
        return cast(num)
    raise ValueError(f'Cannot parse "{text}" into number')
