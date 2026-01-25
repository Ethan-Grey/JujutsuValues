"""
Management command to match vow images from media/vows folder to vow items.
Matches images based on vow name.
"""
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from values.models import Item


class Command(BaseCommand):
    help = 'Match vow images from media/vows folder to vow items based on name'

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        vows_folder = os.path.join(media_root, 'vows')
        
        if not os.path.exists(vows_folder):
            self.stdout.write(
                self.style.WARNING(f'Vows folder not found at {vows_folder}')
            )
            self.stdout.write(
                self.style.WARNING('Please create the folder and add vow images first.')
            )
            return
        
        # Get all vow items (items starting with "Vow:")
        vow_items = Item.objects.filter(name__istartswith='Vow:')
        
        if not vow_items.exists():
            self.stdout.write(
                self.style.WARNING('No vow items found in database.')
            )
            return
        
        # Get all image files in vows folder
        image_files = []
        if os.path.isdir(vows_folder):
            for filename in os.listdir(vows_folder):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    image_files.append(filename)
        
        if not image_files:
            self.stdout.write(
                self.style.WARNING(f'No image files found in {vows_folder}')
            )
            return
        
        self.stdout.write(f'Found {vow_items.count()} vow items and {len(image_files)} image files')
        
        # Match images to items
        matched = 0
        updated = 0
        
        for item in vow_items:
            # Extract vow name from item name (e.g., "Vow: Unbreakable" -> "Unbreakable")
            vow_name = item.name.replace('Vow: ', '').strip()
            
            # Try to find matching image
            # Look for images that contain the vow name (case-insensitive)
            matching_image = None
            for img_file in image_files:
                # Remove extension and normalize
                img_name = os.path.splitext(img_file)[0]
                # Try exact match or contains match
                if vow_name.lower() in img_name.lower() or img_name.lower() in vow_name.lower():
                    matching_image = img_file
                    break
            
            if matching_image:
                matched += 1
                # Construct image URL
                image_url = f'/media/vows/{matching_image}'
                
                # Only update if different
                if item.image_url != image_url:
                    item.image_url = image_url
                    item.save(update_fields=['image_url'])
                    updated += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Matched {item.name} -> {matching_image}'
                        )
                    )
                else:
                    self.stdout.write(
                        f'  {item.name} already has correct image'
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'✗ No matching image found for {item.name}')
                )
                # List available images for debugging
                self.stdout.write(f'  Available images: {", ".join(image_files[:5])}...')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted: {matched} matched, {updated} updated'
            )
        )

