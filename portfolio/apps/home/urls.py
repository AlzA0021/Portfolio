from django.urls import path
from .views import ContactView, index

#-----------------------------------------------------
app_name = "home"
urlpatterns = [
    path("",index, name="index"),
    path("contact/", ContactView.as_view(), name="contact"),
]