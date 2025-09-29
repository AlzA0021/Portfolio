# apps/home/urls.py
from django.urls import path
from .views import ContactView, index, portfolio_detail, portfolio_by_category

# -----------------------------------------------------
app_name = "home"
urlpatterns = [
    path("", index, name="index"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("portfolio/<slug:slug>/", portfolio_detail, name="portfolio_detail"),
    path(
        "portfolio/category/<slug:category_slug>/",
        portfolio_by_category,
        name="portfolio_category",
    ),
]
