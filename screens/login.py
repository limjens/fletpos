import flet as ft
import api_service


def login_screen(page: ft.Page, on_login):
    username = ft.TextField(label="Username", width=300)
    password = ft.TextField(
        label="Password", password=True, can_reveal_password=True, width=300
    )
    error = ft.Text(color="red", size=12)

    def handle_login(e):
        try:
            if not username.value or not password.value:
                error.value = "Fill all fields"
                error.color = "red"
                page.update()
                return
            data, status = api_service.login(username.value, password.value)
            if status != 200:
                error.value = data.get("message", "Login failed")
                error.color = "red"
                page.update()
                return
            api_service.set_token(data["token"])
            on_login(data["user"])
        except Exception as ex:
            error.value = f"Login error: {ex}"
            error.color = "red"
            page.update()

    def handle_register(e):
        try:
            if not username.value or not password.value:
                error.value = "Fill all fields"
                error.color = "red"
                page.update()
                return
            data, status = api_service.register(username.value, password.value)
            if status != 201:
                error.value = data.get("message", "Registration failed")
                error.color = "red"
                page.update()
                return
            error.color = "green"
            error.value = "Registered! You can now login."
            page.update()
        except Exception as ex:
            error.value = f"Registration error: {ex}"
            error.color = "red"
            page.update()

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.STORE, size=60, color="indigo"),
                ft.Text("FlowStock POS", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("Sign in to continue", size=14, color="grey"),
                username,
                password,
                error,
                ft.ElevatedButton(
                    "Login",
                    width=300,
                    on_click=handle_login,
                    style=ft.ButtonStyle(bgcolor="indigo", color="white"),
                ),
                ft.TextButton("Register new account", on_click=handle_register),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
        ),
        alignment=ft.Alignment(0, 0),
        expand=True,
    )
