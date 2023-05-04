from django.contrib import admin
from django.urls import path, include

import api
from api import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api.urls)),
]
