"""project_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path

from apps.products_app.views import pages_products
from apps.users_app.views import pages

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


# ...

urlpatterns = [
    # YOUR PATTERNS
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("user-gestion/", include("apps.users_app.urls")),
    path("product-gestion/", include("apps.products_app.urls")),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("index/", login_required(pages.index), name="index"),
    path("usuarios/", login_required(pages.usuarios), name="usuarios"),
    path("area/", login_required(pages.area), name="area"),
    path(
        "responsability/", login_required(pages.responsability), name="responsability"
    ),
    path(
        "classification/",
        login_required(pages_products.classification),
        name="classification",
    ),
    path(
        "destination/",
        login_required(pages_products.destination),
        name="destination",
    ),
    path(
        "entity/",
        login_required(pages_products.entity),
        name="entity",
    ),
    path(
        "munit/",
        login_required(pages_products.munit),
        name="munit",
    ),
    path(
        "plans/",
        login_required(pages_products.plans),
        name="plans",
    ),
    path(
        "individualpackaging/",
        login_required(pages_products.individualpackaging),
        name="individualpackaging",
    ),
    path(
        "groupingpackaging/",
        login_required(pages_products.groupingpackaging),
        name="groupingpackaging",
    ),
    path(
        "product/",
        login_required(pages_products.product),
        name="product",
    ),
    path(
        "production/",
        login_required(pages_products.production),
        name="production",
    ),
    path("", pages.first_login, name="first_login"),
    path("__debug__/", include("debug_toolbar.urls")),
]

# This is for serving media on development stages
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
