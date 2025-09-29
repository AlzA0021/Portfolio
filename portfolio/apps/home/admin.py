# apps/home/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage, PortfolioCategory, PortfolioItem, PortfolioImage


# ----------------------------------------------------------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "subject",
        "category",
        "urgency",
        "created_at",
        "is_read",
    )
    list_filter = ("category", "urgency", "is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at",)
    list_editable = ("is_read",)

    fieldsets = (
        ("Contact Information", {"fields": ("name", "email", "phone")}),
        ("Message Details", {"fields": ("subject", "category", "urgency", "message")}),
        ("Preferences", {"fields": ("subscribe_newsletter", "is_read")}),
        ("Timestamps", {"fields": ("created_at",), "classes": ("collapse",)}),
    )


# ----------------------------------------------------------
@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "items_count", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

    def items_count(self, obj):
        count = obj.items.filter(is_active=True).count()
        return format_html(
            '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            count,
        )

    items_count.short_description = "Active Items"


# ----------------------------------------------------------
class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 1
    fields = ("image", "caption", "order", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Preview"


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail_preview",
        "title",
        "category",
        "project_date",
        "is_featured",
        "is_active",
        "order",
        "created_at",
    )
    list_editable = ("order", "is_featured", "is_active")
    list_filter = ("category", "is_featured", "is_active", "created_at")
    search_fields = ("title", "short_description", "full_description", "technologies")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    inlines = [PortfolioImageInline]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("title", "slug", "category", "short_description")},
        ),
        ("Images", {"fields": ("thumbnail", "detail_image")}),
        ("Detailed Description", {"fields": ("full_description", "key_features")}),
        (
            "Project Information",
            {
                "fields": (
                    "client",
                    "project_date",
                    "project_url",
                    "github_url",
                    "technologies",
                ),
                "classes": ("collapse",),
            },
        ),
        ("Settings", {"fields": ("is_featured", "is_active", "order")}),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
                obj.thumbnail.url,
            )
        return "-"

    thumbnail_preview.short_description = "Thumbnail"

    class Media:
        css = {"all": ("admin/css/custom_admin.css",)}


@admin.register(PortfolioImage)
class PortfolioImageAdmin(admin.ModelAdmin):
    list_display = ("portfolio_item", "image_preview", "caption", "order")
    list_filter = ("portfolio_item__category",)
    list_editable = ("order",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 5px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Preview"
