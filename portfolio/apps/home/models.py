# apps/home/models.py
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


# ----------------------------------------------------------
# ContactMessage model (existing)
class ContactMessage(models.Model):
    CATEGORY_CHOICES = [
        ("general", "General Inquiry"),
        ("support", "Technical Support"),
        ("business", "Business Partnership"),
        ("feedback", "Feedback"),
        ("other", "Other"),
    ]

    URGENCY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=150)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="general"
    )
    message = models.TextField()
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default="medium")
    subscribe_newsletter = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject}"


# ----------------------------------------------------------
# Portfolio Category model
class PortfolioCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Portfolio Category"
        verbose_name_plural = "Portfolio Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ----------------------------------------------------------
# Portfolio Item model
class PortfolioItem(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(
        PortfolioCategory, on_delete=models.CASCADE, related_name="items"
    )
    short_description = models.CharField(
        max_length=300, help_text="Short description for portfolio grid"
    )
    full_description = models.TextField(
        help_text="Detailed description for portfolio details page"
    )

    # Images
    thumbnail = models.ImageField(
        upload_to="portfolio/thumbnails/",
        help_text="Main image for portfolio grid (recommended: 600x400px)",
    )
    detail_image = models.ImageField(
        upload_to="portfolio/details/",
        blank=True,
        null=True,
        help_text="Larger image for detail page (optional)",
    )

    # Project details
    client = models.CharField(max_length=100, blank=True)
    project_date = models.DateField(blank=True, null=True)
    project_url = models.URLField(blank=True, help_text="Live project URL")
    github_url = models.URLField(blank=True, help_text="GitHub repository URL")

    # Technologies used
    technologies = models.CharField(
        max_length=300,
        blank=True,
        help_text="Comma-separated list of technologies (e.g., Django, PostgreSQL, Bootstrap)",
    )

    # Features
    key_features = models.TextField(blank=True, help_text="One feature per line")

    # Settings
    is_featured = models.BooleanField(
        default=False, help_text="Show in featured section"
    )
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Lower numbers appear first")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Portfolio Item"
        verbose_name_plural = "Portfolio Items"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_technologies_list(self):
        """Return technologies as a list"""
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(",")]
        return []

    def get_features_list(self):
        """Return features as a list"""
        if self.key_features:
            return [
                feature.strip()
                for feature in self.key_features.split("\n")
                if feature.strip()
            ]
        return []


# ----------------------------------------------------------
# Portfolio Image Gallery model (for additional images)
class PortfolioImage(models.Model):
    portfolio_item = models.ForeignKey(
        PortfolioItem, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ImageField(upload_to="portfolio/gallery/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Portfolio Image"
        verbose_name_plural = "Portfolio Images"

    def __str__(self):
        return f"{self.portfolio_item.title} - Image {self.order}"
