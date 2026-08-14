from django.urls import path
from .views import Mainpageview, MarketsView, RegisterView, LoginView, LogoutView

urlpatterns = [
    path('', Mainpageview.as_view(), name='mainpage'),
    path('markets/', MarketsView.as_view(), name='markets'),
    
#registration
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
