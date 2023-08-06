from rest_framework.routers import APIRootView
from .. import filters
from ..models import Number, Trunk, UCUCCluster, DevicePool
from netbox.api.views import ModelViewSet
from . import serializers


class UCBoxPluginRootView(APIRootView):
    """
    ucbox_plugin API root view
    """
    def get_view_name(self):
        return 'UCBox'


class NumberViewSet(ModelViewSet):
    queryset = Number.objects.prefetch_related('tenant', 'region', 'tags')
    serializer_class = serializers.NumberSerializer
    filterset_class = filters.NumberFilterSet

class TrunkViewSet(ModelViewSet):
    queryset = Trunk.objects.prefetch_related('tenant', 'region', 'tags')
    serializer_class = serializers.TrunkSerializer
    filterset_class = filters.TrunkFilterSet

class UCUCClusterViewSet(ModelViewSet):
    queryset = UCUCCluster.objects.prefetch_related('tenant', 'tags')
    serializer_class = serializers.UCUCClusterSerializer
    filterset_class = filters.UCUCClusterFilterSet

class DevicePoolViewSet(ModelViewSet):
    queryset = DevicePool.objects.prefetch_related('tenant', 'region', 'tags')
    serializer_class = serializers.DevicePoolSerializer
    filterset_class = filters.DevicePoolFilterSet