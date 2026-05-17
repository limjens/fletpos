# ============================================================
# POS SCREEN — connected to API, checkbox + qty adjuster
# ============================================================

import flet as ft
import api_service
import data


def pos_screen(page: ft.Page):
    cart = []
    cart_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=4)
    total_text = ft.Text("Total: ₱0.00", size=18, weight=ft.FontWeight.BOLD)
    error = ft.Text(color="red", size=12, visible=False)
    search = ft.TextField(
        label="Search product", expand=True, on_change=lambda e: refresh_products()
    )
    product_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=4)

    def show_error(msg):
        error.value = msg
        error.visible = True
        page.update()

    def hide_error():
        error.value = ""
        error.visible = False

    def refresh_products():
        try:
            product_list.controls.clear()
            query = search.value.lower()
            products, status = api_service.get_products()
            if status != 200:
                show_error("Failed to load products")
                return
            for p in products:
                if query in p["name"].lower():
                    out_of_stock = int(p["stock"]) <= 0
                    in_cart = next((i for i in cart if i["id"] == p["id"]), None)
                    product_list.controls.append(
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Checkbox(
                                        value=in_cart is not None,
                                        disabled=out_of_stock,
                                        on_change=lambda e, p=p: toggle_cart(
                                            p, e.control.value
                                        ),
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                p["name"],
                                                weight=ft.FontWeight.BOLD,
                                                color="grey" if out_of_stock else None,
                                            ),
                                            ft.Text(
                                                f"₱{float(p['price']):.2f} | Stock: {p['stock']}",
                                                color="red" if out_of_stock else "grey",
                                                size=12,
                                            ),
                                        ],
                                        expand=True,
                                        spacing=2,
                                    ),
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=8,
                            ),
                            padding=ft.Padding(left=10, right=10, top=6, bottom=6),
                            border=ft.Border(
                                left=ft.BorderSide(1, "grey200"),
                                right=ft.BorderSide(1, "grey200"),
                                top=ft.BorderSide(1, "grey200"),
                                bottom=ft.BorderSide(1, "grey200"),
                            ),
                            border_radius=8,
                        )
                    )
            page.update()
        except Exception as ex:
            show_error(f"Failed to load products: {ex}")

    def toggle_cart(p, checked):
        try:
            if checked:
                if not any(i["id"] == p["id"] for i in cart):
                    cart.append(
                        {
                            "id": p["id"],
                            "name": p["name"],
                            "price": float(p["price"]),
                            "stock": int(p["stock"]),
                            "qty": 1,
                        }
                    )
            else:
                cart[:] = [i for i in cart if i["id"] != p["id"]]
            hide_error()
            refresh_cart()
        except Exception as ex:
            show_error(f"Error updating cart: {ex}")

    def change_qty(item, delta):
        try:
            new_qty = item["qty"] + delta
            if new_qty <= 0:
                cart.remove(item)
                refresh_cart()
                refresh_products()
                return
            if new_qty > item["stock"]:
                show_error(f"Not enough stock for {item['name']}")
                return
            item["qty"] = new_qty
            hide_error()
            refresh_cart()
        except Exception as ex:
            show_error(f"Failed to update quantity: {ex}")

    def refresh_cart():
        try:
            cart_list.controls.clear()
            for item in cart:
                cart_list.controls.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text(item["name"], expand=True, size=13),
                                ft.IconButton(
                                    ft.Icons.REMOVE,
                                    on_click=lambda e, item=item: change_qty(item, -1),
                                    icon_size=16,
                                    style=ft.ButtonStyle(
                                        padding=ft.Padding(0, 0, 0, 0)
                                    ),
                                ),
                                ft.Text(
                                    f"{item['qty']}",
                                    width=24,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.IconButton(
                                    ft.Icons.ADD,
                                    on_click=lambda e, item=item: change_qty(item, 1),
                                    icon_size=16,
                                    style=ft.ButtonStyle(
                                        padding=ft.Padding(0, 0, 0, 0)
                                    ),
                                ),
                                ft.Text(
                                    f"₱{float(item['price']) * item['qty']:.2f}",
                                    width=70,
                                    text_align=ft.TextAlign.RIGHT,
                                    size=13,
                                ),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=2,
                        ),
                        padding=ft.Padding(left=8, right=8, top=4, bottom=4),
                        border=ft.Border(
                            left=ft.BorderSide(1, "grey200"),
                            right=ft.BorderSide(1, "grey200"),
                            top=ft.BorderSide(1, "grey200"),
                            bottom=ft.BorderSide(1, "grey200"),
                        ),
                        border_radius=6,
                    )
                )
            total = sum(float(i["price"]) * i["qty"] for i in cart)
            total_text.value = f"Total: ₱{total:.2f}"
            page.update()
        except Exception as ex:
            show_error(f"Failed to refresh cart: {ex}")

    def checkout(e):
        try:
            if not cart:
                show_error("Cart is empty")
                return

            for item in cart:
                new_stock = item["stock"] - item["qty"]
                api_service.update_product(
                    item["id"], item["name"], item["price"], new_stock
                )

            total = sum(float(i["price"]) * i["qty"] for i in cart)
            data.add_transaction(
                items=[
                    {"name": i["name"], "qty": i["qty"], "price": i["price"]}
                    for i in cart
                ],
                total=total,
            )

            cart.clear()
            hide_error()
            refresh_cart()
            refresh_products()

            dlg = ft.AlertDialog(
                title=ft.Text("Checkout Success!"),
                content=ft.Text(f"Total: ₱{total:.2f}"),
                actions=[ft.TextButton("OK", on_click=lambda e: close_dlg(dlg))],
            )
            page.overlay.append(dlg)
            dlg.open = True
            page.update()
        except Exception as ex:
            show_error(f"Checkout failed: {ex}")

    def close_dlg(dlg):
        dlg.open = False
        page.update()

    refresh_products()

    return ft.Row(
        [
            # LEFT — product list
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("Products", size=20, weight=ft.FontWeight.BOLD),
                                ft.IconButton(
                                    ft.Icons.REFRESH,
                                    on_click=lambda e: refresh_products(),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        search,
                        error,
                        product_list,
                    ],
                    expand=True,
                    spacing=2,
                ),
                expand=True,
                padding=10,
            ),
            ft.VerticalDivider(width=1),
            # RIGHT — cart
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Cart", size=20, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=1),
                        cart_list,
                        ft.Divider(height=1),
                        total_text,
                        ft.ElevatedButton(
                            "Checkout",
                            on_click=checkout,
                            width=220,
                            style=ft.ButtonStyle(bgcolor="green", color="white"),
                        ),
                    ],
                    expand=True,
                    spacing=8,
                ),
                width=280,
                padding=10,
            ),
        ],
        expand=True,
        spacing=0,
    )
