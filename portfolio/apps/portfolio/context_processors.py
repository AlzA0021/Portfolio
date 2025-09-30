from .models import ProjectCategory, Technology


def portfolio_context(request):
    """
    Add portfolio-related data to all templates
    """
    return {
        "portfolio_categories": ProjectCategory.objects.filter(is_active=True).order_by(
            "order"
        ),
        "portfolio_technologies": Technology.objects.all().order_by("order"),
    }
