from django.db import migrations
from django.utils.text import slugify


def reorganize_categories_and_add_images(apps, schema_editor):
    Category = apps.get_model("values", "Category")
    Item = apps.get_model("values", "Item")

    # Get main categories
    weapons_cat = Category.objects.get(slug="weapons")
    armor_cat = Category.objects.get(slug="armor")
    titles_cat = Category.objects.get(slug="titles")
    items_cat = Category.objects.get(slug="items")
    cursed_objects_cat = Category.objects.get(slug="cursed-objects")

    # Map event items to their proper categories
    event_item_mapping = {
        # Halloween items
        "Halloween Armor Pieces": armor_cat,
        "Hallowed Scythe": weapons_cat,
        # Exchange items - weapons
        "Spiked Gauntlets": weapons_cat,
        "Twin Kusarigama": weapons_cat,
        # Exchange items - scrolls/items
        "Scroll of Overwhelming Energy": cursed_objects_cat,
        "Premium Battle Pass": items_cat,
        # Exchange items - vows (treating as items for now, adjust if needed)
        "Vow: Unbreakable": items_cat,
        "Vow: Snow Grave": items_cat,
        "Vow: Justice": items_cat,
        "Vow: Impact": items_cat,
        "Vow: Ceaseless Slashes": items_cat,
        "Vow: Blood Beam": items_cat,
        "Vow: Red Reflection": items_cat,
        "Vow: Spatial Pulverize": items_cat,
        # Winter items - titles
        "Krampus Slayer (Title)": titles_cat,
        "Ice Exorcist (Title)": titles_cat,
        # Winter items - weapons
        "Scroll of Sub Zero": cursed_objects_cat,
        "Twin Cryo Blasters": weapons_cat,
        # Winter items - armor
        "Frosted Coat": armor_cat,
        "Frosted Leggings": armor_cat,
        "Halo of Frost": armor_cat,
        "Ring of Frost": armor_cat,
    }

    # Move event items to proper categories
    for item_name, new_category in event_item_mapping.items():
        try:
            item = Item.objects.get(name=item_name)
            item.category = new_category
            item.save()
        except Item.DoesNotExist:
            pass

    # Comprehensive image mapping
    image_mapping = {
        # Cursed Objects
        "Frost Scroll": "Cursed objects/Frost_Scroll.png",
        "Sleigh Skill Scroll": "Cursed objects/Sleigh_Scroll.png",
        "Snow Brigade / Snowman Scroll": "Cursed objects/Snow_Brigade.png",
        "Golden Wind Scroll": "Cursed objects/Golden_Wind_Scroll.png",
        "Domain Shards": "Cursed objects/Domain_Shard.png",
        "Max Scroll": "Cursed objects/Maximum_Scroll.png",
        "Demonic Hellstomp Scroll": "Cursed objects/Demonic_Hellstomp_Scroll.png",
        "Cursed Hands": "Cursed objects/Cursed_Hand.png",
        "Energy Nature Scrolls": "Cursed objects/Energy_Nature_Scroll.png",
        "Demon Fingers": "Cursed objects/Demon_Finger.png",
        # Weapons
        "Heian Gauntlets": "Weapons/Heian_Gauntlet.png",
        "Turbo Mask (Turbo Max)": "Weapons/Turbo_Mask.png",
        "Hollow Sword": "Weapons/Hollow_Sword.png",
        "Sword of Lapse (Blue)": "Weapons/Sword_Of_Lapse_Blue.png",
        "Sword of Lapse (Red)": "Weapons/Sword_Of_Lapse_Red.png",
        "Winter Bell": "Weapons/Winter_Bell.png",
        "Infinity Piercer": "Weapons/Infinity_Piercer.png",
        "ISOH": "Weapons/ISOH.png",
        "Vengeance": "Weapons/Vengeance.png",
        "Viscera Scythe": "Weapons/Viscera_Scythe.png",
        "Ravenous Axe": "Weapons/Ravenous_Axe.png",
        "Impossible Dream": "Weapons/Impossible_Dream.png",
        "Dragon Bone": "Weapons/Dragon_Bone.png",
        "Playful Cloud": "Weapons/Playful_Cloud.png",
        "Feathered Spear": "Weapons/Feathered_Spear.png",
        "Jet Black Blade": "Weapons/Jet_Black_Blade.png",
        "Hallowed Scythe": "Weapons/Halloween_Hallowed_Scythe_Unobtainable.png",
        "Spiked Gauntlets": "Weapons/ExchangeEvent_Spiked_Gauntlets_Unobtainable.png",
        "Twin Kusarigama": "Weapons/ExchangeEvent_Twin_Kusarigama_Unobtainable.png",
        "Twin Cryo Blasters": "Weapons/WinterEvent_Twin_Cryoblasters_Unobtainable.png",
        # Armor
        "Dark Heian Robe": "Armor/Dark_Heian_Robe_Uobtainable.png",
        "Dark Heian Pants": "Armor/Dark_Heian_Pants_Uobtainable.png",
        "Scarf of the Chosen": "Armor/Scarf_Of_The_Chosen_Uobtainable.png",
        "Golden Haori": "Armor/Golden_Haori_Uobtainable.png",
        "Lobotomy Volcano Head": "Armor/Lobotomy_Volcano_Unobtainable.png",
        "Halloween Armor Pieces": "Armor/HalloweenArmorSet_Pumpkin_Reaper's_Head_Unobtainable.png",
        "Frosted Coat": "Armor/WinterEvent_Forsted_Coat_Unobtainable.png",
        "Frosted Leggings": "Armor/WinterEvent_Forsted_Leggings_Unobtainable.png",
        "Halo of Frost": "Armor/WinterEvent_Halo_Frost_Unobtainable.png",
        "Ring of Frost": "Armor/WinterEvent_Ring_Of_Frost_Unobtainable.png",
        # Titles
        "Divine Heian Sorcerer": "Titles/Divine_Heian_Sorcerer.png",
        "Domain Master": "Titles/Domain_Master.png",
        "El Finger": "Titles/El_Finger.png",
        "God of Domains": "Titles/God_Of_Domains.png",
        "Heian Angel": "Titles/Heian_Angel.png",
        "Heian Centimillionaire": "Titles/Heian_Centimillionare.png",
        "Heian Demon": "Titles/Heian_Demon.png",
        "Heian Millionaire": "Titles/Heian_Millionare.png",
        "Heian Multimillionaire": "Titles/Heian_Multimillionare.png",
        "Heian Spirit": "Titles/Heian_Spirit.png",
        "Lord of Domains / Go Outside": "Titles/Lord_Of_Domains.png",
        "Maximum Master": "Titles/Maximum_Master.png",
        "Maximum Merchant": "Titles/Maximum_Merchant.png",
        "Nah I'd Win": "Titles/Nah_I'd_Win.png",
        "Please Touch Grass": "Titles/Please_Touch_Grass.png",
        "Stand Proud": "Titles/Stand_Proud.png",
        "The Fraudulent One": "Titles/The_Fraudulent_One.png",
        "Frost Slayer": "Titles/NewTitles_Frost_Slayer.png",
        "King of Souls": "Titles/NewTitles_King_Of_Souls.png",
        "1 Year Anniversary": "Titles/NewTitle_1_Year_Anniversary.png",
        "Halloween One Aura Title": "Titles/NewTitles_Hallowed_One.png",
        "Krampus Slayer (Title)": "Titles/WinterEvent_Krampus_Slayer.png",
        "Ice Exorcist (Title)": "Titles/WinterEvent_Ice_Exorcist.png",
        "Release Festival": "Titles/Release_Festivle_Unobtainable.png",
    }

    # Add images to items
    for item_name, image_path in image_mapping.items():
        try:
            item = Item.objects.get(name=item_name)
            item.image_url = f"/media/{image_path}"
            item.save(update_fields=["image_url"])
        except Item.DoesNotExist:
            pass

    # Delete event categories
    Category.objects.filter(slug__in=["event-items-halloween", "event-items-exchange", "event-items-winter"]).delete()


def reverse_migration(apps, schema_editor):
    # This would be complex to reverse, so we'll just pass
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("values", "0008_alter_item_rarity"),
    ]

    operations = [
        migrations.RunPython(reorganize_categories_and_add_images, reverse_migration),
    ]
