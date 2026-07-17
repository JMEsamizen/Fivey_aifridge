from django.shortcuts import render
from .models import FridgeItem
from django.views import View

class FridgeCreateView(View):
    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
    
        new_fridge = FridgeItem.objects.create(title=title, description=description)
        return render(request, 'fridge/my_fridge.html', {'fridge': new_fridge})