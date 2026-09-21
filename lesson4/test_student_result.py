import pytest
from student_result import get_result


# --- Обычные (типичные) сценарии для каждого класса эквивалентности ---

@pytest.mark.parametrize("score, attendance, expected", [
    (95, 85, "Отлично"),
    (75, 75, "Хорошо"),
    (55, 65, "Зачёт"),
    (30, 30, "Незачёт"),
])
def test_typical_cases(score, attendance, expected):
    assert get_result(score, attendance) == expected


# --- Некорректные значения (вне диапазона 0-100) ---

@pytest.mark.parametrize("score, attendance, expected", [
    (-1, 50, "Некорректный балл"),
    (150, 50, "Некорректный балл"),
    (50, -1, "Некорректная посещаемость"),
    (50, 150, "Некорректная посещаемость"),
])
def test_invalid_ranges(score, attendance, expected):
    assert get_result(score, attendance) == expected


# --- Некорректный тип данных ---

@pytest.mark.parametrize("score, attendance", [
    ("abc", 50),
    (None, 50),
    (50, "abc"),
    (50, None),
])
def test_wrong_type_raises_error(score, attendance):
    with pytest.raises(TypeError):
        get_result(score, attendance)


# --- Граничные значения score (attendance зафиксирован на 100) ---

@pytest.mark.parametrize("score, expected", [
    (0, "Незачёт"),
    (49, "Незачёт"),
    (50, "Зачёт"),
    (69, "Зачёт"),
    (70, "Хорошо"),
    (89, "Хорошо"),
    (90, "Отлично"),
    (100, "Отлично"),
])
def test_score_boundaries(score, expected):
    assert get_result(score, 100) == expected


# --- Граничные значения attendance (score зафиксирован на 100) ---

@pytest.mark.parametrize("attendance, expected", [
    (0, "Незачёт"),
    (59, "Незачёт"),
    (60, "Зачёт"),
    (69, "Зачёт"),
    (70, "Хорошо"),
    (79, "Хорошо"),
    (80, "Отлично"),
    (100, "Отлично"),
])
def test_attendance_boundaries(attendance, expected):
    assert get_result(100, attendance) == expected