# Generated migration for adding vow images

from django.db import migrations
import os


def add_vow_images(apps, schema_editor):
    """Add images to vow items from media/Vows folder"""
    Item = apps.get_model('values', 'Item')
    Category = apps.get_model('values', 'Category')
    
    # Ensure vows category exists
    vows_category, created = Category.objects.get_or_create(
        slug='vows',
        defaults={
            'name': 'Vows',
            'description': 'Binding Vows and special abilities',
            'color': '#9333EA'  # Purple color for vows
        }
    )
    
    # Map of vow image filenames to item names
    # Remove .png extension and replace underscores with spaces
    vow_images = {
        'Blood_Beam': 'Blood Beam',
        'Ceaseless_Slashes': 'Ceaseless Slashes',
        'Impact': 'Impact',
        'Justice': 'Justice',
        'Red_Reflection': 'Red Reflection',
        'Snow_Graves': 'Snow Graves',
        'Spatial_Pulvarize': 'Spatial Pulverize',  # Note: might be "Pulverize" typo
        'Swap_Onslaught': 'Swap Onslaught',
        'The_Unbreakable': 'The Unbreakable',
    }
    
    # Update items with vow images
    for filename, item_name in vow_images.items():
        image_path = f'/media/Vows/{filename}.png'
        
        # Try to find the item by name (case-insensitive)
        items = Item.objects.filter(name__iexact=item_name)
        
        if items.exists():
            item = items.first()
            item.image_url = image_path
            item.category = vows_category
            item.save(update_fields=['image_url', 'category'])
            print(f'Updated {item.name} with image {image_path}')
        else:
            # Try with variations (e.g., without "The", with different spacing)
            alt_names = [
                item_name.replace('_', ' '),
                item_name.replace('_', '-'),
                item_name.title(),
            ]
            
            found = False
            for alt_name in alt_names:
                items = Item.objects.filter(name__icontains=alt_name)
                if items.exists():
                    item = items.first()
                    item.image_url = image_path
                    item.category = vows_category
                    item.save(update_fields=['image_url', 'category'])
                    print(f'Updated {item.name} with image {image_path}')
                    found = True
                    break
            
            if not found:
                print(f'Warning: Could not find item for {item_name}')


def reverse_vow_images(apps, schema_editor):
    """Remove vow images"""
    Item = apps.get_model('values', 'Item')
    
    # Clear image_url for items with Vows images
    Item.objects.filter(image_url__startswith='/media/Vows/').update(image_url='')


class Migration(migrations.Migration):

    dependencies = [
        ('values', '0014_valuechangerequest'),
    ]

    operations = [
        migrations.RunPython(add_vow_images, reverse_vow_images),
    ]
