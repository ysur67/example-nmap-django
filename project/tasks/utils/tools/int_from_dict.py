

def get_int_value(dict_: dict, key, incoming_default_value: int = 0):
    """Получить int из переданного dict

    Args:
        dict_ (dict): Словарь
        key (Any): Ключ, по которому требуется получить значение

    Returns:
        int: Искомое значение, если было найдено
        или переданное значение по умолчанию
        (0 by default)
    """
    DEFAULT_VALUE = incoming_default_value
    try:
        return int(dict_.get(key, DEFAULT_VALUE))
    except TypeError:
        return DEFAULT_VALUE
