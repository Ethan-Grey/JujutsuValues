from django.db import migrations
from django.utils.text import slugify


def add_sample_data(apps, schema_editor):
    Category = apps.get_model("values", "Category")
    Item = apps.get_model("values", "Item")

    categories = [
        ("Cursed Tools", "#6366F1", "High-impact weapons and blades."),
        ("Abilities", "#14b8a6", "Movesets and ability unlocks."),
        ("Titles", "#f97316", "Seasonal and ranked titles."),
        ("Game Passes", "#0ea5e9", "Premium upgrades and perks."),
        ("Event Exclusives", "#8b5cf6", "Limited time drops and collectibles."),
    ]

    category_map = {}
    for name, color, description in categories:
        category, _ = Category.objects.get_or_create(
            name=name,
            defaults={"slug": slugify(name), "color": color, "description": description},
        )
        category_map[name] = category

    items = [
        {
            "name": "Sukuna's Dagger",
            "category": "Cursed Tools",
            "item_type": "item",
            "rarity": "exotic",
            "value": 1100,
            "demand": 9,
            "trend": "rising",
            "is_limited": True,
            "featured": True,
            "obtained_from": "Halloween Domain Raid",
            "notes": "Top-tier cursed tool with high bleed damage and solid scaling.",
        },
        {
            "name": "Blazing Katana",
            "category": "Cursed Tools",
            "item_type": "item",
            "rarity": "legendary",
            "value": 750,
            "demand": 7,
            "trend": "stable",
            "is_limited": False,
            "featured": False,
            "obtained_from": "Flame Challenge Shop",
            "notes": "Reliable mid-high value blade with consistent demand.",
        },
        {
            "name": "Heavenly Restriction",
            "category": "Abilities",
            "item_type": "item",
            "rarity": "mythic",
            "value": 920,
            "demand": 8,
            "trend": "rising",
            "is_limited": True,
            "featured": True,
            "obtained_from": "Tournament Reward",
            "notes": "Sought-after build for high mobility PvP setups.",
        },
        {
            "name": "Six Eyes",
            "category": "Abilities",
            "item_type": "item",
            "rarity": "exotic",
            "value": 1250,
            "demand": 10,
            "trend": "rising",
            "is_limited": True,
            "featured": True,
            "obtained_from": "Gojo Event",
            "notes": "Premium ability core; pairs well with most endgame kits.",
        },
        {
            "name": "Sorcerer Supreme",
            "category": "Titles",
            "item_type": "title",
            "rarity": "limited",
            "value": 540,
            "demand": 6,
            "trend": "stable",
            "is_limited": True,
            "featured": False,
            "obtained_from": "Ranked Season 3",
            "notes": "Popular flex title; collectors keep value afloat.",
        },
        {
            "name": "Shadow Monarch",
            "category": "Titles",
            "item_type": "title",
            "rarity": "legendary",
            "value": 420,
            "demand": 5,
            "trend": "falling",
            "is_limited": False,
            "featured": False,
            "obtained_from": "Boss Rush Milestone",
            "notes": "Value soft-correcting as supply increases.",
        },
        {
            "name": "Domain Expansion Pass",
            "category": "Game Passes",
            "item_type": "gamepass",
            "rarity": "rare",
            "value": 310,
            "demand": 6,
            "trend": "stable",
            "is_limited": False,
            "featured": False,
            "obtained_from": "Robux Store",
            "notes": "Steady utility pass; trades well for mid-tier items.",
        },
        {
            "name": "Cursed Energy Booster",
            "category": "Game Passes",
            "item_type": "gamepass",
            "rarity": "uncommon",
            "value": 180,
            "demand": 4,
            "trend": "stable",
            "is_limited": False,
            "featured": False,
            "obtained_from": "Robux Store",
            "notes": "Entry-level trade chip for newer players.",
        },
        {
            "name": "Winter's Heart",
            "category": "Event Exclusives",
            "item_type": "event",
            "rarity": "limited",
            "value": 680,
            "demand": 7,
            "trend": "rising",
            "is_limited": True,
            "featured": False,
            "obtained_from": "Snowfall Festival",
            "notes": "Seasonal collectible trending up as event closes.",
        },
        {
            "name": "Cursed Lantern",
            "category": "Event Exclusives",
            "item_type": "event",
            "rarity": "rare",
            "value": 260,
            "demand": 5,
            "trend": "stable",
            "is_limited": True,
            "featured": False,
            "obtained_from": "Night Parade Event",
            "notes": "Starter limited that trades quickly in lower tiers.",
        },
    ]

    for item in items:
        category = category_map[item["category"]]
        Item.objects.update_or_create(
            name=item["name"],
            defaults={
                "slug": slugify(item["name"]),
                "category": category,
                "item_type": item["item_type"],
                "rarity": item["rarity"],
                "value": item["value"],
                "demand": item["demand"],
                "trend": item["trend"],
                "is_limited": item["is_limited"],
                "featured": item["featured"],
                "obtained_from": item.get("obtained_from", ""),
                "notes": item.get("notes", ""),
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("values", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_sample_data, migrations.RunPython.noop),
    ]

