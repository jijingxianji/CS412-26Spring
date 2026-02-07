import time
from django.shortcuts import render, redirect

# --- Pizza flavors ---
PIZZAS = [
    {"id": "pepperoni", "name": "Pepperoni Pizza"},
    {"id": "margherita", "name": "Margherita Pizza"},
    {"id": "hawaiian", "name": "Hawaiian Pizza"},
    {"id": "bbq_chicken", "name": "BBQ Chicken Pizza"},
]

# pricing for size
PIZZA_PRICES = {
    "slice": 4.50,
    "whole": 18.00,
}

# --- Toppings (extra) ---
TOPPINGS = [
    {"id": "extra_cheese", "name": "Extra cheese", "price": 1.50},
    {"id": "mushrooms", "name": "Mushrooms", "price": 1.00},
    {"id": "olives", "name": "Olives", "price": 1.00},
    {"id": "jalapenos", "name": "Jalapeños", "price": 1.00},
    {"id": "pepperoni_extra", "name": "Extra pepperoni", "price": 1.50},
]

# --- Desserts ---
DESSERTS = [
    {"id": "pudding", "name": "Pudding", "price": 4.00},
    {"id": "vanilla_ice", "name": "Vanilla ice cream", "price": 3.50},
    {"id": "matcha_ice", "name": "Matcha ice cream", "price": 4.00},
    {"id": "brownie", "name": "Brownie cake", "price": 4.50},
]

# --- Drinks ---
DRINKS = [
    {"id": "lemonade", "name": "Lemonade", "price": 3.00},
    {"id": "coke", "name": "Coca-Cola", "price": 2.50},
    {"id": "boba", "name": "Brown sugar boba milk tea", "price": 5.50},
    {"id": "strawberry", "name": "Strawberry smoothie", "price": 5.00},
    {"id": "passionfruit", "name": "Passionfruit smoothie", "price": 5.00},
]

# ---Daily Special ---
DAILY_SPECIALS = [
    {"name": "Garlic knots (6 pcs)", "price": 5.00, "desc": "Fresh baked knots with garlic butter."},
    {"name": "Tiramisu cup", "price": 5.50, "desc": "Coffee-flavored dessert cup."},
    {"name": "Spicy wings (6 pcs)", "price": 7.50, "desc": "Crispy wings with spicy sauce."},
]


# For pizzas, we use a dropdown per flavor:
PIZZA_SELECT_VALUES = [
    ("none", "0"),
    ("slice", "1 slice"),
    ("whole", "1 whole pizza"),
]


def main(request):
    context = {
        "name": "Yan’s Pizza",
        "location": "Boston, MA (pickup only)",
        "hours": [
            ("Mon–Fri", "11:00 AM – 9:00 PM"),
            ("Sat", "12:00 PM – 8:00 PM"),
            ("Sun", "12:00 PM – 8:00 PM"),
        ],
        # Replace these with pizza-only images (see below)
        "photos": [
            "https://images.unsplash.com/photo-1494346480775-936a9f0d0877?q=80&w=1632&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=1400&q=60",
            "https://images.unsplash.com/photo-1590947132387-155cc02f3212?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        ],
    }
    return render(request, "restaurant/main.html", context)


def order(request):

    import random
    special = random.choice(DAILY_SPECIALS)
    request.session["daily_special"] = special

    context = {
        "pizzas": PIZZAS,
        "pizza_select_values": PIZZA_SELECT_VALUES,
        "pizza_prices": PIZZA_PRICES,
        "toppings": TOPPINGS,
        "desserts": DESSERTS,
        "drinks": DRINKS,
        "special": special,
    }
    return render(request, "restaurant/order.html", context)


def confirmation(request):
    import random
    import time

    if request.method != "POST":
        return redirect("restaurant_root")

    total = 0.0
    ordered = []

    # pizzas (你当前如果是 dropdown 版本：pizza_<id> = slice/whole/none)
    for p in PIZZAS:
        key = f"pizza_{p['id']}"
        choice = request.POST.get(key, "none")
        if choice in ("slice", "whole"):
            price = PIZZA_PRICES[choice]
            label = " (1 slice)" if choice == "slice" else " (1 whole)"
            ordered.append({"name": p["name"] + label, "price": price})
            total += price

    # toppings
    topping_by_id = {t["id"]: t for t in TOPPINGS}
    selected_toppings = []
    for tid in request.POST.getlist("toppings"):
        if tid in topping_by_id:
            t = topping_by_id[tid]
            selected_toppings.append({"name": t["name"], "price": t["price"]})
            total += float(t["price"])

    # desserts
    dessert_by_id = {d["id"]: d for d in DESSERTS}
    selected_desserts = []
    for did in request.POST.getlist("desserts"):
        if did in dessert_by_id:
            d = dessert_by_id[did]
            selected_desserts.append({"name": d["name"], "price": d["price"]})
            total += float(d["price"])

    # drinks
    drink_by_id = {d["id"]: d for d in DRINKS}
    selected_drinks = []
    for did in request.POST.getlist("drinks"):
        if did in drink_by_id:
            d = drink_by_id[did]
            selected_drinks.append({"name": d["name"], "price": d["price"]})
            total += float(d["price"])

    # daily special (checkbox name="daily_special" value="yes")
    special_ordered = None
    special = request.session.get("daily_special")
    if request.POST.get("daily_special") == "yes" and special:
        special_ordered = special
        total += float(special["price"])

    customer = {
        "name": request.POST.get("customer_name", "").strip(),
        "phone": request.POST.get("customer_phone", "").strip(),
        "email": request.POST.get("customer_email", "").strip(),
        "instructions": request.POST.get("instructions", "").strip(),
    }

    minutes = random.randint(30, 60)
    ready_ts = time.time() + minutes * 60
    ready_time = time.strftime("%I:%M %p", time.localtime(ready_ts))

    return render(request, "restaurant/confirmation.html", {
        "ordered": ordered,
        "toppings": selected_toppings,
        "desserts": selected_desserts,
        "drinks": selected_drinks,
        "special_ordered": special_ordered,
        "customer": customer,
        "total": f"{total:.2f}",
        "ready_time": ready_time,
        "ready_minutes": minutes,
    })
