# ============================================================
# SALES REPORT SCREEN — connected to API
# ============================================================

import flet as ft
import api_service


def sales_report_screen(page: ft.Page):
    report_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    error = ft.Text(color="red", size=12)

    def refresh(e=None):
        try:
            report_list.controls.clear()
            error.value = ""
            transactions, status = api_service.get_transactions()

            if status != 200:
                error.value = "Failed to load transactions"
                page.update()
                return

            if not transactions:
                report_list.controls.append(
                    ft.Text("No transactions yet.", color="grey")
                )
                page.update()
                return

            total_sales = sum(float(t["total"]) for t in transactions)

            for t in transactions:
                try:
                    items_text = ", ".join(
                        f"{i['name']} x{i['qty']}" for i in t["items"]
                    )
                    report_list.controls.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ft.Text(
                                                    f"Transaction #{t['id'][:8]}...",
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                                ft.Text(
                                                    t["date"], color="grey", size=12
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        ),
                                        ft.Text(items_text, color="grey", size=12),
                                        ft.Text(
                                            f"Total: ₱{float(t['total']):.2f}",
                                            color="green",
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                    ],
                                ),
                                padding=12,
                            )
                        )
                    )
                except Exception as ex:
                    report_list.controls.append(
                        ft.Text(f"Error loading transaction: {ex}", color="red")
                    )

            report_list.controls.append(ft.Divider())
            report_list.controls.append(
                ft.Text(
                    f"Overall Sales: ₱{total_sales:.2f}",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color="indigo",
                )
            )
            page.update()

        except Exception as ex:
            error.value = f"Failed to load sales report: {ex}"
            page.update()

    refresh()

    return ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text("Sales Report", size=24, weight=ft.FontWeight.BOLD),
                    ft.IconButton(ft.Icons.REFRESH, on_click=refresh),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            error,
            ft.Divider(),
            report_list,
        ],
        expand=True,
    )
