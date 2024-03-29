from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views import View

from shared.permissions import PERMISSION_ON_SITE
from .store_statistics import get_quantity_of_product_sold
from .models import ViewStatistics


class StatisticsView(PermissionRequiredMixin, View):
    permission_required = PERMISSION_ON_SITE['moderator']

    def get(self, request):
        return render(request, 'dashboard/statistics_detail.html',
                      context={'get_quantity_of_product_sold': get_quantity_of_product_sold(),
                               'get_views_product_statistics': ViewStatistics.objects.all()})
