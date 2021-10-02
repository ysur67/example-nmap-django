from functools import singledispatch

@singledispatch
def keys_to_strings(ob):
    return ob

@keys_to_strings.register
def _handle_dict(ob: dict):
    return {str(k): keys_to_strings(v) for k, v in ob.items()}

@keys_to_strings.register
def _handle_list(ob: list):
    return [keys_to_strings(v) for v in ob]
