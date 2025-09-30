from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from .models import Project, ProjectCategory, Technology


# ----------------------------------------------------------
# Portfolio List View
class ProjectListView(ListView):
    model = Project
    template_name = "portfolio/project_list.html"
    context_object_name = "projects"
    paginate_by = 9

    def get_queryset(self):
        queryset = Project.objects.filter(is_active=True).select_related("category")
        queryset = queryset.prefetch_related("technologies", "gallery_images")

        # Filter by category
        category_slug = self.request.GET.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Filter by technology
        tech_slug = self.request.GET.get("tech")
        if tech_slug:
            queryset = queryset.filter(technologies__slug=tech_slug)

        # Filter by status
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)

        # Search
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(short_description__icontains=search_query)
                | Q(full_description__icontains=search_query)
            )

        # Featured first
        queryset = queryset.order_by("-is_featured", "order", "-created_at")

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all categories with project count
        context["categories"] = (
            ProjectCategory.objects.filter(is_active=True)
            .annotate(
                project_count=Count("projects", filter=Q(projects__is_active=True))
            )
            .order_by("order")
        )

        # Get all technologies
        context["technologies"] = (
            Technology.objects.all()
            .annotate(
                project_count=Count("projects", filter=Q(projects__is_active=True))
            )
            .order_by("order")
        )

        # Current filters
        context["current_category"] = self.request.GET.get("category", "")
        context["current_tech"] = self.request.GET.get("tech", "")
        context["current_status"] = self.request.GET.get("status", "")
        context["search_query"] = self.request.GET.get("search", "")

        # Stats
        context["total_projects"] = Project.objects.filter(is_active=True).count()
        context["featured_projects"] = Project.objects.filter(
            is_active=True, is_featured=True
        ).count()

        return context


# ----------------------------------------------------------
# Portfolio Detail View
class ProjectDetailView(DetailView):
    model = Project
    template_name = "portfolio/project_detail.html"
    context_object_name = "project"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return (
            Project.objects.filter(is_active=True)
            .select_related("category")
            .prefetch_related("technologies", "gallery_images", "testimonials")
        )

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment view count (you might want to add session-based tracking)
        obj.increment_view_count()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        # Related projects (same category, excluding current)
        context["related_projects"] = (
            Project.objects.filter(category=project.category, is_active=True)
            .exclude(pk=project.pk)
            .order_by("-is_featured", "?")[:3]
        )

        # Next and Previous projects
        context["next_project"] = (
            Project.objects.filter(is_active=True, created_at__lt=project.created_at)
            .order_by("-created_at")
            .first()
        )

        context["prev_project"] = (
            Project.objects.filter(is_active=True, created_at__gt=project.created_at)
            .order_by("created_at")
            .first()
        )

        # Get active testimonials
        context["testimonials"] = project.testimonials.filter(is_active=True)

        # Get gallery images
        context["gallery_images"] = project.gallery_images.filter(is_active=True)

        return context


# ----------------------------------------------------------
# Function-based view alternative (if you prefer)
def portfolio_home(request):
    """Portfolio homepage with featured projects"""
    featured_projects = (
        Project.objects.filter(is_active=True, is_featured=True)
        .select_related("category")
        .prefetch_related("technologies")[:6]
    )

    recent_projects = Project.objects.filter(is_active=True).order_by("-created_at")[:6]

    categories = ProjectCategory.objects.filter(is_active=True).annotate(
        project_count=Count("projects", filter=Q(projects__is_active=True))
    )

    context = {
        "featured_projects": featured_projects,
        "recent_projects": recent_projects,
        "categories": categories,
        "total_projects": Project.objects.filter(is_active=True).count(),
    }

    return render(request, "portfolio/portfolio_home.html", context)


# ----------------------------------------------------------
# Projects by Category
def projects_by_category(request, category_slug):
    """Filter projects by category"""
    category = get_object_or_404(ProjectCategory, slug=category_slug, is_active=True)

    projects = (
        Project.objects.filter(category=category, is_active=True)
        .select_related("category")
        .prefetch_related("technologies")
    )

    context = {
        "category": category,
        "projects": projects,
        "project_count": projects.count(),
    }

    return render(request, "portfolio/projects_by_category.html", context)


# ----------------------------------------------------------
# Projects by Technology
def projects_by_technology(request, tech_slug):
    """Filter projects by technology"""
    technology = get_object_or_404(Technology, slug=tech_slug)

    projects = (
        Project.objects.filter(technologies=technology, is_active=True)
        .select_related("category")
        .prefetch_related("technologies")
    )

    context = {
        "technology": technology,
        "projects": projects,
        "project_count": projects.count(),
    }

    return render(request, "portfolio/projects_by_technology.html", context)
