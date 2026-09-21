students = []
next_id = 1


def add_student(name, surname, age, score):
    if age < 16 or age > 100: 
        raise ValueError("Некорректный возраст")

    if score < 0 or score > 100:
        raise ValueError("Некорректный балл")

    global next_id

    student = {
        "id": next_id,
        "name": name,
        "surname": surname,
        "age": age,
        "score": score
    }

    students.append(student)
    next_id += 1

    return student


def get_students():
    return students


def update_student(student_id, name, surname, age, score):
    for student in students:
        if student["id"] == student_id:
            student["name"] = name
            student["surname"] = surname
            student["age"] = age
            student["score"] = score
            return student
    return None


def delete_student(student_id):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return True
    return False