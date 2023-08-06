from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    """Application entry config."""

    name = "jnt_django_graphene_toolbox"
    verbose_name = "Django graphene toolbox"
    default = True
