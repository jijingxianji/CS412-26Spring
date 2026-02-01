import random
from django.shortcuts import render

items = [
    {
        "text": "The greatest wealth is to live content with little.",
        "author": "Plato",
        "image": "plato.png",
    },
    {
        "text": "The future belongs to those who prepare for it today.",
        "author": "Malcolm X",
        "image": "malcolm_x.jpg",
    },
    {
        "text": "I have no special talent. I am only passionately curious.",
        "author": "Albert Einstein",
        "image": "einstein.jpg",
    },
    {
        "text": "The successful warrior is the average man, with laser-like focus.",
        "author": "Bruce Lee",
        "image": "bruce_lee.jpg",
    },
]

def quote(request):
    item = random.choice(items)
    return render(request, "quotes/quote.html", {"item": item})

def show_all(request):
    return render(request, "quotes/show_all.html", {"items": items})

def about(request):
    return render(request, "quotes/about.html")

