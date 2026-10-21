from flask import Flask, render_template

app = Flask(__name__)

MENU = [
    {"name": "cà phê đen", "price": 20000, "available": True},
    {"name": "bạc xỉu", "price": 30000, "available": False},
    {"name": "cà phê sữa", "price": 25000, "available": True},
    {"name": "cà phê kem trứng", "price": 35000, "available": True},
    {"name": "cà phê muối", "price": 40000, "available": True},
]


@app.template_filter("vnd")
def vnd(value):
    # 25000 -> "25.000 đ"
    return f"{int(value):,}".replace(",", ".") + " đ"


@app.route("/menu")
def menu():
    total = len(MENU)
    avg_price = sum(m["price"] for m in MENU) / total if total else 0
    available_count = sum(1 for m in MENU if m["available"])
    return render_template(
        "menu.html",
        menu=MENU,
        total=total,
        avg_price=avg_price,
        available_count=available_count,
    )


if __name__ == "__main__":
    app.run(debug=True)