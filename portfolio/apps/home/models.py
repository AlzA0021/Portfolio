from django.db import models
from django.utils import timezone

#----------------------------------------------------------
# ContactMessage model
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
