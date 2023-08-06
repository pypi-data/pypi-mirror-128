from typing import List, Type

import graphene
from django.db import models
from django_filters import OrderingFilter
from django_filters.fields import BaseCSVField
from django_filters.widgets import BaseCSVWidget

DEFAULT_SORT_FIELD = "id"


class SortWidget(BaseCSVWidget):
    """Sort widget."""

    def value_from_datadict(self, data, files, name):  # noqa: WPS110
        """Parse data from graphql."""
        sort_value = data.get(name)

        if sort_value is not None:
            if sort_value == "":  # empty value should parse as an empty list
                return []
            elif isinstance(sort_value, list):
                return sort_value
            return sort_value.split(",")
        return None


class SortField(BaseCSVField):
    """Custom sort field for overriding default."""

    widget = SortWidget


class SortHandler(OrderingFilter):
    """Custom ordering filter."""

    base_field_class = SortField

    def __init__(
        self,
        enum: Type[graphene.Enum],
        *args,
        **kwargs,
    ) -> None:
        """Init ordering filter."""
        self.enum = enum
        kwargs["fields"] = self._build_fields(enum)
        super().__init__(*args, **kwargs)

    def filter(  # noqa: A003 WPS125
        self,
        queryset,
        ordering_fields,
    ) -> models.QuerySet:
        """Ordering queryset by fields."""
        ordering_fields = ordering_fields or []

        if not ordering_fields:
            ordering_fields = self._get_model_ordering(queryset.model)

        ordering_fields = self._adjust_default_sort(ordering_fields)

        return super().filter(queryset, ordering_fields)

    def _build_fields(self, enum: Type[graphene.Enum]):
        fields = {DEFAULT_SORT_FIELD}

        if enum:
            for enum_item in list(enum._meta.enum):  # noqa: WPS437
                fields.add(enum_item.value.strip("-"))

        return set(fields)

    def _get_model_ordering(self, model: models.Model) -> List[str]:
        """Get default ordering for model."""
        return (
            list(model._meta.ordering)  # noqa: WPS437
            if model._meta.ordering  # noqa: WPS437
            else []
        )

    def _adjust_default_sort(self, ordering: List[str]) -> List[str]:
        """Append ordering field."""
        default_exists = any(
            field.strip("-") == DEFAULT_SORT_FIELD for field in ordering
        )
        if default_exists:
            return ordering

        return [*ordering, "-{0}".format(DEFAULT_SORT_FIELD)]
