from django.contrib import admin
from .models import ContactMessage

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
