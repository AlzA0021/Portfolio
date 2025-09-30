from django.urls import path
from .views import (
    ProjectListView,
    ProjectDetailView,
    portfolio_home,
    projects_by_category,
    projects_by_technology,
)

app_name = "portfolio"

urlpatterns = [
    # Portfolio home/list
    path("", ProjectListView.as_view(), name="project_list"),
    path("home/", portfolio_home, name="portfolio_home"),
    # Project detail
    path("project/<slug:slug>/", ProjectDetailView.as_view(), name="project_detail"),
    # Filter by category
    path(
        "category/<slug:category_slug>/",
        projects_by_category,
        name="projects_by_category",
    ),
    # Filter by technology
    path(
        "technology/<slug:tech_slug>/",
        projects_by_technology,
        name="projects_by_technology",
    ),
]
