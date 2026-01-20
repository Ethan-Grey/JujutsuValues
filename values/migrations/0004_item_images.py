from django.db import migrations


def add_item_images(apps, schema_editor):
    Item = apps.get_model("values", "Item")

    # Map item names in the DB to image paths inside MEDIA_ROOT
    mapping = {
        # Cursed objects
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
        "Sword of Lapse (Blue) / Red Reversal": "Weapons/Sword_Of_Lapse_Blue.png",
        "Winter Bell": "Weapons/Winter_Bell.png",
        "Infinity Piercer": "Weapons/Infinity_Piercer.png",
        "ISOH": "Weapons/ISOH.png",
        "Vengeance": "Weapons/Vengeance.png",
        "Viscera Scythe": "Weapons/Viscera_Scythe.png",
        "Ravenous Axe": "Weapons/Ravenous_Axe.png",
        "Impossible Dream": "Weapons/Impossible_Dream.png",
        "Dragon Bone": "Weapons/Dragon_Bone.png",
        "Playful Cloud": "Weapons/Playful_Cloud.png",
        "Feathered Spear / Jet Black Blade": "Weapons/Feathered_Spear.png",
    }

    for name, rel_path in mapping.items():
        try:
            item = Item.objects.get(name=name)
        except Item.DoesNotExist:
            continue
        # Store as an absolute URL path so templates can use it directly
        item.image_url = f"/media/{rel_path}"
        item.save(update_fields=["image_url"])


class Migration(migrations.Migration):
    dependencies = [
        ("values", "0003_real_value_catalog"),
    ]

    operations = [
        migrations.RunPython(add_item_images, migrations.RunPython.noop),
    ]


