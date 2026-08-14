def get_product_shape(product_name):
    name = product_name.lower().strip()

    shapes = {
        "milk": "milk.svg",
        "eggs": "eggs.svg",
        "egg": "eggs.svg",
        "cheese": "cheese.svg",
        "butter": "butter.svg",
        "yogurt": "yogurt.svg",
        "chicken": "chicken.svg",
        "sausage": "sausage.svg",
        "tomato": "tomato.svg",
        "tomatoes": "tomato.svg",
        "cucumber": "cucumber.svg",
        "cucumbers": "cucumber.svg",
        "carrot": "carrot.svg",
        "carrots": "carrot.svg",
        "potato": "potato.svg",
        "potatoes": "potato.svg",
        "onion": "onion.svg",
        "onions": "onion.svg",
        "bell pepper": "bell_pepper.svg",
        "bell peppers": "bell_pepper.svg",
        "apple": "apple.svg",
        "apples": "apple.svg",
        "banana": "banana.svg",
        "bananas": "banana.svg",
        "orange": "orange.svg",
        "oranges": "orange.svg",
        "bread": "bread.svg",
        "ketchup": "ketchup.svg",
        "water": "water.svg",
        "juice": "juice.svg",
    }

    return shapes.get(name, "default.svg")