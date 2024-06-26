# Generated by Django 5.0.4 on 2024-05-04 21:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('menu_items', '0001_initial'),
        ('order', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='menu_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu_items.menuitem'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order'),
        ),
    ]
