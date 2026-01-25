# Generated migration for changing image_url from URLField to CharField

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('values', '0015_add_vow_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image_url',
            field=models.CharField(blank=True, help_text='Image URL or path (e.g., /media/Weapons/Item.png)', max_length=500),
        ),
    ]
