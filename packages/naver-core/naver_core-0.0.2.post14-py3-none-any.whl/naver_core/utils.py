def replaceDictIf(data, key, replacement):
    """Método para remplazar un valor de un diccionario en caso de que coincida con una llave
    Args:
        data (dict): Diccionario con los datos de entrada
        key (str): Llave del diccionario
        replacement (any): Valor por defecto

    Returns:
        any: Valor del diccionario o el valor por defecto
    """
    assert isinstance(data, dict)
    return str(data.get(key)).replace(" ", "") or replacement


def replaceIf(value, key, replacement):
    """Método para remplazar un valor en caso de que coincida con una llave

    Args:
        value (any): Valor a comparar
        key (any): Llave a comparar
        replacement (any): Valor por defecto

    Returns:
        any: Valor por defecto o el valor de entrada
    """    
    if value == key:
        return replacement
    return value
