MIN_VALUE = -100
MAX_VALUE = 100


def increment(value):
    if not isinstance(value, int):
        raise TypeError("Значение счётчика должно быть числом (int)")
    if value >= MAX_VALUE:
        raise ValueError(f"Счётчик не может быть больше {MAX_VALUE}")
    return value + 1       

def decrement(value):
    if not isinstance(value, int):
        raise TypeError("Значение счётчика должно быть числом (int)")
    if value <= MIN_VALUE:
        raise ValueError(f"Счётчик не может быть меньше {MIN_VALUE}")
    return value - 1


def reset():
    return 0