import flet as ft
import api_service


def login_screen(page: ft.Page, on_login):
    # Modern styling with glassmorphism
    PRIMARY_COLOR = ft.Colors.INDIGO

    username = ft.TextField(
        hint_text="Username",
        width=320,
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        border_color=ft.Colors.WHITE,
        focused_border_color=PRIMARY_COLOR,
        bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
        text_size=14,
        content_padding=ft.Padding(12, 16, 12, 16),
        border_radius=10,
    )
    password = ft.TextField(
        hint_text="Password",
        password=True,
        can_reveal_password=True,
        width=320,
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        border_color=ft.Colors.WHITE,
        focused_border_color=PRIMARY_COLOR,
        bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
        text_size=14,
        content_padding=ft.Padding(12, 16, 12, 16),
        border_radius=10,
    )
    error = ft.Text(color=ft.Colors.RED_400, size=12, visible=False)

    def handle_login(e):
        try:
            if not username.value or not password.value:
                error.value = "Please fill in all fields"
                error.color = ft.Colors.RED_400
                error.visible = True
                page.update()
                return

            # Show loading state
            login_btn.content = ft.Row(
                controls=[
                    ft.ProgressRing(
                        width=20, height=20, stroke_width=2, color=ft.Colors.WHITE
                    ),
                    ft.Text("Logging in...", color=ft.Colors.WHITE),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            )
            login_btn.disabled = True
            page.update()

            data, status = api_service.login(username.value, password.value)

            if status != 200:
                error.value = data.get("message", "Login failed")
                error.color = ft.Colors.RED_400
                error.visible = True
                login_btn.content = ft.Text("Login", color=ft.Colors.WHITE)
                login_btn.disabled = False
                page.update()
                return

            api_service.set_token(data["token"])
            on_login(data["user"])
        except Exception as ex:
            error.value = f"Login error: {ex}"
            error.color = ft.Colors.RED_400
            error.visible = True
            login_btn.content = ft.Text("Login", color=ft.Colors.WHITE)
            login_btn.disabled = False
            page.update()

    def handle_register(e):
        try:
            if not username.value or not password.value:
                error.value = "Please fill in all fields"
                error.color = ft.Colors.RED_400
                error.visible = True
                page.update()
                return

            # Show loading state
            register_btn.content = ft.Row(
                controls=[
                    ft.ProgressRing(
                        width=16, height=16, stroke_width=2, color=ft.Colors.WHITE
                    ),
                    ft.Text("Creating account...", color=ft.Colors.WHITE),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            )
            register_btn.disabled = True
            page.update()

            data, status = api_service.register(username.value, password.value)

            if status != 201:
                error.value = data.get("message", "Registration failed")
                error.color = ft.Colors.RED_400
                error.visible = True
            else:
                error.value = "✓ Account created successfully! You can now login."
                error.color = ft.Colors.GREEN_400
                error.visible = True
                username.value = ""
                password.value = ""

            register_btn.content = ft.Text("Create Account", color=ft.Colors.WHITE)
            register_btn.disabled = False
            page.update()
        except Exception as ex:
            error.value = f"Registration error: {ex}"
            error.color = ft.Colors.RED_400
            error.visible = True
            register_btn.content = ft.Text("Create Account", color=ft.Colors.WHITE)
            register_btn.disabled = False
            page.update()

    login_btn = ft.ElevatedButton(
        content=ft.Text(
            "Login", color=ft.Colors.WHITE, size=15, weight=ft.FontWeight.W_600
        ),
        width=320,
        height=45,
        on_click=handle_login,
        style=ft.ButtonStyle(
            bgcolor=PRIMARY_COLOR,
            color=ft.Colors.WHITE,
            elevation={"pressed": 0, "": 3},
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
    )

    register_btn = ft.TextButton(
        content=ft.Text(
            "Create Account", size=13, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500
        ),
        on_click=handle_register,
        style=ft.ButtonStyle(color=ft.Colors.WHITE),
    )

    # Glassmorphism card with blur effect
    login_card = ft.Container(
        content=ft.Column(
            controls=[
                # Logo section
                ft.Container(
                    content=ft.Icon(ft.Icons.STORE, size=70, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                    border_radius=ft.BorderRadius(35, 35, 35, 35),
                    padding=ft.Padding(20, 20, 20, 20),
                    margin=ft.Margin(0, 0, 0, 10),
                ),
                ft.Text(
                    "FlowStock POS",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Text(
                    "Smart Inventory Management",
                    size=13,
                    color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
                ),
                ft.Container(height=20),
                username,
                ft.Container(height=5),
                password,
                ft.Container(
                    content=error,
                    margin=ft.Margin(0, 10, 0, 0),
                ),
                login_btn,
                ft.Row(
                    controls=[
                        ft.Text(
                            "Don't have an account?",
                            size=12,
                            color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE),
                        ),
                        register_btn,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        width=420,
        blur=ft.Blur(10, 10),
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
        border_radius=ft.BorderRadius(25, 25, 25, 25),
        border=ft.Border(
            left=ft.BorderSide(
                width=1, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)
            ),
            right=ft.BorderSide(
                width=1, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)
            ),
            top=ft.BorderSide(
                width=1, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)
            ),
            bottom=ft.BorderSide(
                width=1, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)
            ),
        ),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=30,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(0, 10),
        ),
        padding=ft.Padding(40, 40, 40, 40),
    )

    # Gradient background
    background = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[ft.Colors.INDIGO_800, ft.Colors.BLUE_600, ft.Colors.PURPLE_600],
        ),
    )

    return ft.Stack(
        controls=[
            background,
            ft.Container(
                content=login_card,
                alignment=ft.Alignment(0, 0),
                expand=True,
            ),
        ],
        expand=True,
    )
