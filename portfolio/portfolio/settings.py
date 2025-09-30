"""
Django settings for portfolio project.
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
SECRET_KEY = "django-insecure-cm*nx9s8_^oj1mb!&(e)t$wdnaot!+ja*@i3reged8m09d$xls"

DEBUG = True

ALLOWED_HOSTS = ["fffba52e8934.ngrok-free.app", "127.0.0.1"]


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",  # ✅ برای GIS
    "django.contrib.humanize",  # ✅ برای فرمت‌های بهتر
    # Apps
    "apps.home.apps.HomeConfig",
    "apps.portfolio.apps.PortfolioConfig",  # ✅ اپ Portfolio
    "apps.demos.apps.DemosConfig",  # ✅ اپ Demo
    # Third-party
    "django_render_partial",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "portfolio.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates/")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.home.views.media_admin",
                "apps.home.context_processors.portfolio_context",
                "apps.portfolio.context_processors.portfolio_context",  # ✅ Context processor جدید
            ],
        },
    },
]

WSGI_APPLICATION = "portfolio.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",  # ✅ PostGIS برای GIS
        "NAME": "portfolio",
        "USER": "postgres",
        "PASSWORD": "1234",
        "HOST": "localhost",
        "PORT": "5432",
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static/"),)

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# GIS Libraries Path
GDAL_LIBRARY_PATH = os.environ.get("GDAL_LIBRARY_PATH", r"C:\OSGeo4W\bin\gdal311.dll")
GEOS_LIBRARY_PATH = os.environ.get("GEOS_LIBRARY_PATH", r"C:\OSGeo4W\bin\geos_c.dll")
PROJ_LIBRARY_PATH = os.environ.get("PROJ_LIBRARY_PATH", r"C:\OSGeo4W\bin\proj.dll")


# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="alirezaanari119@gmail.com")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="qzjp pvae eykn godq")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="alirezaanari119@gmail.com")

# Contact form specific settings
CONTACT_EMAIL = config("CONTACT_EMAIL", default="alirezaanari119@gmail.com")
