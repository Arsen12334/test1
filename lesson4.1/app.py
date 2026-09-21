import flet as ft
from student_service import add_student, get_students, update_student, delete_student


def main(page: ft.Page):
    page.title = 'Студенты'
    page.window.width = 800
    page.window.height = 600

    name = ft.TextField(label='Имя')
    surname = ft.TextField(label='Фамилия')
    age = ft.TextField(label='Возраст')
    score = ft.TextField(label='Баллы')

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('ID')),
            ft.DataColumn(ft.Text('Имя')),
            ft.DataColumn(ft.Text('Фамилия')),
            ft.DataColumn(ft.Text('Возраст')),
            ft.DataColumn(ft.Text('Баллы'))
        ],
        rows=[]
    )

    def refresh_table():
        table.rows.clear()
        for student in get_students():
            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(student['id']))),
                        ft.DataCell(ft.Text(str(student['name']))),
                        ft.DataCell(ft.Text(str(student['surname']))),
                        ft.DataCell(ft.Text(str(student['age']))),
                        ft.DataCell(ft.Text(str(student['score']))),
                    ]
                )
            )
        page.update()

    def add_click(e):
        try:
            add_student(name.value, surname.value, int(age.value), int(score.value))
            name.value = ''
            surname.value = ''
            age.value = ''
            score.value = ''
            refresh_table()
        except ValueError as error:
            page.snack_bar = ft.SnackBar(ft.Text(str(error)))
            page.snack_bar.open = True
            page.update()

    page.add(
        ft.Text('Система управления студентами!', size=25),
        name, surname, age, score,
        ft.Button('добавить', on_click=add_click),
        table
    )

    refresh_table()

ft.run(main)