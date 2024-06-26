from rest_framework import routers
from django.urls import include, path
from django.contrib import admin
from labfairyapi.views import *


router = routers.DefaultRouter(trailing_slash=False)
router.register(r"equipment", EquipmentViewSet, "equipment")
router.register(r"labequipment", LabEquipmentViewSet, "labequipment")
router.register(r"maintenance", EquipmentMaintenanceViewSet, "equipmentmaintenance")
router.register(r"maintenance_types", MaintenanceViewSet, "maintenance")
router.register(r"buildings", BuildingViewSet, "buildings")
router.register(r"rooms", RoomViewSet, "rooms")
router.register(r"locations", LocationViewSet, "locations")
router.register(r"labs", LabViewSet, "labs")
router.register(r"profile", UserViewSet, "profile")
router.register(r"equipmentrequests", ResearcherEquipmentViewSet, "researcherequipment")
router.register(r"inventories", InventoryViewSet, "inventories")
router.register(
    r"inventoryconsumables", ConsumableInventoryViewSet, "consumableinventories"
)
router.register(r"supplyrequests", SupplyRequestViewSet, "supplyrequests")
router.register(r"orders", OrderViewSet, "orders")
router.register(r"researcher", ResearcherViewSet, "researcher")

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("register", register_user),
    path("login", login_user),
]
