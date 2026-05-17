import flet as ft
import api_service


def inventory_screen(page: ft.Page):
    name = ft.TextField(label="Product Name", expand=True)
    price = ft.TextField(label="Price", width=120, keyboard_type=ft.KeyboardType.NUMBER)
    stock = ft.TextField(label="Stock", width=120, keyboard_type=ft.KeyboardType.NUMBER)
    error = ft.Text(color="red", size=12)
    product_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def show_error(msg, color="red"):
        error.value = msg
        error.color = color
        page.update()

    def refresh():
        try:
            product_list.controls.clear()
            products, status = api_service.get_products()
            if status != 200:
                show_error("Failed to load products")
                return
            for p in products:
                product_list.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                p["name"], weight=ft.FontWeight.BOLD
                                            ),
                                            ft.Text(
                                                f"₱{p['price']} | Stock: {p['stock']}",
                                                color="grey",
                                                size=12,
                                            ),
                                        ],
                                        expand=True,
                                    ),
                                    ft.IconButton(
                                        ft.Icons.EDIT,
                                        on_click=lambda e, p=p: open_edit(p),
                                        icon_color="blue",
                                    ),
                                    ft.IconButton(
                                        ft.Icons.DELETE,
                                        on_click=lambda e, p=p: handle_delete(p["id"]),
                                        icon_color="red",
                                    ),
                                ],
                            ),
                            padding=10,
                        )
                    )
                )
            page.update()
        except Exception as ex:
            show_error(f"Failed to load products: {ex}")

    def handle_add(e):
        try:
            if not name.value or not price.value or not stock.value:
                show_error("Fill all fields")
                return
            data, status = api_service.add_product(
                name.value, float(price.value), int(stock.value)
            )
            if status != 201:
                show_error(data.get("message", "Failed to add product"))
                return
            name.value = price.value = stock.value = error.value = ""
            show_error("Product added!", color="green")
            refresh()
        except ValueError:
            show_error("Price and stock must be valid numbers")
        except Exception as ex:
            show_error(f"Failed to add product: {ex}")

    def handle_delete(id):
        try:
            data, status = api_service.delete_product(id)
            if status != 200:
                show_error(data.get("message", "Failed to delete product"))
                return
            refresh()
        except Exception as ex:
            show_error(f"Failed to delete product: {ex}")

    def open_edit(p):
        edit_name = ft.TextField(label="Name", value=p["name"])
        edit_price = ft.TextField(label="Price", value=str(p["price"]))
        edit_stock = ft.TextField(label="Stock", value=str(p["stock"]))
        edit_error = ft.Text(color="red", size=12)

        def save_edit(e):
            try:
                if not edit_name.value or not edit_price.value or not edit_stock.value:
                    edit_error.value = "Fill all fields"
                    page.update()
                    return
                data, status = api_service.update_product(
                    p["id"],
                    edit_name.value,
                    float(edit_price.value),
                    int(edit_stock.value),
                )
                if status != 200:
                    edit_error.value = data.get("message", "Failed to update product")
                    page.update()
                    return
                dlg.open = False
                refresh()
            except ValueError:
                edit_error.value = "Price and stock must be valid numbers"
                page.update()
            except Exception as ex:
                edit_error.value = f"Failed to update: {ex}"
                page.update()

        def close_dlg():
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Edit Product"),
            content=ft.Column(
                controls=[edit_name, edit_price, edit_stock, edit_error], tight=True
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
            ft.Text("Inventory", size=24, weight=ft.FontWeight.BOLD),
            ft.Row(controls=[name, price, stock]),
            error,
            ft.ElevatedButton("Add Product", on_click=handle_add, icon=ft.Icons.ADD),
            ft.Divider(),
            product_list,
        ],
        expand=True,
    )
