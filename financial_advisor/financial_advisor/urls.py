from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # This prefixes all app urls with /api/
    path("api/", include("financial_advisor_api.urls")),
]
