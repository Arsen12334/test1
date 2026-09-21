from counter_logic import increment, decrement, reset, MIN_VALUE, MAX_VALUE
import pytest

# --- корректная работа ---

def test_increment_normal():
    assert increment(5) == 6

def test_decrement_normal():
    assert decrement(5) == 4

def test_reset():
    assert reset() == 0

# --- границы (тоже часть корректной работы) ---

def test_increment_below_max():
    assert increment(MAX_VALUE - 1) == MAX_VALUE

def test_decrement_above_min():
    assert decrement(MIN_VALUE + 1) == MIN_VALUE

# --- обработка некорректных данных ---

def test_increment_at_max_raises_error():
    with pytest.raises(ValueError):
        increment(MAX_VALUE)

def test_decrement_at_min_raises_error():
    with pytest.raises(ValueError):
        decrement(MIN_VALUE)

def test_increment_wrong_type_raises_error():
    with pytest.raises(TypeError):
        increment("5")

def test_decrement_wrong_type_raises_error():
    with pytest.raises(TypeError):
        decrement(None)