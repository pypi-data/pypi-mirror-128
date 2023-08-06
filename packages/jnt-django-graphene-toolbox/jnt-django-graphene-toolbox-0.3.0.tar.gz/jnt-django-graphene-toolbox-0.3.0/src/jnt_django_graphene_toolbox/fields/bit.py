import graphene
from graphene.utils import str_converters


class BitField(graphene.List):
    """Bit field."""

    def __init__(self, enum, *args, **kwargs):
        """
        Initialize.

        Add resolver-wrapper
        """
        self._resolver = kwargs.get("resolver")
        kwargs["resolver"] = self._resolver_wrap
        super().__init__(graphene.Enum.from_enum(enum), *args, **kwargs)

    def _resolver_wrap(self, instance, info):  # noqa: WPS110
        if self._resolver:
            field_value = self._resolver(instance, info)
        else:
            field_value = getattr(
                instance,
                str_converters.to_snake_case(info.field_name),
            )

        return [key for key, setted in field_value if setted]
