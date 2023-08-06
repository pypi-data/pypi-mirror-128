import sys
from typing import Optional

import graphene
from graphene.types import mutation
from graphql import ResolveInfo

from jnt_django_graphene_toolbox.errors import (
    BaseGraphQLError,
    GraphQLPermissionDenied,
)


class MutationOptions(mutation.MutationOptions):
    """Base mutation options."""

    auth_required = None


class BaseMutation(graphene.Mutation):
    """A base class mutation."""

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(  # noqa: WPS211
        cls,
        auth_required=False,
        _meta=None,
        **options,
    ):
        """Initialize class with meta."""
        if not _meta:
            _meta = MutationOptions(cls)  # noqa: WPS122

        _meta.auth_required = auth_required
        super().__init_subclass_with_meta__(_meta=_meta, **options)

    @classmethod
    def mutate(cls, root, info, **kwargs):  # noqa: WPS110
        """Mutate."""
        if not cls.check_premissions(root, info, **kwargs):
            return GraphQLPermissionDenied()

        try:
            return cls.mutate_and_get_payload(root, info, **kwargs)
        except Exception as err:
            payload = cls.handle_error(root, info, err)
            if payload:
                return payload

            raise

    @classmethod
    def check_premissions(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,  # noqa: WPS125
    ) -> bool:
        """Check permissions."""
        user = info.context.user  # type: ignore
        if cls._meta.auth_required:
            return user.is_authenticated

        return True

    @classmethod
    def handle_error(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110,
        error: Exception,
    ):
        """Handle error."""
        if isinstance(error, BaseGraphQLError):
            error.stack = sys.exc_info()[2]
            return error

    @classmethod
    def mutate_and_get_payload(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110,
        **kwargs,
    ) -> None:  # noqa: WPS110
        """Method should be implemented in subclasses."""
        raise NotImplementedError
