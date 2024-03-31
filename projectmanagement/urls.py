
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', include('cup.urls')), #the app url are linked here,app is named cup:client+user+project
        # Include the URLs of the Cup app
]

