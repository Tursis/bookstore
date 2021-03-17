from django.shortcuts import render
from django.views import View


class StatisticsView(View):
    def get(self, request):
        return render(request, 'dashboard/statistics_detail.html')