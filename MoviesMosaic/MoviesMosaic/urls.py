from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static  # <-- import here

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]


# Custom 404 view
def custom_404_view(request, exception):
    return render(request, "404.html", status=404)


handler404 = custom_404_view

# ✅ Serve static files manually when DEBUG = False (for local development or custom error page styling)
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
