from rest_framework import filters


class IngredientFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        name = request.query_params.get("name")
        if name:
            return queryset.filter(name__istartswith=name)
        return queryset
