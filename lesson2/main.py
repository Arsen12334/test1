import flet as ft

def main(page: ft.Page):
    page.title = "Мой счётчик"
    page.window.width = 400
    page.window.height = 500
    page.window.resizable = False
    page.bgcolor = "#1a1a2e"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    count = ft.Text(
        value="0",
        size=70,
        weight=ft.FontWeight.BOLD,
        color="#ffffff",
    )

    def increase(e):
        count.value = str(int(count.value) + 1)
        page.update()

    def decrease(e):
        count.value = str(int(count.value) - 1)
        page.update()

    def reset(e):
        count.value = "0"
        page.update()

    card = ft.Container(
        content=ft.Column(
            [
                ft.Text("СЧЁТЧИК", size=18, color="#a29bfe", weight=ft.FontWeight.W_600),
                count,
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.REMOVE_CIRCLE,
                            icon_color="#ff6b6b",
                            icon_size=45,
                            on_click=decrease,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.REFRESH,
                            icon_color="#dfe6e9",
                            icon_size=30,
                            on_click=reset,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.ADD_CIRCLE,
                            icon_color="#55efc4",
                            icon_size=45,
                            on_click=increase,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        width=300,
        padding=40,
        bgcolor="#16213e",
        border_radius=25,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=25,
            color="#00000080",
            offset=ft.Offset(0, 10),
        ),
    )

    page.add(card)

ft.run(main)