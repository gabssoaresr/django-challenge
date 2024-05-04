# Generated by Django 5.0.4 on 2024-05-04 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('photo_path', models.CharField(blank=True, max_length=100, null=True)),
                ('ingredients', models.TextField()),
                ('nutritional_information', models.TextField()),
            ],
        ),
    ]
