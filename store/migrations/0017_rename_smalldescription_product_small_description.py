# Generated by Django 5.1.2 on 2024-11-21 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_alter_profile_old_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='smalldescription',
            new_name='small_description',
        ),
    ]