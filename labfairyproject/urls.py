from rest_framework import routers
from django.urls import include, path
from django.contrib import admin
from labfairyapi.views import *


router = routers.DefaultRouter(trailing_slash=False)
router.register(r"equipment", EquipmentViewSet, "equipment")

urlpatterns = [path("", include(router.urls)), path("admin/", admin.site.urls)]
