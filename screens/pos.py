# ============================================================
# POS SCREEN — connected to API, checkbox + qty adjuster (Redesigned UI)
# ============================================================

import flet as ft
import api_service


def pos_screen(page: ft.Page):
    PRIMARY_COLOR = ft.Colors.INDIGO
    SUCCESS_COLOR = ft.Colors.GREEN_600
    DANGER_COLOR = ft.Colors.RED_400
    BG_COLOR = ft.Colors.GREY_50
    CARD_COLOR = ft.Colors.WHITE

    cart = []
    cart_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=8)
    total_text = ft.Text(
        "₱0.00", size=32, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR
    )
    error = ft.Text(color=DANGER_COLOR, size=12, visible=False)
    search = ft.TextField(
        hint_text="Search products...",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        on_change=lambda e: refresh_products(),
        border_color=ft.Colors.GREY_300,
        focused_border_color=PRIMARY_COLOR,
        bgcolor=CARD_COLOR,
        filled=True,
    )
    product_list = ft.GridView(
        expand=True,
        runs_count=2,
        max_extent=280,
        child_aspect_ratio=1.1,
        spacing=15,
        run_spacing=15,
        padding=ft.Padding(5, 5, 5, 5),
    )

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

                    # Product card
                    product_card = ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(
                                        (
                                            ft.Icons.PRODUCTION_QUANTITY_LIMITS
                                            if out_of_stock
                                            else ft.Icons.INVENTORY_2
                                        ),
                                        size=40,
                                        color=(
                                            ft.Colors.GREY_400
                                            if out_of_stock
                                            else PRIMARY_COLOR
                                        ),
                                    ),
                                    alignment=ft.Alignment(0, 0),
                                    expand=True,
                                ),
                                ft.Text(
                                    p["name"],
                                    weight=ft.FontWeight.W_600,
                                    size=14,
                                    text_align=ft.TextAlign.CENTER,
                                    color=(
                                        ft.Colors.GREY_600
                                        if out_of_stock
                                        else ft.Colors.GREY_900
                                    ),
                                ),
                                ft.Text(
                                    f"₱{float(p['price']):.2f}",
                                    weight=ft.FontWeight.BOLD,
                                    size=16,
                                    color=PRIMARY_COLOR,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Text(
                                    f"Stock: {p['stock']}",
                                    size=11,
                                    color=(
                                        DANGER_COLOR
                                        if out_of_stock
                                        else ft.Colors.GREY_500
                                    ),
                                ),
                                ft.Checkbox(
                                    value=in_cart is not None,
                                    disabled=out_of_stock,
                                    on_change=lambda e, p=p: toggle_cart(
                                        p, e.control.value
                                    ),
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        padding=ft.Padding(12, 12, 12, 12),
                        bgcolor=CARD_COLOR,
                        border_radius=ft.BorderRadius(15, 15, 15, 15),
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=8,
                            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                            offset=ft.Offset(0, 2),
                        ),
                        ink=True,
                    )
                    product_list.controls.append(product_card)
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
            refresh_products()
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
            if not cart:
                cart_list.controls.append(
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Icon(
                                    ft.Icons.SHOPPING_CART_OUTLINED,
                                    size=50,
                                    color=ft.Colors.GREY_300,
                                ),
                                ft.Text(
                                    "Your cart is empty",
                                    size=14,
                                    color=ft.Colors.GREY_400,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        alignment=ft.Alignment(0, 0),
                        expand=True,
                    )
                )
            else:
                for item in cart:
                    cart_item = ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    item["name"], weight=ft.FontWeight.W_600, size=14
                                ),
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            ft.Icons.REMOVE_CIRCLE_OUTLINE,
                                            on_click=lambda e, i=item: change_qty(
                                                i, -1
                                            ),
                                            icon_size=24,
                                            icon_color=DANGER_COLOR,
                                        ),
                                        ft.Text(
                                            f"{item['qty']}",
                                            width=30,
                                            text_align=ft.TextAlign.CENTER,
                                            weight=ft.FontWeight.W_500,
                                            size=16,
                                        ),
                                        ft.IconButton(
                                            ft.Icons.ADD_CIRCLE_OUTLINE,
                                            on_click=lambda e, i=item: change_qty(i, 1),
                                            icon_size=24,
                                            icon_color=SUCCESS_COLOR,
                                        ),
                                        ft.Container(expand=True),
                                        ft.Text(
                                            f"₱{float(item['price']) * item['qty']:.2f}",
                                            weight=ft.FontWeight.W_600,
                                            size=15,
                                            color=PRIMARY_COLOR,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    spacing=5,
                                ),
                            ],
                            spacing=8,
                        ),
                        padding=ft.Padding(12, 10, 12, 10),
                        bgcolor=ft.Colors.with_opacity(0.05, PRIMARY_COLOR),
                        border_radius=ft.BorderRadius(10, 10, 10, 10),
                        border=ft.Border(
                            left=ft.BorderSide(
                                1, ft.Colors.with_opacity(0.1, PRIMARY_COLOR)
                            ),
                            right=ft.BorderSide(
                                1, ft.Colors.with_opacity(0.1, PRIMARY_COLOR)
                            ),
                            top=ft.BorderSide(
                                1, ft.Colors.with_opacity(0.1, PRIMARY_COLOR)
                            ),
                            bottom=ft.BorderSide(
                                1, ft.Colors.with_opacity(0.1, PRIMARY_COLOR)
                            ),
                        ),
                    )
                    cart_list.controls.append(cart_item)

            total = sum(float(i["price"]) * i["qty"] for i in cart)
            total_text.value = f"₱{total:.2f}"
            page.update()
        except Exception as ex:
            show_error(f"Failed to refresh cart: {ex}")

    def checkout(e):
        try:
            if not cart:
                show_error("Cart is empty")
                return

            # Show loading
            checkout_btn.content = ft.Row(
                controls=[
                    ft.ProgressRing(
                        width=20, height=20, stroke_width=2, color=ft.Colors.WHITE
                    ),
                    ft.Text("Processing...", color=ft.Colors.WHITE),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            )
            checkout_btn.disabled = True
            page.update()

            for item in cart:
                new_stock = item["stock"] - item["qty"]
                api_service.update_product(
                    item["id"], item["name"], item["price"], new_stock
                )

            total = sum(float(i["price"]) * i["qty"] for i in cart)
            api_service.add_transaction(
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

            # Success dialog
            dlg = ft.AlertDialog(
                title=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color=SUCCESS_COLOR),
                        ft.Text(
                            "Checkout Successful!", size=18, weight=ft.FontWeight.BOLD
                        ),
                    ],
                    spacing=10,
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                f"Total Amount:", size=14, color=ft.Colors.GREY_600
                            ),
                            ft.Text(
                                f"₱{total:.2f}",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=SUCCESS_COLOR,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                    ),
                    padding=ft.Padding(20, 10, 20, 10),
                ),
                actions=[
                    ft.TextButton(
                        "OK",
                        on_click=lambda e: close_dlg(dlg),
                        style=ft.ButtonStyle(color=PRIMARY_COLOR),
                    ),
                ],
            )
            page.overlay.append(dlg)
            dlg.open = True
            page.update()

            # Reset button
            checkout_btn.content = ft.Text(
                "Checkout", color=ft.Colors.WHITE, weight=ft.FontWeight.W_600
            )
            checkout_btn.disabled = False
            page.update()
        except Exception as ex:
            show_error(f"Checkout failed: {ex}")
            checkout_btn.content = ft.Text(
                "Checkout", color=ft.Colors.WHITE, weight=ft.FontWeight.W_600
            )
            checkout_btn.disabled = False
            page.update()

    def close_dlg(dlg):
        dlg.open = False
        page.update()

    checkout_btn = ft.ElevatedButton(
        content=ft.Text("Checkout", color=ft.Colors.WHITE, weight=ft.FontWeight.W_600),
        on_click=checkout,
        width=220,
        height=45,
        style=ft.ButtonStyle(
            bgcolor=SUCCESS_COLOR,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
    )

    refresh_products()

    # Left panel - Products
    left_panel = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            "Products",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800,
                        ),
                        ft.IconButton(
                            ft.Icons.REFRESH,
                            on_click=lambda e: refresh_products(),
                            icon_color=PRIMARY_COLOR,
                            tooltip="Refresh",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                search,
                ft.Container(
                    content=error,
                    margin=ft.Margin(0, 0, 0, 0),
                ),
                product_list,
            ],
            expand=True,
            spacing=15,
        ),
        expand=True,
        padding=ft.Padding(20, 20, 20, 20),
        bgcolor=BG_COLOR,
    )

    # Right panel - Cart
    right_panel = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Shopping Cart",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_800,
                ),
                ft.Divider(height=1, color=ft.Colors.GREY_200),
                cart_list,
                ft.Divider(height=1, color=ft.Colors.GREY_200),
                ft.Row(
                    controls=[
                        ft.Text(
                            "Total:",
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=ft.Colors.GREY_700,
                        ),
                        total_text,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                checkout_btn,
            ],
            expand=True,
            spacing=12,
        ),
        width=340,
        padding=ft.Padding(20, 20, 20, 20),
        bgcolor=CARD_COLOR,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
            offset=ft.Offset(-2, 0),
        ),
    )

    return ft.Row(
        [left_panel, right_panel],
        expand=True,
        spacing=0,
    )
