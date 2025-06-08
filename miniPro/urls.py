from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from posts.views import PostViewSet
from animes.views import AnimeViewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="MiniPro API",
        default_version="v1",
        description="API documentation for MiniPro project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="zeiny.cheikh.dev@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)


router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"animes", AnimeViewSet, basename="anime")

urlpatterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui(
        "redoc",
        cache_timeout=0),
        name="schema-redoc"
        ),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]


urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
