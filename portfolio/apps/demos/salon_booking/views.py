from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count, Avg
from .models import Salon, Service, ServiceCategory, SalonReview


# ----------------------------------------------------------
# Demo Home View
def salon_demo_home(request):
    """
    Homepage for Salon Booking Demo
    Shows featured salons and services
    """
    featured_salons = Salon.objects.filter(is_active=True).order_by("-view_count")[:6]
    popular_services = Service.objects.filter(is_active=True)[:8]
    service_categories = ServiceCategory.objects.filter(is_active=True)

    # Stats
    total_salons = Salon.objects.filter(is_active=True).count()
    total_services = Service.objects.filter(is_active=True).count()

    context = {
        "featured_salons": featured_salons,
        "popular_services": popular_services,
        "service_categories": service_categories,
        "total_salons": total_salons,
        "total_services": total_services,
        "page_title": "Salon Booking Platform Demo",
    }

    return render(request, "demos/salon_booking/home.html", context)


# ----------------------------------------------------------
# Salon List View
class SalonListView(ListView):
    model = Salon
    template_name = "demos/salon_booking/salon_list.html"
    context_object_name = "salons"
    paginate_by = 12

    def get_queryset(self):
        queryset = Salon.objects.filter(is_active=True)
        queryset = queryset.prefetch_related(
            "gallery_images", "services", "reviews", "amenities"
        )

        # Filter by zone
        zone = self.request.GET.get("zone")
        if zone:
            queryset = queryset.filter(zone=zone)

        # Filter by service
        service_id = self.request.GET.get("service")
        if service_id:
            queryset = queryset.filter(services__id=service_id)

        # Search
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(salon_name__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(address__icontains=search_query)
            )

        # Sort
        sort_by = self.request.GET.get("sort", "-view_count")
        if sort_by == "name":
            queryset = queryset.order_by("salon_name")
        elif sort_by == "rating":
            # Add rating annotation
            queryset = queryset.annotate(
                avg_rating=Avg("reviews__rating", filter=Q(reviews__is_active=True))
            ).order_by("-avg_rating")
        elif sort_by == "newest":
            queryset = queryset.order_by("-registered_date")
        else:  # default: popular
            queryset = queryset.order_by("-view_count")

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all zones
        zones = (
            Salon.objects.filter(is_active=True)
            .values_list("zone", flat=True)
            .distinct()
            .order_by("zone")
        )
        context["zones"] = [z for z in zones if z is not None]

        # Get all services
        context["services"] = Service.objects.filter(is_active=True)

        # Current filters
        context["current_zone"] = self.request.GET.get("zone", "")
        context["current_service"] = self.request.GET.get("service", "")
        context["search_query"] = self.request.GET.get("search", "")
        context["current_sort"] = self.request.GET.get("sort", "-view_count")

        context["page_title"] = "Browse Salons"

        return context


# ----------------------------------------------------------
# Salon Detail View
class SalonDetailView(DetailView):
    model = Salon
    template_name = "demos/salon_booking/salon_detail.html"
    context_object_name = "salon"
    slug_field = "id"
    slug_url_kwarg = "salon_id"

    def get_queryset(self):
        return Salon.objects.filter(is_active=True).prefetch_related(
            "gallery_images",
            "services",
            "services__category",
            "reviews",
            "amenities",
            "opening_hours",
        )

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment view count
        obj.increment_view_count()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        salon = self.object

        # Get gallery images
        context["gallery_images"] = salon.gallery_images.filter(is_active=True)

        # Get cover image
        cover_image = salon.gallery_images.filter(is_cover=True, is_active=True).first()
        context["cover_image"] = cover_image

        # Get services grouped by category
        services = salon.services.filter(is_active=True).select_related("category")
        services_by_category = {}
        for service in services:
            category_name = service.category.name if service.category else "Other"
            if category_name not in services_by_category:
                services_by_category[category_name] = []
            services_by_category[category_name].append(service)
        context["services_by_category"] = services_by_category

        # Get reviews
        reviews = salon.reviews.filter(is_active=True).order_by("-created_at")
        context["reviews"] = reviews[:5]  # Show latest 5
        context["total_reviews"] = reviews.count()

        # Get amenities
        context["amenities"] = salon.amenities.filter(is_active=True)

        # Get opening hours
        opening_hours = salon.opening_hours.all().order_by("day_of_week")
        context["opening_hours"] = opening_hours

        # Related salons (same zone)
        context["related_salons"] = (
            Salon.objects.filter(zone=salon.zone, is_active=True)
            .exclude(id=salon.id)
            .order_by("?")[:3]
        )

        context["page_title"] = salon.salon_name

        return context


# ----------------------------------------------------------
# Service List View
class ServiceListView(ListView):
    model = Service
    template_name = "demos/salon_booking/service_list.html"
    context_object_name = "services"
    paginate_by = 16

    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True).select_related("category")
        queryset = queryset.prefetch_related("salons")

        # Filter by category
        category_slug = self.request.GET.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Search
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

        # Price range
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        if min_price:
            queryset = queryset.filter(base_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(base_price__lte=max_price)

        return queryset.order_by("category", "name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all categories
        context["categories"] = ServiceCategory.objects.filter(is_active=True)

        # Current filters
        context["current_category"] = self.request.GET.get("category", "")
        context["search_query"] = self.request.GET.get("search", "")

        context["page_title"] = "Our Services"

        return context


# ----------------------------------------------------------
# Service Detail View
class ServiceDetailView(DetailView):
    model = Service
    template_name = "demos/salon_booking/service_detail.html"
    context_object_name = "service"
    slug_field = "id"
    slug_url_kwarg = "service_id"

    def get_queryset(self):
        return (
            Service.objects.filter(is_active=True)
            .select_related("category")
            .prefetch_related("salons")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.object

        # Get salons offering this service
        context["salons"] = service.salons.filter(is_active=True)

        # Related services (same category)
        context["related_services"] = (
            Service.objects.filter(category=service.category, is_active=True)
            .exclude(id=service.id)
            .order_by("?")[:4]
        )

        context["page_title"] = service.name

        return context


# ----------------------------------------------------------
# About Demo View
def about_demo(request):
    """
    About page explaining this demo
    """
    context = {
        "page_title": "About This Demo",
    }
    return render(request, "demos/salon_booking/about.html", context)
