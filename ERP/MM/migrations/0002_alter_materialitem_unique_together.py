# Generated by Django 4.0.5 on 2022-08-31 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MM', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='materialitem',
            unique_together={('material', 'stock')},
        ),
    ]
