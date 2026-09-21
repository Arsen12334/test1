def get_result(score, attendance):
    if not isinstance(score, (int, float)):
        raise TypeError("Баллы должны быть числом")

    if not isinstance(attendance, (int, float)):
        raise TypeError("Посещаемость должна быть числом")

    if score < 0 or score > 100:
        return "Некорректный балл"

    if attendance < 0 or attendance > 100:
        return "Некорректная посещаемость"

    if score >= 90 and attendance >= 80:
        return "Отлично"

    if score >= 70 and attendance >= 70:
        return "Хорошо"

    if score >= 50 and attendance >= 60:
        return "Зачёт"

    return "Незачёт"