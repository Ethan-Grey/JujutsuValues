from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


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
    image_url = models.CharField(max_length=500, blank=True, help_text="Image URL or path (e.g., /media/Weapons/Item.png)")
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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name or self.user.username


class InventoryItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inventory_items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="inventory_entries")
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "item")
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.user.username} - {self.item.name} x{self.quantity}"


class SavedTrade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_trades")
    created_at = models.DateTimeField(auto_now_add=True)
    offer_items = models.JSONField()
    request_items = models.JSONField()
    offer_total = models.PositiveIntegerField(default=0)
    request_total = models.PositiveIntegerField(default=0)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Trade #{self.pk} by {self.user.username}"


class VerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="verification_token")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Verification token for {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Ensure profile exists and stays in sync
    Profile.objects.get_or_create(user=instance)


class ValueChangeRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="value_change_requests")
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="value_change_requests")
    current_value = models.PositiveIntegerField(help_text="Current value of the item")
    requested_value = models.PositiveIntegerField(help_text="Requested new value")
    reason = models.TextField(help_text="Reason for the value change request")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_value_changes",
        help_text="Superuser who reviewed this request"
    )
    review_notes = models.TextField(blank=True, help_text="Admin notes on approval/rejection")
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Value Change Request"
        verbose_name_plural = "Value Change Requests"

    def __str__(self):
        return f"{self.item.name}: {self.current_value} → {self.requested_value} ({self.get_status_display()})"
