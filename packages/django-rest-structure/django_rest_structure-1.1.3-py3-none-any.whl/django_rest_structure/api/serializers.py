from typing import Tuple
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from rest_framework import serializers

from .validations import StrFieldValidation
from ..results.exception import Err


class BaseSerializer(serializers.Serializer):

    def __init__(self, check_is_valid: bool = True, request: WSGIRequest = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if check_is_valid:
            self.raise_error_if_not_valid()
        self.request = request
        self.user = request.user if hasattr(request, 'user') else None

    def validate(self, attrs: dict) -> dict:
        for k, v in attrs.items():
            if k in self.fields:
                for validator in self.fields[k].validators:
                    if type(validator) in [StrFieldValidation] and validator.ef is not None:
                        attrs[k] = validator.validated_value
        return attrs

    def raise_error_if_not_valid(self):
        if not self.is_valid():
            raise Err(Err.ENTERED_DATA_NOT_VALID, self.errors)

    def create(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass


class BaseListSerializer(BaseSerializer):
    def __init__(self, *args, **kwargs):
        super(BaseListSerializer, self).__init__(*args, **kwargs)

    page = serializers.IntegerField(default=1)
    count = serializers.IntegerField(default=10, max_value=50)

    FILTERS = []

    def paging(self, objects, total_count: int = None) -> Tuple[list, int]:
        total_count = len(objects) if total_count is None else total_count
        paginator = Paginator(objects, self.validated_data['count'])
        try:
            result = paginator.page(self.validated_data['page']).object_list
        except EmptyPage:
            result = []

        return result, total_count

    def get_query_filters(self) -> Q:
        query_filter = Q()
        for key, value, use_not in self.FILTERS:
            if key in self.validated_data:
                query_filter.add(
                    ~self.__get_query_filter_dict(
                        value,
                        self.validated_data[key]
                    ) if use_not else self.__get_query_filter_dict(
                        value,
                        self.validated_data[key]
                    ), Q.AND)
        return query_filter

    @staticmethod
    def __get_query_filter_dict(key, value) -> Q:
        return Q(**{key: value})

    def paging_structure(self, paging_objects: list, total_count: int) -> dict:
        return {
            'list': paging_objects,
            'page': self.validated_data['page'],
            'count_in_page': len(paging_objects),
            'total_count': total_count
        }
