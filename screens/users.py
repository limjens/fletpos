import flet as ft
import api_service


def users_screen(page: ft.Page, current_user):
    username = ft.TextField(label="Username", expand=True)
    password = ft.TextField(
        label="Password", password=True, can_reveal_password=True, width=200
    )
    error = ft.Text(color="red", size=12)
    user_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def show_error(msg, color="red"):
        error.value = msg
        error.color = color
        page.update()

    def refresh():
        try:
            user_list.controls.clear()
            users, status = api_service.get_users()
            if status != 200:
                show_error("Failed to load users")
                return
            for u in users:
                is_current = u["username"] == current_user["username"]
                user_list.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.Icons.PERSON, color="indigo"),
                                            ft.Text(
                                                u["username"], weight=ft.FontWeight.BOLD
                                            ),
                                            ft.Container(
                                                content=ft.Text(
                                                    "you", size=11, color="white"
                                                ),
                                                bgcolor="indigo",
                                                border_radius=10,
                                                padding=ft.Padding(8, 2, 8, 2),
                                                visible=is_current,
                                            ),
                                        ],
                                        expand=True,
                                    ),
                                    ft.IconButton(
                                        ft.Icons.EDIT,
                                        on_click=lambda e, u=u: open_edit(u),
                                        icon_color="blue",
                                    ),
                                    ft.IconButton(
                                        ft.Icons.DELETE,
                                        on_click=lambda e, u=u: handle_delete(
                                            u["username"]
                                        ),
                                        icon_color="red",
                                        disabled=is_current,
                                    ),
                                ],
                            ),
                            padding=10,
                        )
                    )
                )
            page.update()
        except Exception as ex:
            show_error(f"Failed to load users: {ex}")

    def handle_add(e):
        try:
            if not username.value or not password.value:
                show_error("Fill all fields")
                return
            data, status = api_service.add_user(username.value, password.value)
            if status != 201:
                show_error(data.get("message", "Failed to add user"))
                return
            username.value = password.value = error.value = ""
            show_error("User added successfully!", color="green")
            refresh()
        except Exception as ex:
            show_error(f"Failed to add user: {ex}")

    def handle_delete(uname):
        try:
            data, status = api_service.delete_user(uname)
            if status != 200:
                show_error(data.get("message", "Failed to delete user"))
                return
            refresh()
        except Exception as ex:
            show_error(f"Failed to delete user: {ex}")

    def open_edit(u):
        new_password = ft.TextField(
            label="New Password", password=True, can_reveal_password=True
        )
        edit_error = ft.Text(color="red", size=12)

        def save_edit(e):
            try:
                if not new_password.value:
                    edit_error.value = "Password cannot be empty"
                    page.update()
                    return
                data, status = api_service.update_user(
                    u["username"], new_password.value
                )
                if status != 200:
                    edit_error.value = data.get("message", "Failed to update user")
                    page.update()
                    return
                dlg.open = False
                show_error("Password updated!", color="green")
                refresh()
            except Exception as ex:
                edit_error.value = f"Failed to update: {ex}"
                page.update()

        def close_dlg():
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text(f"Edit User: {u['username']}"),
            content=ft.Column(
                controls=[
                    ft.Text("Change password:", color="grey", size=12),
                    new_password,
                    edit_error,
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: close_dlg()),
                ft.ElevatedButton("Save", on_click=save_edit),
            ],
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    refresh()

    return ft.Column(
        controls=[
            ft.Text("Users", size=24, weight=ft.FontWeight.BOLD),
            ft.Row(controls=[username, password]),
            error,
            ft.ElevatedButton(
                "Add User", on_click=handle_add, icon=ft.Icons.PERSON_ADD
            ),
            ft.Divider(),
            user_list,
        ],
        expand=True,
    )
