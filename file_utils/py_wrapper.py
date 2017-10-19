
def get_or(dict1, key):
    return dict1.get(key, key)


def left_outer_compose(dict2, dict1):
    if not dict2:
        return dict1
    return {k: get_or(dict2, v) for k, v in dict1.items()}


def full_outer_compose(dict2, dict1):
    if not dict1 or not dict2:
        return dict2 or dict1 # the order matters: None or {} -> {}; {} or None -> None
    return {k: get_or(dict2, get_or(dict1, k)) for k in dict1.keys() | dict2.keys()}