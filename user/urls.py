from django.urls import path
from .views import Mainpageview, FridgesView, MarketsView, RecipiesView, MyHealthView, RegisterView, LoginView, LogoutView, AIAnalyzeView

urlpatterns = [
    path('', Mainpageview.as_view(), name='mainpage'),
    path('smartfridge/', FridgesView.as_view(), name='smart-fridge'),
    path('markets/', MarketsView.as_view(), name='markets'),
    path('recipies/', RecipiesView.as_view(), name='recipies'),
    path('myhealth/', MyHealthView.as_view(), name='my-health'),
#registration
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
#ai
    path("ai/analyze/", AIAnalyzeView.as_view(), name="ai_analyze")
]
