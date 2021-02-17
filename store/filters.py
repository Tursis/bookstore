from rest_framework.filters import BaseFilterBackend

class CatalogFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        print('hello')
        queryset = queryset.order_by('attribute__sortmetric')
        return queryset