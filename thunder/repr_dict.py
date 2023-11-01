from typing import Any


def repr_dict(data: Any, child_indent: int = 4, indent: int = 0, is_last: bool = True, prefix: str = '') -> str:
    if not isinstance(data, (dict, list)):
        return f"{prefix}{'└── ' if is_last else '├── '}{data}\n"

    results = []
    if isinstance(data, dict):
        items = list(data.items())
        is_dict = True
    else:
        items = list(enumerate(data))
        is_dict = False

    for i, (key, value) in enumerate(items):
        is_last_item = i == len(items) - 1
        spaces = ' ' * (child_indent * indent)
        connector = '└── ' if is_last_item else '├── '
        key_str = ''
        if is_dict:
            longest_key = max(len(str(k)) for k in data.keys())
            key_str = str(key).ljust(longest_key + 3)
            if not isinstance(value, (dict, list)):
                key_str += ': '
        new_prefix = f"{spaces}{connector}{key_str}"
        child_prefix = spaces + ('│   ' if not is_last else '    ')
        if isinstance(value, dict):
            results.append(f"{new_prefix}\n{repr_dict(value, child_indent, indent + 1, is_last_item, child_prefix)}")
        elif isinstance(value, list):
            results.append(f"{spaces}{connector}{'LIST ITEM' if type(value) in [list, dict] else value}"
                           f"\n{repr_dict(value, child_indent, indent + 1, is_last_item, child_prefix)}")
        else:
            results.append(f"{new_prefix}{value}\n")

    return ''.join(results)

