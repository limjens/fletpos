# ============================================================
# MAIN — entry point (Redesigned UI)
# ============================================================

import flet as ft
from screens.login import login_screen
from screens.pos import pos_screen
from screens.inventory import inventory_screen
from screens.sales_report import sales_report_screen
from screens.users import users_screen


def main(page: ft.Page):
    page.title = "FlowStock POS"
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 900
    page.window.min_height = 600
    page.padding = 0
    page.bgcolor = ft.Colors.GREY_50
    page.theme_mode = ft.ThemeMode.LIGHT

    PRIMARY_COLOR = ft.Colors.INDIGO
    BG_COLOR = ft.Colors.GREY_50
    CARD_COLOR = ft.Colors.WHITE

    current_user = {"value": None}

    def on_login(user):
        current_user["value"] = user
        show_main()

    def show_main():
        page.controls.clear()

        # Create the screens first to ensure they exist
        pos_content = pos_screen(page)
        inventory_content = inventory_screen(page)
        sales_content = sales_report_screen(page)
        users_content = users_screen(page, current_user["value"])

        tabs = [
            ft.Container(
                content=pos_content, padding=ft.Padding(20, 20, 20, 20), expand=True
            ),
            ft.Container(
                content=inventory_content,
                padding=ft.Padding(20, 20, 20, 20),
                expand=True,
            ),
            ft.Container(
                content=sales_content, padding=ft.Padding(20, 20, 20, 20), expand=True
            ),
            ft.Container(
                content=users_content, padding=ft.Padding(20, 20, 20, 20), expand=True
            ),
        ]

        content_area = ft.Container(content=tabs[0], expand=True)

        def change_tab(e):
            content_area.content = tabs[e.control.selected_index]
            content_area.update()

        # Navigation Rail
        nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            on_change=change_tab,
            bgcolor=CARD_COLOR,
            extended=False,
            min_width=80,
            leading=ft.Icon(ft.Icons.STORE, size=32, color=PRIMARY_COLOR),
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.SHOPPING_CART_OUTLINED,
                    selected_icon=ft.Icons.SHOPPING_CART,
                    label="POS",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.INVENTORY_2_OUTLINED,
                    selected_icon=ft.Icons.INVENTORY_2,
                    label="Inventory",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.BAR_CHART_OUTLINED,
                    selected_icon=ft.Icons.BAR_CHART,
                    label="Sales",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.PEOPLE_OUTLINED,
                    selected_icon=ft.Icons.PEOPLE,
                    label="Users",
                ),
            ],
            trailing=ft.IconButton(
                ft.Icons.LOGOUT,
                on_click=lambda e: show_login(),
                tooltip="Logout",
            ),
        )

        # Main layout
        main_row = ft.Row(
            controls=[
                nav_rail,
                ft.VerticalDivider(width=1),
                content_area,
            ],
            expand=True,
            spacing=0,
        )

        page.add(main_row)
        page.update()

    def show_login():
        page.controls.clear()
        login_container = login_screen(page, on_login)
        page.add(login_container)
        page.update()

    show_login()


ft.app(target=main)
