from django.urls import path
from .views import (
    salon_demo_home,
    SalonListView,
    SalonDetailView,
    ServiceListView,
    ServiceDetailView,
    about_demo,
)

app_name = "salon_booking"

urlpatterns = [
    # Home
    path("", salon_demo_home, name="home"),
    # Salons
    path("salons/", SalonListView.as_view(), name="salon_list"),
    path("salons/<int:salon_id>/", SalonDetailView.as_view(), name="salon_detail"),
    # Services
    path("services/", ServiceListView.as_view(), name="service_list"),
    path(
        "services/<int:service_id>/", ServiceDetailView.as_view(), name="service_detail"
    ),
    # About
    path("about/", about_demo, name="about"),
]
