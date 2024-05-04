from django.db.models.signals import post_save
from django.dispatch import receiver
from sf_cafe.order.models import Order, OrderDetail
from django.core.exceptions import ValidationError

from django.db.models import F

processed_orders = {}

@receiver(post_save, sender=Order)
def update_inventory_available_quantity(sender, instance, created, **kwargs):
    if instance.pk in processed_orders:
        return

    if not instance.payied_at:
        return
    
    order_details = OrderDetail.objects.filter(order=instance)
    for detail in order_details:
        menu_item = detail.menu_item
        inventory = menu_item.inventory
        if not inventory:
            continue

        if not inventory.available_quantity >= detail.quantity:
            raise ValidationError(f"The quantity available for {menu_item.name} is not enough.")

        inventory.available_quantity = F('available_quantity') - detail.quantity
        inventory.save()

    processed_orders[instance.pk] = True


@receiver(post_save, sender=OrderDetail)
def check_product_availability(sender, instance, created, **kwargs):
    menu_item = instance.menu_item
    inventory = menu_item.inventory
    if not inventory:
        instance.delete()
        raise ValidationError("O produto não possui estoque.")

    if inventory.available_quantity < instance.quantity:
        instance.delete()
        raise ValidationError(f"A quantidade disponível para {menu_item.name} não é suficiente.")