from django.db import models
from sf_cafe.menu_items.models import MenuItem

class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    menu_item = models.OneToOneField(MenuItem, on_delete=models.CASCADE, related_name='inventory')
    available_quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.menu_item.name} - Available Quantity: {self.available_quantity}"
