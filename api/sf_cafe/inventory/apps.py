from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sf_cafe.inventory'

    def ready(self):
        import sf_cafe.inventory.signals