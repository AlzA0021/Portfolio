from django.db import models
from django.utils.text import slugify
from django.urls import reverse


# ----------------------------------------------------------
# Project Category
class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")
    icon_class = models.CharField(
        max_length=50,
        blank=True,
        help_text="Bootstrap Icon class (e.g., 'bi-laptop')",
        verbose_name="Icon Class",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"
        ordering = ["order", "name"]
        db_table = "portfolio_category"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ----------------------------------------------------------
# Technology/Tool
class Technology(models.Model):
    name = models.CharField(max_length=50, verbose_name="Technology Name")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Icon class or image path",
        verbose_name="Icon",
    )
    color = models.CharField(
        max_length=7,
        default="#007bff",
        help_text="Hex color code (e.g., #007bff)",
        verbose_name="Badge Color",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")

    class Meta:
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"
        ordering = ["order", "name"]
        db_table = "portfolio_technology"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ----------------------------------------------------------
# Main Project Model
class Project(models.Model):
    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("in_progress", "In Progress"),
        ("demo", "Demo/Showcase"),
    ]

    # Basic Info
    title = models.CharField(max_length=200, verbose_name="Project Title")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    tagline = models.CharField(
        max_length=250,
        blank=True,
        help_text="Short catchy description (one line)",
        verbose_name="Tagline",
    )

    # Descriptions
    short_description = models.TextField(
        max_length=500,
        help_text="Brief description for cards (2-3 lines)",
        verbose_name="Short Description",
    )
    full_description = models.TextField(verbose_name="Full Description")

    # Visual Content
    thumbnail = models.ImageField(
        upload_to="portfolio/thumbnails/",
        help_text="Main project image (recommended: 800x600)",
        verbose_name="Thumbnail",
    )
    banner_image = models.ImageField(
        upload_to="portfolio/banners/",
        blank=True,
        null=True,
        help_text="Large banner for detail page (recommended: 1920x600)",
        verbose_name="Banner Image",
    )

    # Categorization
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="projects",
        verbose_name="Category",
    )
    technologies = models.ManyToManyField(
        Technology, related_name="projects", verbose_name="Technologies Used"
    )

    # Project Details
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="completed",
        verbose_name="Project Status",
    )
    client = models.CharField(max_length=200, blank=True, verbose_name="Client Name")
    completion_date = models.DateField(
        null=True, blank=True, verbose_name="Completion Date"
    )
    duration = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g., '3 months', '6 weeks'",
        verbose_name="Project Duration",
    )

    # Features & Challenges
    key_features = models.TextField(
        blank=True, help_text="One feature per line", verbose_name="Key Features"
    )
    challenges_solutions = models.TextField(
        blank=True,
        help_text="Describe challenges faced and solutions implemented",
        verbose_name="Challenges & Solutions",
    )

    # Demo Integration
    has_live_demo = models.BooleanField(
        default=False,
        verbose_name="Has Live Demo",
        help_text="Does this project have a live demo in this portfolio?",
    )
    demo_app_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Django app name for demo (e.g., 'salon_booking')",
        verbose_name="Demo App Name",
    )
    demo_url_prefix = models.CharField(
        max_length=100,
        blank=True,
        help_text="URL prefix for demo (e.g., 'salon-demo')",
        verbose_name="Demo URL Prefix",
    )

    # External Links
    github_url = models.URLField(blank=True, verbose_name="GitHub URL")
    live_url = models.URLField(blank=True, verbose_name="Live Project URL")

    # SEO & Metadata
    view_count = models.PositiveIntegerField(default=0, verbose_name="View Count")
    is_featured = models.BooleanField(default=False, verbose_name="Featured Project")
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["-is_featured", "order", "-created_at"]
        db_table = "portfolio_project"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})

    def get_demo_url(self):
        if self.has_live_demo and self.demo_url_prefix:
            return reverse("demos:salon_home")  # این رو بعداً تنظیم می‌کنیم
        return None

    def get_features_list(self):
        """Return key features as a list"""
        if self.key_features:
            return [f.strip() for f in self.key_features.split("\n") if f.strip()]
        return []

    def increment_view_count(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=["view_count"])


# ----------------------------------------------------------
# Project Images Gallery
class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="gallery_images",
        verbose_name="Project",
    )
    image = models.ImageField(upload_to="portfolio/gallery/", verbose_name="Image")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Caption")
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"
        ordering = ["order"]
        db_table = "portfolio_project_image"

    def __str__(self):
        return f"{self.project.title} - Image {self.order}"


# ----------------------------------------------------------
# Project Testimonial/Review
class ProjectTestimonial(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="testimonials",
        verbose_name="Project",
    )
    client_name = models.CharField(max_length=100, verbose_name="Client Name")
    client_position = models.CharField(
        max_length=100, blank=True, verbose_name="Client Position"
    )
    client_company = models.CharField(
        max_length=100, blank=True, verbose_name="Client Company"
    )
    client_photo = models.ImageField(
        upload_to="portfolio/testimonials/",
        blank=True,
        null=True,
        verbose_name="Client Photo",
    )
    testimonial = models.TextField(verbose_name="Testimonial Text")
    rating = models.PositiveSmallIntegerField(
        default=5,
        choices=[(i, f"{i} Stars") for i in range(1, 6)],
        verbose_name="Rating",
    )
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Project Testimonial"
        verbose_name_plural = "Project Testimonials"
        ordering = ["-created_at"]
        db_table = "portfolio_testimonial"

    def __str__(self):
        return f"{self.client_name} - {self.project.title}"
