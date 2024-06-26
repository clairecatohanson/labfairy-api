from .equipment import (
    EquipmentCreatedSerializer,
    EquipmentListSerializer,
    EquipmentFullSerializer,
)
from .labequipment import LabEquipmentSerializer
from .equipmentmaintenance import (
    EquipmentMaintenanceSerializer,
    EquipmentMaintenanceDetailsSerializer,
)
from .building import BuildingSerializer
from .room import RoomSerializer
from .location import LocationSerializer
from .lab import LabSerializer
from .maintenance import MaintenanceSerializer
from .user import SuperUserSerializer, UserResearcherSerializer
from .researchequipment import ResearcherEquipmentSerializer
from .inventory import InventorySerializer
from .consumableinventory import (
    ConsumableInventoryListSerializer,
    ConsumableInventoryDetailSerializer,
    ConsumableInventoryBasicSerializer,
)
from .supplyrequest import SupplyRequestSerializer
from .order import OrderSerializer, OrderDetailSerializer
