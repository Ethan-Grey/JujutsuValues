from django.db import migrations
from django.utils.text import slugify


def fix_items(apps, schema_editor):
    Category = apps.get_model("values", "Category")
    Item = apps.get_model("values", "Item")

    # Get categories
    titles_cat = Category.objects.get(slug="titles")
    weapons_cat = Category.objects.get(slug="weapons")

    # Fix Finger Collector - change to Titles
    try:
        finger_collector = Item.objects.get(name="Finger Collector")
        finger_collector.category = titles_cat
        finger_collector.item_type = "title"
        finger_collector.save()
    except Item.DoesNotExist:
        pass

    # Split Sword of Lapse Blue and Red
    try:
        sword_combo = Item.objects.get(name="Sword of Lapse (Blue) / Red Reversal")
        # Create Sword of Lapse Blue (keep existing)
        sword_blue, created = Item.objects.update_or_create(
            name="Sword of Lapse (Blue)",
            defaults={
                "slug": slugify("Sword of Lapse (Blue)"),
                "category": weapons_cat,
                "item_type": "item",
                "rarity": sword_combo.rarity,
                "value": sword_combo.value,
                "demand": sword_combo.demand,
                "trend": sword_combo.trend,
                "is_limited": sword_combo.is_limited,
                "featured": sword_combo.featured,
                "obtained_from": sword_combo.obtained_from,
                "notes": sword_combo.notes.replace("(Blue) / Red Reversal", "(Blue)"),
                "image_url": "/media/Weapons/Sword_Of_Lapse_Blue.png",
            },
        )
        # Create Sword of Lapse Red
        sword_red, created = Item.objects.update_or_create(
            name="Sword of Lapse (Red)",
            defaults={
                "slug": slugify("Sword of Lapse (Red)"),
                "category": weapons_cat,
                "item_type": "item",
                "rarity": sword_combo.rarity,
                "value": sword_combo.value,
                "demand": sword_combo.demand,
                "trend": sword_combo.trend,
                "is_limited": sword_combo.is_limited,
                "featured": sword_combo.featured,
                "obtained_from": sword_combo.obtained_from,
                "notes": sword_combo.notes.replace("(Blue) / Red Reversal", "(Red)"),
                "image_url": "/media/Weapons/Sword_Of_Lapse_Red.png",
            },
        )
        # Delete the old combined item
        sword_combo.delete()
    except Item.DoesNotExist:
        pass

    # Split Feathered Spear and Jet Black Blade
    try:
        spear_combo = Item.objects.get(name="Feathered Spear / Jet Black Blade")
        # Create Feathered Spear
        feathered_spear, created = Item.objects.update_or_create(
            name="Feathered Spear",
            defaults={
                "slug": slugify("Feathered Spear"),
                "category": weapons_cat,
                "item_type": "item",
                "rarity": spear_combo.rarity,
                "value": spear_combo.value,
                "demand": spear_combo.demand,
                "trend": spear_combo.trend,
                "is_limited": spear_combo.is_limited,
                "featured": spear_combo.featured,
                "obtained_from": spear_combo.obtained_from,
                "notes": spear_combo.notes.replace("Feathered Spear / Jet Black Blade", "Feathered Spear"),
                "image_url": "/media/Weapons/Feathered_Spear.png",
            },
        )
        # Create Jet Black Blade
        jet_black, created = Item.objects.update_or_create(
            name="Jet Black Blade",
            defaults={
                "slug": slugify("Jet Black Blade"),
                "category": weapons_cat,
                "item_type": "item",
                "rarity": spear_combo.rarity,
                "value": spear_combo.value,
                "demand": spear_combo.demand,
                "trend": spear_combo.trend,
                "is_limited": spear_combo.is_limited,
                "featured": spear_combo.featured,
                "obtained_from": spear_combo.obtained_from,
                "notes": spear_combo.notes.replace("Feathered Spear / Jet Black Blade", "Jet Black Blade"),
                "image_url": "/media/Weapons/Jet_Black_Blade.png",
            },
        )
        # Delete the old combined item
        spear_combo.delete()
    except Item.DoesNotExist:
        pass


class Migration(migrations.Migration):
    dependencies = [
        ("values", "0005_encode_media_paths"),
    ]

    operations = [
        migrations.RunPython(fix_items, migrations.RunPython.noop),
    ]
