from django.db import models
from sf_cafe.menu_items.models import MenuItem
from sf_cafe.user.models import User


PAYMENT_CHOICES = [
    ('pix', 'PIX'),
    ('cash', 'Dinheiro'),
    ('debit', 'Débito'),
    ('credit', 'Crédito'),
]


STATUS = [
    ('finished', 'Finished'),
    ('open', 'Open'),
]


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_order = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='open')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='pix', blank=True, null=True,)
    payied_at = models.DateTimeField(blank=True, null=True, verbose_name='Payment Date and Time')

    def get_total_order_float(self):
        if self.total_order:
            return self.total_order / 100
    
    def __str__(self):
        return f"Order {self.id}"

class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    customizations = models.TextField(blank=True, null=True,)

    class Meta:
        verbose_name = 'Order Detail'
        verbose_name_plural = 'Order Details'
