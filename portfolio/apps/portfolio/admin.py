from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ProjectCategory,
    Technology,
    Project,
    ProjectImage,
    ProjectTestimonial,
)


# ----------------------------------------------------------
# Inline for Project Images
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("image", "caption", "order", "is_active")


# ----------------------------------------------------------
# Inline for Project Testimonials
class ProjectTestimonialInline(admin.StackedInline):
    model = ProjectTestimonial
    extra = 0
    fields = (
        ("client_name", "client_position"),
        "client_company",
        "client_photo",
        "testimonial",
        "rating",
        "is_active",
    )


# ----------------------------------------------------------
# Project Category Admin
@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "project_count", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("order", "is_active")

    def project_count(self, obj):
        count = obj.projects.filter(is_active=True).count()
        return format_html(
            '<span style="background: #007bff; color: white; padding: 3px 10px; '
            'border-radius: 12px;">{}</span>',
            count,
        )

    project_count.short_description = "Active Projects"


# ----------------------------------------------------------
# Technology Admin
@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color_preview", "project_count", "order")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("order",)

    def color_preview(self, obj):
        return format_html(
            '<span style="background: {}; color: white; padding: 5px 15px; '
            'border-radius: 15px;">{}</span>',
            obj.color,
            obj.name,
        )

    color_preview.short_description = "Color Badge"

    def project_count(self, obj):
        count = obj.projects.filter(is_active=True).count()
        return count

    project_count.short_description = "Projects"


# ----------------------------------------------------------
# Project Admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail_preview",
        "title",
        "category",
        "status",
        "view_count",
        "is_featured",
        "has_live_demo",
        "is_active",
        "created_at",
    )
    list_filter = (
        "status",
        "is_featured",
        "is_active",
        "has_live_demo",
        "category",
        "technologies",
    )
    search_fields = ("title", "short_description", "full_description")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_featured", "is_active")
    readonly_fields = ("view_count", "created_at", "updated_at", "thumbnail_display")

    filter_horizontal = ("technologies",)
    inlines = [ProjectImageInline, ProjectTestimonialInline]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("title", "slug", "tagline", "category", "status")},
        ),
        (
            "Descriptions",
            {
                "fields": (
                    "short_description",
                    "full_description",
                    "key_features",
                    "challenges_solutions",
                )
            },
        ),
        (
            "Visual Content",
            {"fields": ("thumbnail", "thumbnail_display", "banner_image")},
        ),
        ("Technologies & Skills", {"fields": ("technologies",)}),
        ("Project Details", {"fields": ("client", "completion_date", "duration")}),
        (
            "Demo Integration",
            {
                "fields": ("has_live_demo", "demo_app_name", "demo_url_prefix"),
                "classes": ("collapse",),
            },
        ),
        ("External Links", {"fields": ("github_url", "live_url")}),
        ("Display Settings", {"fields": ("is_featured", "order", "is_active")}),
        (
            "Statistics & Metadata",
            {
                "fields": ("view_count", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="width: 80px; height: 60px; '
                'object-fit: cover; border-radius: 8px;" />',
                obj.thumbnail.url,
            )
        return "-"

    thumbnail_preview.short_description = "Thumbnail"

    def thumbnail_display(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-width: 400px; border-radius: 8px;" />',
                obj.thumbnail.url,
            )
        return "No thumbnail uploaded"

    thumbnail_display.short_description = "Thumbnail Preview"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            # Log or send notification for new project
            pass


# ----------------------------------------------------------
# Project Image Admin
@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("image_preview", "project", "caption", "order", "is_active")
    list_filter = ("is_active", "project")
    list_editable = ("order", "is_active")
    search_fields = ("project__title", "caption")

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 70px; '
                'object-fit: cover; border-radius: 5px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Preview"


# ----------------------------------------------------------
# Project Testimonial Admin
@admin.register(ProjectTestimonial)
class ProjectTestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "client_name",
        "client_company",
        "project",
        "rating_stars",
        "is_active",
        "created_at",
    )
    list_filter = ("rating", "is_active", "project")
    search_fields = ("client_name", "client_company", "testimonial")
    list_editable = ("is_active",)
    readonly_fields = ("created_at",)

    def rating_stars(self, obj):
        stars = "⭐" * obj.rating
        return format_html('<span style="font-size: 16px;">{}</span>', stars)

    rating_stars.short_description = "Rating"
