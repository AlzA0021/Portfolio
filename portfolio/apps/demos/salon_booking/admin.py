from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Salon,
    SalonGallery,
    SalonOpeningHours,
    ServiceCategory,
    Service,
    SalonReview,
    SalonAmenity,
)


# ----------------------------------------------------------
# Inlines
class SalonGalleryInline(admin.TabularInline):
    model = SalonGallery
    extra = 1
    fields = ("image", "caption", "order", "is_cover", "is_active")


class SalonOpeningHoursInline(admin.TabularInline):
    model = SalonOpeningHours
    extra = 0
    fields = ("day_of_week", "open_time", "close_time", "is_closed")


class SalonAmenityInline(admin.TabularInline):
    model = SalonAmenity
    extra = 1
    fields = ("title", "icon_class", "description", "is_active")


class SalonReviewInline(admin.TabularInline):
    model = SalonReview
    extra = 0
    readonly_fields = ("created_at",)
    fields = ("customer_name", "rating", "comment", "is_active", "created_at")


# ----------------------------------------------------------
# Salon Admin
@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = (
        "banner_preview",
        "salon_name",
        "zone",
        "phone_number",
        "average_rating",
        "view_count",
        "is_active",
        "registered_date",
    )
    list_filter = ("is_active", "zone", "registered_date")
    search_fields = ("salon_name", "description", "address")
    list_editable = ("is_active",)
    readonly_fields = ("view_count", "registered_date", "banner_display")

    inlines = [
        SalonGalleryInline,
        SalonOpeningHoursInline,
        SalonAmenityInline,
        SalonReviewInline,
    ]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("salon_name", "description", "banner_image", "banner_display")},
        ),
        ("Location", {"fields": ("zone", "address")}),
        (
            "Contact Information",
            {"fields": ("phone_number", "instagram_link", "telegram_link")},
        ),
        (
            "Status & Statistics",
            {"fields": ("is_active", "view_count", "registered_date")},
        ),
    )

    def banner_preview(self, obj):
        if obj.banner_image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 60px; '
                'object-fit: cover; border-radius: 5px;" />',
                obj.banner_image.url,
            )
        return "-"

    banner_preview.short_description = "Banner"

    def banner_display(self, obj):
        if obj.banner_image:
            return format_html(
                '<img src="{}" style="max-width: 600px; border-radius: 10px;" />',
                obj.banner_image.url,
            )
        return "No banner uploaded"

    banner_display.short_description = "Banner Preview"

    def average_rating(self, obj):
        avg = obj.get_average_score()
        if avg:
            stars = "⭐" * int(avg)
            return format_html(
                '<span style="font-size: 14px;">{} ({})</span>', stars, avg
            )
        return "No ratings"

    average_rating.short_description = "Rating"


# ----------------------------------------------------------
# Salon Gallery Admin
@admin.register(SalonGallery)
class SalonGalleryAdmin(admin.ModelAdmin):
    list_display = (
        "image_preview",
        "salon",
        "caption",
        "order",
        "is_cover",
        "is_active",
    )
    list_filter = ("is_cover", "is_active", "salon")
    list_editable = ("order", "is_cover", "is_active")
    search_fields = ("salon__salon_name", "caption")

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 120px; height: 80px; '
                'object-fit: cover; border-radius: 5px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Image"


# ----------------------------------------------------------
# Service Category Admin
@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "service_count", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("order", "is_active")

    def service_count(self, obj):
        count = obj.services.filter(is_active=True).count()
        return format_html(
            '<span style="background: #28a745; color: white; padding: 3px 10px; '
            'border-radius: 12px;">{}</span>',
            count,
        )

    service_count.short_description = "Services"


# ----------------------------------------------------------
# Service Admin
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "image_preview",
        "name",
        "category",
        "duration_minutes",
        "base_price",
        "salon_count",
        "is_active",
        "created_at",
    )
    list_filter = ("category", "is_active", "created_at")
    search_fields = ("name", "description")
    list_editable = ("is_active",)
    filter_horizontal = ("salons",)
    readonly_fields = ("created_at", "image_display")

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "category", "description", "image", "image_display")},
        ),
        ("Pricing & Duration", {"fields": ("base_price", "duration_minutes")}),
        ("Availability", {"fields": ("salons", "is_active")}),
        ("Metadata", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; '
                'object-fit: cover; border-radius: 5px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Image"

    def image_display(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 400px; border-radius: 10px;" />',
                obj.image.url,
            )
        return "No image uploaded"

    image_display.short_description = "Service Image"

    def salon_count(self, obj):
        count = obj.salons.filter(is_active=True).count()
        return count

    salon_count.short_description = "Salons"


# ----------------------------------------------------------
# Salon Review Admin
@admin.register(SalonReview)
class SalonReviewAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "salon", "rating_stars", "is_active", "created_at")
    list_filter = ("rating", "is_active", "salon", "created_at")
    search_fields = ("customer_name", "comment", "salon__salon_name")
    list_editable = ("is_active",)
    readonly_fields = ("created_at",)

    fieldsets = (
        (
            "Review Information",
            {"fields": ("salon", "customer_name", "rating", "comment")},
        ),
        ("Moderation", {"fields": ("is_active", "created_at")}),
    )

    def rating_stars(self, obj):
        stars = "⭐" * obj.rating
        return format_html('<span style="font-size: 16px;">{}</span>', stars)

    rating_stars.short_description = "Rating"


# ----------------------------------------------------------
# Salon Amenity Admin
@admin.register(SalonAmenity)
class SalonAmenityAdmin(admin.ModelAdmin):
    list_display = ("title", "salon", "icon_class", "is_active")
    list_filter = ("is_active", "salon")
    search_fields = ("title", "description", "salon__salon_name")
    list_editable = ("is_active",)


# ----------------------------------------------------------
# Salon Opening Hours Admin
@admin.register(SalonOpeningHours)
class SalonOpeningHoursAdmin(admin.ModelAdmin):
    list_display = ("salon", "day_of_week", "open_time", "close_time", "is_closed")
    list_filter = ("day_of_week", "is_closed", "salon")
    search_fields = ("salon__salon_name",)
    list_editable = ("open_time", "close_time", "is_closed")
