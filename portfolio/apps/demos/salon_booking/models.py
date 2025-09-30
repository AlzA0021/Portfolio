"""
Salon Booking Demo Models
Simplified version from the original Salonify project
"""

from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


# ----------------------------------------------------------
# Helper function for file uploads
def salon_image_upload(instance, filename):
    return f'demos/salons/{instance.salon.id if hasattr(instance, "salon") else "default"}/{filename}'


# ----------------------------------------------------------
# Salon Model (Simplified)
class Salon(models.Model):
    salon_name = models.CharField(max_length=200, verbose_name="Salon Name")
    description = models.TextField(blank=True, verbose_name="Description")
    banner_image = models.ImageField(
        upload_to="demos/salons/banners/",
        default="default_salon_banner.jpg",
        verbose_name="Banner Image",
        null=True,
        blank=True,
    )

    # Location info (simplified - no GIS for now)
    zone = models.PositiveIntegerField(
        verbose_name="Zone", null=True, blank=True, help_text="District/Zone number"
    )
    address = models.TextField(verbose_name="Address", blank=True, null=True)

    # Contact info
    phone_number = models.CharField(
        max_length=15, verbose_name="Phone Number", null=True, blank=True
    )

    # Social links
    instagram_link = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Instagram Link"
    )
    telegram_link = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Telegram Link"
    )

    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    registered_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Registration Date"
    )

    # Stats
    view_count = models.PositiveIntegerField(default=0, verbose_name="View Count")

    class Meta:
        verbose_name = "Demo Salon"
        verbose_name_plural = "Demo Salons"
        db_table = "demo_salon"
        ordering = ["-registered_date"]

    def __str__(self):
        return self.salon_name

    def get_average_score(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.filter(is_active=True)
        if reviews.exists():
            return round(reviews.aggregate(models.Avg("rating"))["rating__avg"], 1)
        return None

    def get_salon_age_years(self):
        """Calculate salon age in years"""
        from datetime import datetime

        if self.registered_date.tzinfo is not None:
            now = datetime.now(self.registered_date.tzinfo)
        else:
            now = datetime.now()
        delta = now - self.registered_date
        return delta.days // 365

    def increment_view_count(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=["view_count"])


# ----------------------------------------------------------
# Salon Gallery
class SalonGallery(models.Model):
    salon = models.ForeignKey(
        Salon,
        on_delete=models.CASCADE,
        verbose_name="Salon",
        related_name="gallery_images",
    )
    image = models.ImageField(
        upload_to=salon_image_upload, verbose_name="Gallery Image"
    )
    caption = models.CharField(max_length=200, blank=True, verbose_name="Caption")
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_cover = models.BooleanField(default=False, verbose_name="Cover Image")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name = "Salon Gallery Image"
        verbose_name_plural = "Salon Gallery Images"
        db_table = "demo_salon_gallery"
        ordering = ["order", "-is_cover"]

    def __str__(self):
        return f"{self.salon.salon_name} - Image {self.order}"


# ----------------------------------------------------------
# Salon Opening Hours
class SalonOpeningHours(models.Model):
    DAY_CHOICES = [
        (1, "Saturday"),
        (2, "Sunday"),
        (3, "Monday"),
        (4, "Tuesday"),
        (5, "Wednesday"),
        (6, "Thursday"),
        (7, "Friday"),
    ]

    salon = models.ForeignKey(
        Salon,
        on_delete=models.CASCADE,
        related_name="opening_hours",
        verbose_name="Salon",
    )
    day_of_week = models.PositiveSmallIntegerField(
        choices=DAY_CHOICES, verbose_name="Day of Week"
    )
    open_time = models.TimeField(null=True, blank=True, verbose_name="Opening Time")
    close_time = models.TimeField(null=True, blank=True, verbose_name="Closing Time")
    is_closed = models.BooleanField(default=False, verbose_name="Closed")

    class Meta:
        verbose_name = "Salon Opening Hours"
        verbose_name_plural = "Salon Opening Hours"
        db_table = "demo_salon_opening_hours"
        unique_together = ("salon", "day_of_week")

    def __str__(self):
        return f"{self.salon.salon_name} - {self.get_day_of_week_display()}"


# ----------------------------------------------------------
# Service Category
class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Icon Class")
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"
        db_table = "demo_service_category"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


# ----------------------------------------------------------
# Service
class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Service Name")
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="services",
        verbose_name="Category",
    )
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(
        upload_to="demos/services/", null=True, blank=True, verbose_name="Service Image"
    )
    duration_minutes = models.PositiveIntegerField(
        default=30, verbose_name="Duration (minutes)"
    )
    base_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Base Price"
    )
    salons = models.ManyToManyField(
        Salon, related_name="services", verbose_name="Available at Salons"
    )
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Demo Service"
        verbose_name_plural = "Demo Services"
        db_table = "demo_service"
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


# ----------------------------------------------------------
# Salon Review/Rating
class SalonReview(models.Model):
    salon = models.ForeignKey(
        Salon, on_delete=models.CASCADE, related_name="reviews", verbose_name="Salon"
    )
    customer_name = models.CharField(max_length=100, verbose_name="Customer Name")
    rating = models.PositiveSmallIntegerField(
        choices=[(i, f"{i} Stars") for i in range(1, 6)], verbose_name="Rating"
    )
    comment = models.TextField(verbose_name="Review Comment")
    is_active = models.BooleanField(default=True, verbose_name="Approved")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Salon Review"
        verbose_name_plural = "Salon Reviews"
        db_table = "demo_salon_review"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer_name} - {self.salon.salon_name} ({self.rating}⭐)"


# ----------------------------------------------------------
# Amenity/Feature
class SalonAmenity(models.Model):
    salon = models.ForeignKey(
        Salon, on_delete=models.CASCADE, related_name="amenities", verbose_name="Salon"
    )
    title = models.CharField(max_length=100, verbose_name="Amenity Title")
    icon_class = models.CharField(max_length=50, blank=True, verbose_name="Icon Class")
    description = models.CharField(
        max_length=200, blank=True, verbose_name="Description"
    )
    is_active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name = "Salon Amenity"
        verbose_name_plural = "Salon Amenities"
        db_table = "demo_salon_amenity"

    def __str__(self):
        return f"{self.salon.salon_name} - {self.title}"
