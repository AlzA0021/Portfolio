# forms.py (Updated with save method)
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .models import ContactMessage
import re


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your full name",
                "required": True,
            }
        ),
        validators=[
            MinLengthValidator(2, message="Name must be at least 2 characters long")
        ],
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email address",
                "required": True,
            }
        ),
        error_messages={
            "invalid": "Please enter a valid email address.",
            "required": "Email field is required.",
        },
    )

    phone = forms.CharField(
        max_length=15,
        required=False,
        label="Phone Number (Optional)",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+1234567890", "type": "tel"}
        ),
    )

    subject = forms.CharField(
        max_length=150,
        label="Subject",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Brief subject of your message",
                "required": True,
            }
        ),
        validators=[
            MinLengthValidator(5, message="Subject must be at least 5 characters long")
        ],
    )

    category = forms.ChoiceField(
        choices=[
            ("general", "General Inquiry"),
            ("support", "Technical Support"),
            ("business", "Business Partnership"),
            ("feedback", "Feedback"),
            ("other", "Other"),
        ],
        label="Category",
        widget=forms.Select(attrs={"class": "form-select"}),
        initial="general",
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 6,
                "cols": 50,
                "placeholder": "Write your detailed message here...",
                "class": "form-control",
                "required": True,
            }
        ),
        label="Message",
        validators=[
            MinLengthValidator(
                10, message="Message must be at least 10 characters long"
            )
        ],
    )

    urgency = forms.ChoiceField(
        choices=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("urgent", "Urgent"),
        ],
        label="Urgency Level",
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        initial="medium",
    )

    subscribe_newsletter = forms.BooleanField(
        required=False,
        label="Subscribe to our newsletter",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    consent = forms.BooleanField(
        required=True,
        label="I agree to the Terms of Service and Privacy Policy",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        error_messages={"required": "You must agree to the terms to proceed."},
    )

    def clean_name(self):
        name = self.cleaned_data["name"]
        name = " ".join(name.split())
        if not re.match(r"^[a-zA-Z\s\u0600-\u06FF]+$", name):
            raise ValidationError("Name can only contain letters and spaces.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone:
            phone = re.sub(r"[^\d+]", "", phone)
            if not re.match(r"^\+?[\d]{7,15}$", phone):
                raise ValidationError("Please enter a valid phone number.")
        return phone

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email and not email.lower().endswith(
            (".com", ".org", ".net", ".edu", ".gov", ".ir")
        ):
            raise ValidationError("Please use a valid email domain.")
        return email.lower()

    def save_to_database(self):
        """Save form data to database"""
        contact = ContactMessage(
            name=self.cleaned_data["name"],
            email=self.cleaned_data["email"],
            phone=self.cleaned_data.get("phone", ""),
            subject=self.cleaned_data["subject"],
            category=self.cleaned_data["category"],
            message=self.cleaned_data["message"],
            urgency=self.cleaned_data["urgency"],
            subscribe_newsletter=self.cleaned_data["subscribe_newsletter"],
        )
        contact.save()
        return contact

    def send_email(self):
        """Send email notification"""
        try:
            # Email to admin
            admin_subject = f"New Contact Form: {self.cleaned_data['subject']}"
            admin_message = f"""
                New contact form submission:

                Name: {self.cleaned_data['name']}
                Email: {self.cleaned_data['email']}
                Phone: {self.cleaned_data.get('phone', 'Not provided')}
                Category: {self.cleaned_data['category']}
                Urgency: {self.cleaned_data['urgency']}

                Message:
                {self.cleaned_data['message']}

                Newsletter Subscription: {'Yes' if self.cleaned_data['subscribe_newsletter'] else 'No'}
                            """

            send_mail(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )

            # Thank you email to user
            user_subject = "Thank you for contacting us"
            user_message = f"""
                Dear {self.cleaned_data['name']},

                Thank you for your message. We have received your inquiry regarding "{self.cleaned_data['subject']}" and will get back to you as soon as possible.

                Best regards,
                The Team
                            """

            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [self.cleaned_data["email"]],
                fail_silently=True,
            )

            return True
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False
