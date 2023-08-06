import django_filters
from django.db.models import Q
from circuits.models import Provider
from dcim.models import Region
from tenancy.models import Tenant
from .models import Number, Trunk
from packaging import version
from django.conf import settings

NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)

if NETBOX_CURRENT_VERSION < version.parse("2.11.3"):
    from utilities.filters import BaseFilterSet
    from utilities.filters import TagFilter
else:
    from netbox.filtersets import BaseFilterSet
    from extras.filters import TagFilter


class NumberFilterSet(BaseFilterSet):

    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    number = django_filters.ModelMultipleChoiceFilter(
        field_name='number',
        queryset=Number.objects.all(),
        to_field_name='number',
        label='number',
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        field_name='tenant__id',
        to_field_name='id',
        label='Tenant (id)',
    )
    region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name='region__id',
        to_field_name='id',
        label='Region (id)',
    )
    provider = django_filters.ModelMultipleChoiceFilter(
        queryset=Provider.objects.all(),
        field_name='provider__id',
        to_field_name='id',
        label='Region (id)',
    )
    forward_to = django_filters.ModelMultipleChoiceFilter(
        field_name='forward_to',
        queryset=Number.objects.all(),
        to_field_name='number',
        label='forward_to',
    )
    tag = TagFilter()

    class Meta():
        model = Number
        fields = ('number',)

    def search(self, queryset, number, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(number__icontains=value)
        )



class TrunkFilterSet(BaseFilterSet):

    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    number = django_filters.ModelMultipleChoiceFilter(
        field_name='trunk',
        queryset=Trunk.objects.all(),
        to_field_name='trunk',
        label='trunk',
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        field_name='tenant__id',
        to_field_name='id',
        label='Tenant (id)',
    )
    region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name='region__id',
        to_field_name='id',
        label='Region (id)',
    )
    provider = django_filters.ModelMultipleChoiceFilter(
        queryset=Provider.objects.all(),
        field_name='provider__id',
        to_field_name='id',
        label='Region (id)',
    )
    destination = django_filters.ModelMultipleChoiceFilter(
        field_name='destination',
        queryset=Trunk.objects.all(),
        to_field_name='destination',
        label='destination',
    )
    tag = TagFilter()

    class Meta():
        model = Trunk
        fields = ('trunk',)

    def search(self, queryset, trunk, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(trunk__icontains=value)
        )
