from django.shortcuts import render, redirect
from .models import FridgeItem, Fridge, Product
from django.views import View
from user.ai_utils import analyze_media
from .additional_func import get_product_shape

class FridgeCreateView(View):
    def post(self, request):
        name = request.POST.get("name")
        quantity = request.POST.get("quantity", 1)

        if not request.user.is_authenticated:
            return redirect("login")

        fridge, created = Fridge.objects.get_or_create(user=request.user)

        product = Product.objects.create(
            fridge=fridge,
            name=name,
            quantity=quantity,
            model_2d=get_product_shape(name)
        )

        return render(
            request,
            "fridge/my_fridge.html",
            {"product": product}
        )

class FridgesView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request,"fridge/smartfridges.html",{"new_user": True})

        fridge, created = Fridge.objects.get_or_create(user=request.user)

        products = fridge.products.all()

        return render(request, "fridge/smartfridges.html",
            {
                "new_user": not products.exists(),
                "products": products,
                "fridge": fridge
            }
        )

    def post(self, request):
        
        if not request.user.is_authenticated:
            return redirect("login")

        file = request.FILES.get("file")

        if not file:
            return render(request,"fridge/smartfridges.html",
                {"error": "File not selected"})

        products = analyze_media(file)

        fridge, created = Fridge.objects.get_or_create(
            user=request.user
        )

        fridge.products.all().delete()

        for product in products:
            name = product.get("name")
            quantity = product.get("quantity", 1)

            if name and name.strip():

                name = name.strip()

                Product.objects.create(
                    fridge=fridge,
                    name=name,
                    quantity=quantity,
                    model_2d=get_product_shape(name)
                )

        return redirect("smart-fridge") 