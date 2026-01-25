from django.db import migrations
from django.utils.text import slugify


def upsert_items(apps, schema_editor):
    Category = apps.get_model("values", "Category")
    Item = apps.get_model("values", "Item")

    category_defs = [
        ("Cursed Objects", "#1d4ed8", "Scrolls and cursed tools."),
        ("Weapons", "#9333ea", "All weapon drops and blades."),
        ("Items", "#047857", "Utility items and special drops."),
        ("Game Passes", "#0ea5e9", "Robux passes and perks."),
        ("Armor", "#f59e0b", "Armor sets and cosmetics."),
        ("Titles", "#ec4899", "Rare and event titles."),
        ("Event Items - Halloween", "#7c3aed", "Halloween exclusives."),
        ("Event Items - Exchange", "#0891b2", "Exchange event rewards."),
        ("Event Items - Winter", "#2563eb", "Winter event exclusives."),
    ]

    categories = {}
    for name, color, desc in category_defs:
        cat, _ = Category.objects.update_or_create(
            name=name,
            defaults={"slug": slugify(name), "color": color, "description": desc},
        )
        categories[name] = cat

    # helper to convert demand words to a 1-10 scale
    def demand_score(label: str) -> int:
        label = label.lower()
        if "insane" in label or "extreme" in label:
            return 10
        if "very high" in label or "extremely" in label:
            return 9
        if "great" in label or "high" in label or "rising" in label:
            return 8
        if "good" in label:
            return 7
        if "mid" in label or "medium" in label or "decent" in label:
            return 5
        if "low" in label:
            return 3
        return 6

    def midpoint(low, high):
        return int((low + high) / 2)

    items = [
        # Cursed Objects
        ("Frost Scroll", "Cursed Objects", 650, 750, "rising", True, "High demand, often overpay"),
        ("Sleigh Skill Scroll", "Cursed Objects", 625, 700, "rising", True, "Good demand, overpay possible"),
        ("Snow Brigade / Snowman Scroll", "Cursed Objects", 100, 100, "stable", False, "Decent demand, occasional underpay"),
        ("Golden Wind Scroll", "Cursed Objects", 100, 120, "rising", False, "Medium demand, trending up"),
        ("Domain Shards", "Cursed Objects", 50, 60, "rising", False, "Great demand, frequent overpay"),
        ("Max Scroll", "Cursed Objects", 50, 60, "rising", False, "Great demand, frequent overpay"),
        ("Demonic Hellstomp Scroll", "Cursed Objects", 20, 35, "falling", False, "Low demand"),
        ("Cursed Hands", "Cursed Objects", 10, 10, "stable", False, "High demand"),
        ("Energy Nature Scrolls", "Cursed Objects", 10, 10, "stable", False, "High demand"),
        ("Demon Fingers", "Cursed Objects", 1, 1, "stable", False, "Good demand"),
        # Weapons
        ("Heian Gauntlets", "Weapons", 3000, 3200, "rising", True, "Demand varies; often sells ~2500 but can reach 3k+"),
        ("Turbo Mask (Turbo Max)", "Weapons", 1000, 1300, "rising", True, "Very high demand; recently surged"),
        ("Finger Collector", "Weapons", 700, 800, "rising", True, "Good demand; overpay common"),
        ("Hollow Sword", "Weapons", 650, 700, "rising", True, "Insane demand; rising"),
        ("Sword of Lapse (Blue) / Red Reversal", "Weapons", 325, 350, "rising", False, "Great demand; rising"),
        ("Winter Bell", "Weapons", 75, 100, "stable", False, "Mid demand; small underpay common"),
        ("Infinity Piercer", "Weapons", 10, 25, "stable", False, "Good demand; fair pay"),
        ("ISOH", "Weapons", 15, 20, "rising", False, "Great demand; overpay common"),
        ("Vengeance", "Weapons", 10, 15, "stable", False, "Mid demand; small overpay"),
        ("Viscera Scythe", "Weapons", 5, 6, "stable", False, "Okay demand; fair to underpay"),
        ("Ravenous Axe", "Weapons", 5, 6, "stable", False, "Good demand; can overpay"),
        ("Impossible Dream", "Weapons", 4, 5, "stable", False, "Decent demand; fair pay"),
        ("Dragon Bone", "Weapons", 3, 5, "falling", False, "Low demand; underpay"),
        ("Playful Cloud", "Weapons", 10, 10, "stable", False, "Stable; slight overpay possible"),
        ("Feathered Spear / Jet Black Blade", "Weapons", 1, 5, "falling", False, "Very low demand; underpay common"),
        # Items
        ("Frost Petal", "Items", 50, 10000, "rising", True, "Special deals"),
        ("Curse Bloom", "Items", 50, 1000, "rising", True, "Special deals"),
        ("Spring Puff", "Items", 50, 1000, "rising", True, "Special deals"),
        ("Prison Realm", "Items", 0, 0, "stable", True, "Unobtainable"),
        ("Tactful Ring", "Items", 1, 5, "stable", False, "Mid; 2nd best calamity ring"),
        ("Rotten Ring", "Items", 3, 5, "stable", False, "Mid"),
        ("Enlightenment Beads", "Items", 800, 800, "falling", False, "Medium demand; heavy underpay common"),
        ("Rotten Chains", "Items", 5, 5, "stable", False, "Holds 5 demon fingers"),
        ("Blackhole Buddy / Nascent Cosmic Gear", "Items", 5, 5, "stable", False, "Good early/mid stats"),
        # Game Passes
        ("Item Notifier", "Game Passes", 250, 300, "rising", False, "Good demand; overpay common"),
        ("Heavenly Restriction (Pass)", "Game Passes", 150, 150, "stable", False, "Mid demand"),
        ("500 Spins", "Game Passes", 100, 100, "rising", False, "Good demand; overpay possible"),
        ("Innate Bag", "Game Passes", 50, 75, "stable", False, "Often sells for ~50"),
        ("Innate Slot 3", "Game Passes", 50, 50, "stable", False, "Good demand; overpay possible"),
        ("Innate Slot 4", "Game Passes", 50, 50, "stable", False, "Fair pay"),
        ("Skip Spins", "Game Passes", 20, 20, "rising", False, "Great demand; big overpay"),
        ("2x Emote Slots", "Game Passes", 20, 20, "stable", False, "Mid demand; fair to small overpay"),
        # Armor
        ("Lobotomy Volcano Head", "Armor", 6, 7, "stable", False, "Low demand; fair pay"),
        ("Dark Heian Robe", "Armor", 1900, 1900, "rising", True, "Good demand; overpay/fair"),
        ("Dark Heian Pants", "Armor", 1650, 1650, "stable", False, "Decent demand; fair"),
        ("Scarf of the Chosen", "Armor", 250, 250, "falling", False, "Low demand; underpay"),
        ("Golden Haori", "Armor", 250, 250, "stable", False, "Mid demand; fair to slight underpay"),
        ("Eyes Sets (Willpower/Insight/Bloodthirst)", "Armor", 5, 5, "stable", False, "Medium demand; occasional overpay"),
        ("Demonic Outfit Pieces", "Armor", 5, 5, "stable", False, "Decent demand; fair"),
        ("Festive Outfit Pieces", "Armor", 50, 60, "stable", False, "Decent demand; fair"),
        ("Imaginary King / Aetherion / Phantasis / Impera", "Armor", 50, 60, "stable", False, "Good demand; fair to overpay"),
        ("Cloak of Fortune", "Armor", 50, 50, "stable", False, "Low demand; uninformed buyers may overpay"),
        ("Lunar New Year Pieces", "Armor", 20, 30, "stable", False, "Good demand; fair"),
        ("Fragments (Reversal/Lapse)", "Armor", 25, 25, "rising", False, "Great/Good demand; overpay possible"),
        ("Celestia / Dynesis / Helkytis", "Armor", 25, 25, "rising", False, "Good demand; overpay common"),
        ("Ragna / Crowns / Snake Masks", "Armor", 25, 25, "stable", False, "Decent demand; fair"),
        ("Golden Chains of Fortune", "Armor", 20, 25, "stable", False, "Mid demand"),
        ("Suit/Trousers of Fortune", "Armor", 15, 25, "falling", False, "Low demand; underpay"),
        # Titles
        ("Release Festival", "Titles", 5, 5, "stable", False, "No demand"),
        ("Heian Millionaire", "Titles", 175, 200, "stable", False, "Low demand"),
        ("Heian Multimillionaire", "Titles", 400, 400, "stable", False, "Low demand"),
        ("Exchange Student", "Titles", 3700, 3800, "rising", True, "Rising; rare"),
        ("The Calamity", "Titles", 3700, 3800, "rising", False, "Good demand"),
        ("Exchange Champion", "Titles", 6000, 7500, "rising", True, "Very high demand during events"),
        ("El Finger", "Titles", 3000, 3000, "stable", False, "Mid–low demand"),
        ("Divine Heian Sorcerer", "Titles", 3700, 3800, "rising", True, "High demand"),
        ("Chains of Calamity", "Titles", 12500, 13000, "rising", True, "Great demand"),
        ("Nah I’d Win", "Titles", 16000, 17000, "rising", True, "Good demand"),
        ("Stand Proud", "Titles", 22000, 23000, "rising", True, "Good demand"),
        ("Domain Master", "Titles", 25000, 28000, "rising", True, "Good demand"),
        ("Heian Spirit", "Titles", 24000, 26000, "rising", True, "Rare"),
        ("Maximum Master", "Titles", 38000, 42000, "rising", True, "Very rare"),
        ("The Fraudulent One", "Titles", 40000, 50000, "rising", True, "Rare; overpay common"),
        ("Lord of Domains / Go Outside", "Titles", 30000, 50000, "rising", True, "Very rare"),
        ("Heian Demon", "Titles", 50000, 75000, "rising", True, "Extremely rare"),
        ("God of Domains", "Titles", 65000, 95000, "rising", True, "Extremely rare"),
        ("Heian Angel", "Titles", 75000, 100000, "rising", True, "Extremely rare"),
        ("Maximum Merchant", "Titles", 105000, 130000, "rising", True, "Extremely rare"),
        ("Please Touch Grass", "Titles", 120000, 160000, "rising", True, "Very high demand"),
        ("Heian Centimillionaire", "Titles", 35000, 35000, "stable", False, "More common than before"),
        ("Mugen Piercer", "Titles", 69000, 72000, "rising", True, "Very rare"),
        ("King of Souls", "Titles", 45, 75, "stable", False, "Recent title"),
        ("Frost Slayer", "Titles", 15, 30, "stable", False, "Recent title"),
        ("1 Year Anniversary", "Titles", 25, 30, "stable", False, "Recent title"),
        ("Halloween One Aura Title", "Titles", 130, 160, "stable", False, "Recent title"),
        ("Krampus Slayer (Title)", "Event Items - Winter", 150, 300, "rising", True, "Insanely rare title"),
        ("Ice Exorcist (Title)", "Event Items - Winter", 15, 25, "stable", False, "Winter title"),
        # Event Items - Halloween
        ("Halloween Armor Pieces", "Event Items - Halloween", 25, 25, "stable", False, "Varies"),
        ("Hallowed Scythe", "Event Items - Halloween", 50, 60, "stable", False, "Varies"),
        # Event Items - Exchange
        ("Scroll of Overwhelming Energy", "Event Items - Exchange", 50, 50, "stable", False, "Medium–low demand"),
        ("Premium Battle Pass", "Event Items - Exchange", 60, 70, "rising", False, "Selling fast"),
        ("Spiked Gauntlets", "Event Items - Exchange", 175, 210, "rising", True, "High demand"),
        ("Twin Kusarigama", "Event Items - Exchange", 150, 150, "stable", False, "Medium–high demand"),
        ("Vow: Unbreakable", "Event Items - Exchange", 100, 150, "rising", False, "Vow item"),
        ("Vow: Snow Grave", "Event Items - Exchange", 100, 140, "stable", False, "Vow item"),
        ("Vow: Justice", "Event Items - Exchange", 120, 120, "stable", False, "Vow item"),
        ("Vow: Impact", "Event Items - Exchange", 50, 50, "stable", False, "Vow item"),
        ("Vow: Ceaseless Slashes", "Event Items - Exchange", 200, 250, "rising", True, "Vow item"),
        ("Vow: Blood Beam", "Event Items - Exchange", 50, 50, "stable", False, "Vow item"),
        ("Vow: Red Reflection", "Event Items - Exchange", 100, 150, "rising", False, "Vow item"),
        ("Vow: Spatial Pulverize", "Event Items - Exchange", 150, 200, "rising", True, "Extreme demand"),
        # Event Items - Winter
        ("Scroll of Sub Zero", "Event Items - Winter", 80, 95, "rising", False, "Winter event"),
        ("Twin Cryo Blasters", "Event Items - Winter", 115, 130, "rising", False, "Winter event"),
        ("Frosted Coat", "Event Items - Winter", 35, 50, "stable", False, "Winter event"),
        ("Frosted Leggings", "Event Items - Winter", 35, 45, "stable", False, "Winter event"),
        ("Halo of Frost", "Event Items - Winter", 35, 40, "stable", False, "Winter event"),
        ("Ring of Frost", "Event Items - Winter", 30, 40, "stable", False, "Winter event"),
    ]

    for name, cat_name, low, high, trend, featured, note in items:
        category = categories[cat_name]
        value_mid = midpoint(low, high)
        demand = demand_score(note)
        # Only create if item doesn't exist - don't update existing items to preserve production data
        Item.objects.get_or_create(
            name=name,
            defaults={
                "slug": slugify(name),
                "category": category,
                "item_type": "item" if cat_name != "Titles" and "Passes" not in cat_name else ("gamepass" if "Passes" in cat_name else "title"),
                "rarity": "legendary" if featured else "rare",
                "value": max(value_mid, 0),
                "demand": demand,
                "trend": trend,
                "is_limited": featured,
                "featured": featured,
                "obtained_from": cat_name,
                "notes": f"{note} • Range {low}-{high}",
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("values", "0002_sample_data"),
    ]

    operations = [
        migrations.RunPython(upsert_items, migrations.RunPython.noop),
    ]

