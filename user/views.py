from django.shortcuts import render
from django.views import View

class Mainpageview(View):
    def get(self, request):
      return render(request, 'user/mainpage.html')


class FridgesView(View):
    def get(self, request):
        return render(request, 'user/smartfridges.html')


class MarketsView(View):
    def get(self, request):
        return render(request, 'user/markets.html')


class RecipiesView(View):
    def get(self, request):
        return render(request, 'user/recipies.html')


class MyHealthView(View):
    def get(self, request):
        return render(request, 'user/myhealth.html')
