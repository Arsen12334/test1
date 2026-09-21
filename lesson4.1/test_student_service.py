import pytest
from student_service import add_student, get_students, update_student, delete_student
import student_service


@pytest.fixture(autouse=True)
def reset_students():
    """Перед каждым тестом очищаем список студентов, чтобы тесты не мешали друг другу."""
    student_service.students.clear()
    student_service.next_id = 1
    yield


# --- корректная работа ---

def test_add_student_success():
    student = add_student("Иван", "Иванов", 20, 85)
    assert student["name"] == "Иван"
    assert student["id"] == 1
    assert len(get_students()) == 1


def test_get_students_returns_list():
    add_student("Анна", "Петрова", 22, 90)
    students = get_students()
    assert isinstance(students, list)
    assert students[0]["surname"] == "Петрова"


def test_update_student_success():
    add_student("Иван", "Иванов", 20, 85)
    updated = update_student(1, "Иван", "Сидоров", 21, 95)
    assert updated["surname"] == "Сидоров"
    assert updated["score"] == 95


def test_delete_student_success():
    add_student("Иван", "Иванов", 20, 85)
    result = delete_student(1)
    assert result is True
    assert len(get_students()) == 0


# --- обработка некорректных данных ---

def test_add_student_age_too_low_raises_error():
    with pytest.raises(ValueError):
        add_student("Иван", "Иванов", 10, 85)


def test_add_student_age_too_high_raises_error():
    with pytest.raises(ValueError):
        add_student("Иван", "Иванов", 150, 85)


def test_add_student_score_too_low_raises_error():
    with pytest.raises(ValueError):
        add_student("Иван", "Иванов", 20, -5)


def test_add_student_score_too_high_raises_error():
    with pytest.raises(ValueError):
        add_student("Иван", "Иванов", 20, 150)


def test_update_nonexistent_student_returns_none():
    result = update_student(999, "Кто-то", "Такой", 20, 50)
    assert result is None


def test_delete_nonexistent_student_returns_false():
    result = delete_student(999)
    assert result is False