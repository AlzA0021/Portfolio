from django.shortcuts import render
from django.conf import settings
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import ContactForm

# ----------------------------------------------------------
# Media settings
def media_admin(request):
    return {"media_url": settings.MEDIA_URL}

# ----------------------------------------------------------
# Index view
def index(request):
    return render(request, "home/index.html")

# ----------------------------------------------------------
# Contact view
class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(
            request, "home/partials/contact.html", {"form": form, "success": None}
        )

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            try:
                # Save to database
                contact_message = form.save_to_database()

                # Send email
                email_sent = form.send_email()

                if email_sent:
                    messages.success(
                        request, "Your message has been sent successfully!"
                    )
                else:
                    messages.warning(
                        request, "Message saved but email notification failed."
                    )

                # For AJAX requests
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse(
                        {
                            "success": True,
                            "message": "Your message has been sent successfully!",
                        }
                    )

                return render(
                    request,
                    "home/partials/contact.html",
                    {"form": ContactForm(), "success": True},  # Fresh form
                )

            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse(
                        {"success": False, "message": f"An error occurred: {str(e)}"}
                    )
        else:
            # Form has validation errors
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "success": False,
                        "errors": form.errors,
                        "message": "Please correct the errors below.",
                    }
                )

        return render(
            request, "home/partials/contact.html", {"form": form, "success": False}
        )
