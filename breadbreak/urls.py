"""
URL configuration for breadbreak project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import RegisterView, LoginView
from django.core.management import call_command

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('catalog.urls')),
    path('api/', include('orders.urls')),
]

# Optional seed endpoint for dev only
from django.conf import settings
from django.http import JsonResponse

def seed_view(_request):
    call_command('shell', '-c', 'import seed; seed.run()')
    return JsonResponse({"ok": True})

if settings.DEBUG:
    urlpatterns += [path('dev/seed/', seed_view)]
