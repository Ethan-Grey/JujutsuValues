from django.db import migrations


def update_rarity_values(apps, schema_editor):
    Item = apps.get_model("values", "Item")
    
    # Map old rarities to new rarities
    rarity_mapping = {
        "legendary": "special_grade",
        "mythic": "special_grade",
        "limited": "rare",
        "exotic": "rare",
        "rare": "rare",
        "uncommon": "uncommon",
        "common": "common",
    }
    
    for old_rarity, new_rarity in rarity_mapping.items():
        Item.objects.filter(rarity=old_rarity).update(rarity=new_rarity)


def reverse_rarity_update(apps, schema_editor):
    Item = apps.get_model("values", "Item")
    
    # Reverse mapping - approximate
    reverse_mapping = {
        "special_grade": "legendary",
        "rare": "rare",
        "uncommon": "uncommon",
        "common": "common",
    }
    
    for new_rarity, old_rarity in reverse_mapping.items():
        Item.objects.filter(rarity=new_rarity).update(rarity=old_rarity)


class Migration(migrations.Migration):
    dependencies = [
        ("values", "0006_fix_items_and_split"),
    ]

    operations = [
        migrations.RunPython(update_rarity_values, reverse_rarity_update),
    ]
