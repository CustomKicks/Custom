# Generated by Django 5.1.2 on 2024-11-07 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_rename_smalldescrption_product_smalldescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.IntegerField(default=0),
        ),
    ]