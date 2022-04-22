"""App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # Django JET URLS
    path('jet/', include('jet.urls', 'jet')),
    # Django JET dashboard URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('api/', include(('Users.urls', 'users'), namespace='users')),
    path('api/', include(('Emails.urls', 'emails'), namespace='emails')),
    path(
        'api/password_reset/',
        include('django_rest_passwordreset.urls', namespace='password_reset'),
    ),
    path(
        'api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'
    ),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'doc/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'doc/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    path("", include('django_prometheus.urls'), name='django-prometheus'),
    re_path(
        r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}
    ),
]
