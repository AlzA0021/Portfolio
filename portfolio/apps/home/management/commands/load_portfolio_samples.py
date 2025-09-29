# apps/home/management/commands/load_portfolio_samples.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.home.models import PortfolioCategory, PortfolioItem
from datetime import datetime


class Command(BaseCommand):
    help = "Load sample portfolio data for testing"

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.SUCCESS("Starting to load sample portfolio data...")
        )

        # Create Categories
        categories_data = [
            {
                "name": "Web Applications",
                "slug": "web-applications",
                "description": "Full-stack web applications built with Django and modern frontend technologies",
                "order": 1,
            },
            {
                "name": "API Development",
                "slug": "api-development",
                "description": "RESTful APIs and backend services",
                "order": 2,
            },
            {
                "name": "E-commerce",
                "slug": "e-commerce",
                "description": "Online shopping platforms and payment integrations",
                "order": 3,
            },
            {
                "name": "Booking Systems",
                "slug": "booking-systems",
                "description": "Reservation and appointment booking solutions",
                "order": 4,
            },
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = PortfolioCategory.objects.get_or_create(
                slug=cat_data["slug"], defaults=cat_data
            )
            categories[cat_data["slug"]] = category
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Created category: {category.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"- Category already exists: {category.name}")
                )

        # Create Sample Portfolio Items
        portfolio_items_data = [
            {
                "title": "Beauty Salon Booking System",
                "slug": "beauty-salon-booking-system",
                "category": "booking-systems",
                "short_description": "A comprehensive online appointment booking platform for beauty salons with payment gateway integration",
                "full_description": """A full-featured booking system designed specifically for beauty salons and spas. 
                
The system allows customers to browse available services, view stylist profiles, check real-time availability, and book appointments online. It includes a sophisticated calendar management system that handles multiple stylists, services, and time slots.

The admin panel provides salon owners with complete control over their business, including service management, staff scheduling, customer management, and detailed analytics.

Built with Django and PostgreSQL, the system is highly scalable and can handle multiple salon locations. Integration with popular payment gateways ensures secure transactions.""",
                "client": "Beauty Paradise Salon",
                "project_date": datetime(2024, 8, 15).date(),
                "project_url": "https://example.com/beauty-booking",
                "github_url": "https://github.com/yourusername/beauty-booking",
                "technologies": "Django, PostgreSQL, Redis, Celery, Bootstrap, JavaScript, Stripe API, Google Calendar API",
                "key_features": """Real-time availability checking
Multiple service and stylist selection
Automated email/SMS notifications
Payment gateway integration (Stripe)
Customer review and rating system
Admin dashboard with analytics
Multi-location support
Loyalty points system
Calendar synchronization
Mobile-responsive design""",
                "is_featured": True,
                "order": 1,
            },
            {
                "title": "E-commerce Platform",
                "slug": "e-commerce-platform",
                "category": "e-commerce",
                "short_description": "Modern online shopping platform with advanced features and seamless checkout experience",
                "full_description": """A robust e-commerce platform built to handle high traffic and provide excellent user experience.

Features include product catalog management, advanced search and filtering, shopping cart, wishlist, order management, and multiple payment options. The platform supports multiple currencies and languages.

Integrated with modern payment gateways and shipping providers for seamless order fulfillment. Admin panel includes inventory management, order processing, customer management, and comprehensive reporting.""",
                "client": "TechMart Online",
                "project_date": datetime(2024, 6, 20).date(),
                "project_url": "",
                "github_url": "",
                "technologies": "Django, PostgreSQL, Redis, Elasticsearch, React, Docker, AWS S3",
                "key_features": """Product catalog with categories
Advanced search and filters
Shopping cart and wishlist
Multiple payment gateways
Order tracking system
Customer accounts
Inventory management
Discount and coupon system
Product reviews and ratings
Admin analytics dashboard""",
                "is_featured": True,
                "order": 2,
            },
            {
                "title": "Task Management API",
                "slug": "task-management-api",
                "category": "api-development",
                "short_description": "RESTful API for project and task management with team collaboration features",
                "full_description": """A comprehensive REST API for task and project management designed for team collaboration.

The API provides endpoints for user management, project creation, task assignment, time tracking, and team communication. Built with Django REST Framework, it follows best practices for API design and includes comprehensive documentation.

Features JWT authentication, role-based permissions, real-time notifications, and WebSocket support for live updates. Optimized for performance with caching and efficient database queries.""",
                "client": "Internal Project",
                "project_date": datetime(2024, 5, 10).date(),
                "project_url": "https://api.example.com/docs",
                "github_url": "https://github.com/yourusername/task-api",
                "technologies": "Django REST Framework, PostgreSQL, Redis, Celery, JWT, WebSockets, Docker",
                "key_features": """RESTful API design
JWT authentication
Role-based permissions
Real-time notifications
WebSocket support
Comprehensive API documentation
Task assignment and tracking
Time tracking
Team collaboration
File attachments""",
                "is_featured": True,
                "order": 3,
            },
            {
                "title": "Restaurant Management System",
                "slug": "restaurant-management-system",
                "category": "web-applications",
                "short_description": "Complete restaurant management solution with POS, inventory, and online ordering",
                "full_description": """An all-in-one restaurant management system that handles everything from order taking to inventory management.

The system includes a POS interface for quick order entry, kitchen display system for order management, table management, inventory tracking, and employee scheduling. Customers can also place orders online through an integrated web interface.

Built with scalability in mind, the system can handle multiple restaurant locations and provides real-time synchronization across all devices.""",
                "client": "Gourmet Kitchen",
                "project_date": datetime(2024, 4, 5).date(),
                "project_url": "",
                "github_url": "",
                "technologies": "Django, PostgreSQL, Redis, Vue.js, WebSockets, Thermal Printer API",
                "key_features": """POS system
Kitchen display system
Table management
Online ordering
Inventory tracking
Employee scheduling
Sales reports
Menu management
Customer database
Multi-location support""",
                "is_featured": False,
                "order": 4,
            },
            {
                "title": "Learning Management System",
                "slug": "learning-management-system",
                "category": "web-applications",
                "short_description": "Educational platform for online courses with video streaming and progress tracking",
                "full_description": """A modern learning management system designed for online education and corporate training.

Features include course creation tools, video hosting and streaming, quizzes and assignments, progress tracking, certificates, and student forums. Instructors can create rich content with multimedia support.

The platform supports both live and recorded classes, includes a messaging system for student-teacher communication, and provides detailed analytics on student performance.""",
                "client": "EduTech Academy",
                "project_date": datetime(2024, 3, 15).date(),
                "project_url": "https://example.com/lms",
                "github_url": "",
                "technologies": "Django, PostgreSQL, Redis, FFmpeg, AWS S3, Stripe, Bootstrap",
                "key_features": """Course management
Video streaming
Quiz and assignments
Progress tracking
Certificates generation
Student forums
Live classes support
Payment integration
Mobile responsive
Advanced analytics""",
                "is_featured": False,
                "order": 5,
            },
            {
                "title": "Real Estate Listing Platform",
                "slug": "real-estate-listing-platform",
                "category": "web-applications",
                "short_description": "Property listing and search platform with advanced filters and map integration",
                "full_description": """A comprehensive real estate platform connecting buyers, sellers, and agents.

The platform allows property owners to list their properties with detailed information, photos, and virtual tours. Buyers can search properties using advanced filters, save favorites, and contact agents directly.

Features include map-based search with Google Maps integration, mortgage calculator, property comparison tool, and agent profiles. The admin panel provides tools for property verification and user management.""",
                "client": "Prime Properties",
                "project_date": datetime(2024, 2, 20).date(),
                "project_url": "",
                "github_url": "",
                "technologies": "Django, PostgreSQL, Elasticsearch, Google Maps API, AWS S3, Bootstrap",
                "key_features": """Property listings
Advanced search filters
Map integration
Virtual tours
Mortgage calculator
Property comparison
Agent profiles
Favorites and alerts
Contact management
Admin verification system""",
                "is_featured": False,
                "order": 6,
            },
        ]

        for item_data in portfolio_items_data:
            category_slug = item_data.pop("category")
            item_data["category"] = categories[category_slug]

            portfolio_item, created = PortfolioItem.objects.get_or_create(
                slug=item_data["slug"], defaults=item_data
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Created portfolio item: {portfolio_item.title}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"- Portfolio item already exists: {portfolio_item.title}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("\n✅ Sample data loading completed!"))
        self.stdout.write(
            self.style.SUCCESS(f"Total categories: {PortfolioCategory.objects.count()}")
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Total portfolio items: {PortfolioItem.objects.count()}"
            )
        )
        self.stdout.write(
            self.style.WARNING(
                "\n⚠️  Note: You still need to upload images for each portfolio item through the admin panel."
            )
        )
