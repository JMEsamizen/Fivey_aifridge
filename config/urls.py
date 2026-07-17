from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('fridge/', include('fridge.urls')),
    # path('market/', include('market.urls')),
]
