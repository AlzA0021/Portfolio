# apps/home/views.py
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import ContactForm
from .models import PortfolioCategory, PortfolioItem


# ----------------------------------------------------------
# Media settings
def media_admin(request):
    return {"media_url": settings.MEDIA_URL}


# ----------------------------------------------------------
# Index view
def index(request):
    # Get active categories and items
    categories = PortfolioCategory.objects.filter(is_active=True)
    portfolio_items = PortfolioItem.objects.filter(is_active=True).select_related(
        "category"
    )
    featured_items = portfolio_items.filter(is_featured=True)[:6]

    context = {
        "categories": categories,
        "portfolio_items": portfolio_items,
        "featured_items": featured_items,
    }
    return render(request, "home/index.html", context)


# ----------------------------------------------------------
# Portfolio detail view
def portfolio_detail(request, slug):
    portfolio_item = get_object_or_404(
        PortfolioItem.objects.select_related("category").prefetch_related(
            "gallery_images"
        ),
        slug=slug,
        is_active=True,
    )

    # Get related projects (same category)
    related_items = PortfolioItem.objects.filter(
        category=portfolio_item.category, is_active=True
    ).exclude(id=portfolio_item.pk)[:3]

    context = {
        "item": portfolio_item,
        "related_items": related_items,
        "technologies": portfolio_item.get_technologies_list(),
        "features": portfolio_item.get_features_list(),
    }
    return render(request, "home/portfolio_detail.html", context)


# ----------------------------------------------------------
# Portfolio list by category
def portfolio_by_category(request, category_slug):
    category = get_object_or_404(PortfolioCategory, slug=category_slug, is_active=True)
    items = PortfolioItem.objects.filter(category=category, is_active=True)

    context = {
        "category": category,
        "items": items,
    }
    return render(request, "home/portfolio_category.html", context)


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
