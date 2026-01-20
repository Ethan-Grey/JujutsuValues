from django.db import migrations
from django.utils.text import slugify


def move_items_and_split(apps, schema_editor):
    Category = apps.get_model("values", "Category")
    Item = apps.get_model("values", "Item")

    armor_cat = Category.objects.get(slug="armor")
    items_cat = Category.objects.get(slug="items")

    # Move items from Items to Armor
    items_to_move = [
        "Tactful Ring",
        "Rotten Ring",
        "Enlightenment Beads",
        "Rotten Chains",
        "Blackhole Buddy / Nascent Cosmic Gear",
    ]

    for item_name in items_to_move:
        try:
            item = Item.objects.get(name=item_name)
            item.category = armor_cat
            item.save()
        except Item.DoesNotExist:
            pass

    # Split Blackhole Buddy / Nascent Cosmic Gear into 3 items
    try:
        combo_item = Item.objects.get(name="Blackhole Buddy / Nascent Cosmic Gear")
        
        # Create Blackhole Buddy
        Item.objects.update_or_create(
            name="Blackhole Buddy",
            defaults={
                "slug": slugify("Blackhole Buddy"),
                "category": armor_cat,
                "item_type": combo_item.item_type,
                "rarity": combo_item.rarity,
                "value": combo_item.value,
                "demand": combo_item.demand,
                "trend": combo_item.trend,
                "is_limited": combo_item.is_limited,
                "featured": combo_item.featured,
                "obtained_from": combo_item.obtained_from,
                "notes": combo_item.notes.replace("Blackhole Buddy / Nascent Cosmic Gear", "Blackhole Buddy"),
                "image_url": "/media/Armor/Blackhole_Buddy_Unobtainable.png",
            },
        )
        
        # Create Nascent Cosmic Cloak
        Item.objects.update_or_create(
            name="Nascent Cosmic Cloak",
            defaults={
                "slug": slugify("Nascent Cosmic Cloak"),
                "category": armor_cat,
                "item_type": combo_item.item_type,
                "rarity": combo_item.rarity,
                "value": combo_item.value,
                "demand": combo_item.demand,
                "trend": combo_item.trend,
                "is_limited": combo_item.is_limited,
                "featured": combo_item.featured,
                "obtained_from": combo_item.obtained_from,
                "notes": combo_item.notes.replace("Blackhole Buddy / Nascent Cosmic Gear", "Nascent Cosmic Cloak"),
                "image_url": "/media/Armor/Nascent_Cosmic_Cloak_Legendary.png",
            },
        )
        
        # Create Nascent Cosmic Scarf
        Item.objects.update_or_create(
            name="Nascent Cosmic Scarf",
            defaults={
                "slug": slugify("Nascent Cosmic Scarf"),
                "category": armor_cat,
                "item_type": combo_item.item_type,
                "rarity": combo_item.rarity,
                "value": combo_item.value,
                "demand": combo_item.demand,
                "trend": combo_item.trend,
                "is_limited": combo_item.is_limited,
                "featured": combo_item.featured,
                "obtained_from": combo_item.obtained_from,
                "notes": combo_item.notes.replace("Blackhole Buddy / Nascent Cosmic Gear", "Nascent Cosmic Scarf"),
                "image_url": "/media/Armor/Nascent_Cosmic_Scarf_Legendary.png",
            },
        )
        
        combo_item.delete()
    except Item.DoesNotExist:
        pass

    # Split Imaginary King / Aetherion / Phantasis / Impera
    try:
        combo_item = Item.objects.get(name="Imaginary King / Aetherion / Phantasis / Impera")
        
        items_to_create = [
            ("Imaginary King", "Imaginary_King_Unique.png"),
            ("Aetherion", "Aetherion_Unique.png"),
            ("Phantasis", "Phantasis_Unique.png"),
            ("Impera", "Impera_Unique.png"),
        ]
        
        for name, image_file in items_to_create:
            Item.objects.update_or_create(
                name=name,
                defaults={
                    "slug": slugify(name),
                    "category": armor_cat,
                    "item_type": combo_item.item_type,
                    "rarity": combo_item.rarity,
                    "value": combo_item.value,
                    "demand": combo_item.demand,
                    "trend": combo_item.trend,
                    "is_limited": combo_item.is_limited,
                    "featured": combo_item.featured,
                    "obtained_from": combo_item.obtained_from,
                    "notes": combo_item.notes.replace("Imaginary King / Aetherion / Phantasis / Impera", name),
                    "image_url": f"/media/Armor/{image_file}",
                },
            )
        
        combo_item.delete()
    except Item.DoesNotExist:
        pass

    # Split Fragments (Reversal/Lapse)
    try:
        combo_item = Item.objects.get(name="Fragments (Reversal/Lapse)")
        
        Item.objects.update_or_create(
            name="Fragment Reversal",
            defaults={
                "slug": slugify("Fragment Reversal"),
                "category": armor_cat,
                "item_type": combo_item.item_type,
                "rarity": combo_item.rarity,
                "value": combo_item.value,
                "demand": combo_item.demand,
                "trend": combo_item.trend,
                "is_limited": combo_item.is_limited,
                "featured": combo_item.featured,
                "obtained_from": combo_item.obtained_from,
                "notes": combo_item.notes.replace("Fragments (Reversal/Lapse)", "Fragment Reversal"),
                "image_url": "/media/Armor/Fragment_Reversal_SpecialGrade.png",
            },
        )
        
        Item.objects.update_or_create(
            name="Fragment Lapse",
            defaults={
                "slug": slugify("Fragment Lapse"),
                "category": armor_cat,
                "item_type": combo_item.item_type,
                "rarity": combo_item.rarity,
                "value": combo_item.value,
                "demand": combo_item.demand,
                "trend": combo_item.trend,
                "is_limited": combo_item.is_limited,
                "featured": combo_item.featured,
                "obtained_from": combo_item.obtained_from,
                "notes": combo_item.notes.replace("Fragments (Reversal/Lapse)", "Fragment Lapse"),
                "image_url": "/media/Armor/Fragment_Lapse_SpecialGrade.png",
            },
        )
        
        combo_item.delete()
    except Item.DoesNotExist:
        pass

    # Split Celestia / Dynesis / Helkytis
    try:
        combo_item = Item.objects.get(name="Celestia / Dynesis / Helkytis")
        
        items_to_create = [
            ("Celestia", "Celestia_SpecialGrade.png"),
            ("Dynesis", "Dynesis_SpecialGrade.png"),
            ("Helkytis", "Helkytis_SpecialGrade.png"),
        ]
        
        for name, image_file in items_to_create:
            Item.objects.update_or_create(
                name=name,
                defaults={
                    "slug": slugify(name),
                    "category": armor_cat,
                    "item_type": combo_item.item_type,
                    "rarity": combo_item.rarity,
                    "value": combo_item.value,
                    "demand": combo_item.demand,
                    "trend": combo_item.trend,
                    "is_limited": combo_item.is_limited,
                    "featured": combo_item.featured,
                    "obtained_from": combo_item.obtained_from,
                    "notes": combo_item.notes.replace("Celestia / Dynesis / Helkytis", name),
                    "image_url": f"/media/Armor/{image_file}",
                },
            )
        
        combo_item.delete()
    except Item.DoesNotExist:
        pass

    # Split Ragna / Crowns / Snake Masks
    try:
        combo_item = Item.objects.get(name="Ragna / Crowns / Snake Masks")
        
        items_to_create = [
            ("Ragna", "Ragna_SpecialGrade.png"),
            ("Crown of Azure", "Crown_Of_Azure_SpecialGrade.png"),
            ("Crown of Crimson", "Crown_Of_Crimson_SpecialGrade.png"),
            ("Red Mask of the Snake", "Red_Mask_Of_The_Snake_Unobtainable.png"),
            ("Black Mask of the Snake", "Black_Mask_Of_The_Snake_Unobtainable.png"),
        ]
        
        for name, image_file in items_to_create:
            Item.objects.update_or_create(
                name=name,
                defaults={
                    "slug": slugify(name),
                    "category": armor_cat,
                    "item_type": combo_item.item_type,
                    "rarity": combo_item.rarity,
                    "value": combo_item.value,
                    "demand": combo_item.demand,
                    "trend": combo_item.trend,
                    "is_limited": combo_item.is_limited,
                    "featured": combo_item.featured,
                    "obtained_from": combo_item.obtained_from,
                    "notes": combo_item.notes.replace("Ragna / Crowns / Snake Masks", name),
                    "image_url": f"/media/Armor/{image_file}",
                },
            )
        
        combo_item.delete()
    except Item.DoesNotExist:
        pass

    # Split Suit/Trousers of Fortune
    try:
        combo_item = Item.objects.get(name="Suit/Trousers of Fortune")
        
        Item.objects.update_or_create(
            name="Suit of Fortune",
            defaults={
                "slug": slugify("Suit of Fortune"),
                "category": armor_cat,
                "item_type": combo_item.item_type,
                "rarity": combo_item.rarity,
                "value": combo_item.value,
                "demand": combo_item.demand,
                "trend": combo_item.trend,
                "is_limited": combo_item.is_limited,
                "featured": combo_item.featured,
                "obtained_from": combo_item.obtained_from,
                "notes": combo_item.notes.replace("Suit/Trousers of Fortune", "Suit of Fortune"),
                "image_url": "/media/Armor/Suit_Of_Fortune_SpecialGrade.png",
            },
        )
        
        Item.objects.update_or_create(
            name="Trousers of Fortune",
            defaults={
                "slug": slugify("Trousers of Fortune"),
                "category": armor_cat,
                "item_type": combo_item.item_type,
                "rarity": combo_item.rarity,
                "value": combo_item.value,
                "demand": combo_item.demand,
                "trend": combo_item.trend,
                "is_limited": combo_item.is_limited,
                "featured": combo_item.featured,
                "obtained_from": combo_item.obtained_from,
                "notes": combo_item.notes.replace("Suit/Trousers of Fortune", "Trousers of Fortune"),
                "image_url": "/media/Armor/Trouser_Of_Fortune_SpecialGrade.png",
            },
        )
        
        combo_item.delete()
    except Item.DoesNotExist:
        pass

    # Update images for moved items
    image_updates = {
        "Tactful Ring": "/media/Armor/Tactful_Ring.png",
        "Rotten Ring": "/media/Armor/Rotten_Ring_Special_Grade.png",
        "Enlightenment Beads": "/media/Armor/Enlightenment_Beads_Unobtainable.png",
        "Rotten Chains": "/media/Armor/Rotten_Chains_SpecialGrade.png",
    }

    for item_name, image_path in image_updates.items():
        try:
            item = Item.objects.get(name=item_name)
            item.image_url = image_path
            item.save(update_fields=["image_url"])
        except Item.DoesNotExist:
            pass


class Migration(migrations.Migration):
    dependencies = [
        ("values", "0010_add_remaining_images"),
    ]

    operations = [
        migrations.RunPython(move_items_and_split, migrations.RunPython.noop),
    ]
