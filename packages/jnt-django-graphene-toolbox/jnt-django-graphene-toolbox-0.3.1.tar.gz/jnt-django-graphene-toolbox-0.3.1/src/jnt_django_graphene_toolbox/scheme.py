import graphene
from graphene.types import enum, typemap
from graphene.types.definitions import GrapheneGraphQLType
from graphql.type.introspection import IntrospectionSchema


class TypeMap(typemap.TypeMap):
    """Type map."""

    def graphene_reducer(self, map, type):  # noqa: WPS125
        """
        Graphene reducer.

        It is a hack for fix "Found different types with the same name... " in
        enums.
        """
        if isinstance(type, (graphene.List, graphene.NonNull)):
            return super().graphene_reducer(map, type)

        if type._meta.name in map and self._is_enum(map, type):  # noqa: WPS437
            return map

        return super().graphene_reducer(map, type)

    def _is_enum(self, gr_map, gr_type) -> bool:
        return (
            isinstance(
                gr_map[gr_type._meta.name],  # noqa: WPS437
                GrapheneGraphQLType,
            )
            and isinstance(gr_type, enum.EnumMeta)
        )


class Schema(graphene.Schema):
    """Graphene schema."""

    def build_typemap(self):
        """Building typemap."""
        initial_types = [
            self._query,
            self._mutation,
            self._subscription,
            IntrospectionSchema,
        ]
        if self.types:
            initial_types += self.types
        self._type_map = TypeMap(
            initial_types,
            auto_camelcase=self.auto_camelcase,
            schema=self,
        )
