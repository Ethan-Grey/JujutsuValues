from django.db import migrations
import os


def update_rarity_from_images(apps, schema_editor):
    Item = apps.get_model("values", "Item")
    
    # Map image filename patterns to rarity values
    # Note: "Unique" and "Legendary" are mapped to "rare" since they're not in our rarity choices
    rarity_mapping = {
        "Unobtainable": "unobtainable",
        "Uobtainable": "unobtainable",  # Handle typo in some filenames
        "SpecialGrade": "special_grade",
        "Special_Grade": "special_grade",
        "Unique": "rare",  # Map Unique to rare
        "Legendary": "rare",  # Map Legendary to rare
    }
    
    # Get all items with images
    items = Item.objects.exclude(image_url="").exclude(image_url__isnull=True)
    
    for item in items:
        if item.image_url:
            # Extract filename from image_url (e.g., "/media/Armor/Item_Name_Unobtainable.png")
            filename = os.path.basename(item.image_url)
            
            # Check for rarity indicators in filename
            for pattern, rarity_value in rarity_mapping.items():
                if pattern in filename:
                    # Check if current rarity doesn't match
                    if item.rarity != rarity_value:
                        item.rarity = rarity_value
                        item.save(update_fields=["rarity"])
                    break


class Migration(migrations.Migration):
    dependencies = [
        ("values", "0011_move_items_to_armor_and_split"),
    ]

    operations = [
        migrations.RunPython(update_rarity_from_images, migrations.RunPython.noop),
    ]
