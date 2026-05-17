import requests

BASE_URL = "http://localhost:3000/api"
token = None


def set_token(t):
    global token
    token = t


def get_headers():
    return {"Authorization": f"Bearer {token}"}


def login(username, password):
    try:
        res = requests.post(
            f"{BASE_URL}/auth/login", json={"username": username, "password": password}
        )
        return res.json(), res.status_code
    except Exception as e:
        return {"message": str(e)}, 500


def register(username, password):
    try:
        res = requests.post(
            f"{BASE_URL}/auth/register",
            json={"username": username, "password": password},
        )
        return res.json(), res.status_code
    except Exception as e:
        return {"message": str(e)}, 500


def get_products():
    try:
        res = requests.get(f"{BASE_URL}/products", headers=get_headers())
        return res.json(), res.status_code
    except Exception as e:
        return {"message": str(e)}, 500


def add_product(name, price, stock):
    try:
        res = requests.post(
            f"{BASE_URL}/products",
            json={"name": name, "price": price, "stock": stock},
            headers=get_headers(),
        )
        return res.json(), res.status_code
    except Exception as e:
        return {"message": str(e)}, 500


def update_product(id, name, price, stock):
    try:
        res = requests.put(
            f"{BASE_URL}/products/{id}",
            json={"name": name, "price": price, "stock": stock},
            headers=get_headers(),
        )
        return res.json(), res.status_code
    except Exception as e:
        return {"message": str(e)}, 500


def delete_product(id):
    try:
        res = requests.delete(f"{BASE_URL}/products/{id}", headers=get_headers())
        return res.json(), res.status_code
    except Exception as e:
        return {"message": str(e)}, 500


def get_transactions():
    try:
        res = requests.get(f"{BASE_URL}/transactions", headers=get_headers())
        return res.json(), res.status_code
    except Exception as e:
        return {"message": str(e)}, 500


def add_transaction(items, total):
    try:
        res = requests.post(
            f"{BASE_URL}/transactions",
            json={"items": items, "total": total},
            headers=get_headers(),
        )
        return res.json(), res.status_code
    except Exception as e:
        return {"message": str(e)}, 500
