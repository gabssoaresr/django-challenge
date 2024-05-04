from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderDetail


@receiver(post_save, sender=OrderDetail)
def update_order_total(sender, instance, created, **kwargs):
    if created or instance.order_id:
        order = instance.order
        total_order_cents = sum(detail.menu_item.price * detail.quantity for detail in order.orderdetail_set.all())
        order.total_order = total_order_cents
        order.save()