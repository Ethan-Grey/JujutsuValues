from django.db import migrations


def encode_paths(apps, schema_editor):
    Item = apps.get_model("values", "Item")
    updates = 0
    for item in Item.objects.exclude(image_url="").iterator():
        if " " in item.image_url and "/media/" in item.image_url:
            new_url = item.image_url.replace(" ", "%20")
            item.image_url = new_url
            item.save(update_fields=["image_url"])
            updates += 1
    # no-op return; keeping updates variable for potential logging/debug


class Migration(migrations.Migration):
    dependencies = [
        ("values", "0004_item_images"),
    ]

    operations = [
        migrations.RunPython(encode_paths, migrations.RunPython.noop),
    ]

