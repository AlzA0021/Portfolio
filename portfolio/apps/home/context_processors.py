# apps/home/context_processors.py

from .models import PortfolioCategory, PortfolioItem


def portfolio_context(request):
    """
    Context processor to make portfolio data available in all templates
    """
    return {
        "all_portfolio_categories": PortfolioCategory.objects.filter(is_active=True),
        "featured_portfolio_items": PortfolioItem.objects.filter(
            is_active=True, is_featured=True
        ).select_related("category")[:6],
        "portfolio_items_count": PortfolioItem.objects.filter(is_active=True).count(),
    }
