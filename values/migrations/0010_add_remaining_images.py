from django.db import migrations


def add_remaining_images(apps, schema_editor):
    Item = apps.get_model("values", "Item")

    # Additional image mappings for items that might have been missed
    additional_images = {
        # Armor items
        "Eyes Sets (Willpower/Insight/Bloodthirst)": "Armor/Willpower_SpecialGrade.png",  # Using Willpower as default
        "Demonic Outfit Pieces": "Armor/Demonic_Outfit_SpecialGrade.png",
        "Festive Outfit Pieces": "Armor/Festive_Set_Unobtainable.png",
        "Imaginary King / Aetherion / Phantasis / Impera": "Armor/Imaginary_King_Unique.png",  # Using Imaginary King as default
        "Cloak of Fortune": "Armor/Cloak_Fortune_SpecialGrade.png",
        "Lunar New Year Pieces": "Armor/Luna_NewYear_Cloak_Unobtainable.png",
        "Fragments (Reversal/Lapse)": "Armor/Fragment_Reversal_SpecialGrade.png",  # Using Reversal as default
        "Celestia / Dynesis / Helkytis": "Armor/Celestia_SpecialGrade.png",  # Using Celestia as default
        "Ragna / Crowns / Snake Masks": "Armor/Ragna_SpecialGrade.png",  # Using Ragna as default
        "Golden Chains of Fortune": "Armor/Golden_Chains_Of_Fortune_SpecialGrade.png",
        "Suit/Trousers of Fortune": "Armor/Suit_Of_Fortune_SpecialGrade.png",
        # Items
        "Blackhole Buddy / Nascent Cosmic Gear": "Armor/Blackhole_Buddy_Unobtainable.png",
        "Enlightenment Beads": "Armor/Enlightenment_Beads_Unobtainable.png",
        "Rotten Chains": "Armor/Rotten_Chains_SpecialGrade.png",
        "Rotten Ring": "Armor/Rotten_Ring_Special_Grade.png",
        "Tactful Ring": "Armor/Tactful_Ring.png",
    }

    for item_name, image_path in additional_images.items():
        try:
            item = Item.objects.get(name=item_name)
            if not item.image_url:  # Only add if image doesn't exist
                item.image_url = f"/media/{image_path}"
                item.save(update_fields=["image_url"])
        except Item.DoesNotExist:
            pass


class Migration(migrations.Migration):
    dependencies = [
        ("values", "0009_reorganize_categories_and_add_images"),
    ]

    operations = [
        migrations.RunPython(add_remaining_images, migrations.RunPython.noop),
    ]
