from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(
        max_length=20,
        default="#6366F1",
        help_text="Hex color used for category badges",
    )

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Item(models.Model):
    class ItemType(models.TextChoices):
        ITEM = "item", "Item"
        TITLE = "title", "Title"
        GAMEPASS = "gamepass", "Game Pass"
        EVENT = "event", "Event Item"

    class Rarity(models.TextChoices):
        UNOBTAINABLE = "unobtainable", "Unobtainable"
        SPECIAL_GRADE = "special_grade", "Special Grade"
        RARE = "rare", "Rare"
        UNCOMMON = "uncommon", "Uncommon"
        COMMON = "common", "Common"

    class Trend(models.TextChoices):
        RISING = "rising", "Rising"
        STABLE = "stable", "Stable"
        FALLING = "falling", "Falling"

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="items"
    )
    item_type = models.CharField(
        max_length=20, choices=ItemType.choices, default=ItemType.ITEM
    )
    rarity = models.CharField(
        max_length=20, choices=Rarity.choices, default=Rarity.COMMON
    )
    value = models.PositiveIntegerField(help_text="Trade value points")
    demand = models.PositiveSmallIntegerField(default=5, help_text="1-10 scale")
    trend = models.CharField(
        max_length=10, choices=Trend.choices, default=Trend.STABLE
    )
    is_limited = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    obtained_from = models.CharField(
        max_length=200, blank=True, help_text="Event, raid, or source"
    )
    image_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-featured", "-value", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("values:item_detail", args=[self.slug])

    def get_star_count(self):
        """Return number of filled stars (1-5) based on demand (1-10 scale)"""
        # Convert 1-10 demand to 1-5 stars
        return min(5, max(1, (self.demand + 1) // 2))

# Create your models here.
