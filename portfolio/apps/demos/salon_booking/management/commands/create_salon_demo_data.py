# apps/demos/salon_booking/management/commands/create_salon_demo_data.py

from django.core.management.base import BaseCommand
from apps.demos.salon_booking.models import (
    Salon,
    ServiceCategory,
    Service,
    SalonReview,
    SalonAmenity,
    SalonOpeningHours,
)
from django.utils.text import slugify
import random


class Command(BaseCommand):
    help = "Create sample data for Salon Booking Demo"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Creating sample data..."))

        # Clear existing data
        self.stdout.write("Clearing existing demo data...")
        Salon.objects.all().delete()
        ServiceCategory.objects.all().delete()
        Service.objects.all().delete()

        # Create Service Categories
        self.stdout.write("Creating service categories...")
        categories_data = [
            {"name": "Hair Services", "icon": "bi-scissors"},
            {"name": "Facial & Skin Care", "icon": "bi-heart"},
            {"name": "Makeup", "icon": "bi-palette"},
            {"name": "Nail Services", "icon": "bi-hand-index"},
            {"name": "Massage & Spa", "icon": "bi-flower1"},
        ]

        categories = {}
        for idx, cat_data in enumerate(categories_data, 1):
            category = ServiceCategory.objects.create(
                name=cat_data["name"],
                slug=slugify(cat_data["name"]),
                icon=cat_data["icon"],
                order=idx,
                is_active=True,
            )
            categories[cat_data["name"]] = category
            self.stdout.write(f"  ✓ {category.name}")

        # Create Services
        self.stdout.write("Creating services...")
        services_data = [
            {
                "name": "Haircut & Styling",
                "category": "Hair Services",
                "duration": 45,
                "price": 250000,
            },
            {
                "name": "Hair Coloring",
                "category": "Hair Services",
                "duration": 120,
                "price": 450000,
            },
            {
                "name": "Hair Treatment",
                "category": "Hair Services",
                "duration": 60,
                "price": 350000,
            },
            {
                "name": "Keratin Treatment",
                "category": "Hair Services",
                "duration": 180,
                "price": 800000,
            },
            {
                "name": "Deep Cleansing Facial",
                "category": "Facial & Skin Care",
                "duration": 60,
                "price": 300000,
            },
            {
                "name": "Anti-Aging Facial",
                "category": "Facial & Skin Care",
                "duration": 90,
                "price": 500000,
            },
            {
                "name": "Acne Treatment",
                "category": "Facial & Skin Care",
                "duration": 45,
                "price": 280000,
            },
            {
                "name": "Bridal Makeup",
                "category": "Makeup",
                "duration": 120,
                "price": 1500000,
            },
            {
                "name": "Party Makeup",
                "category": "Makeup",
                "duration": 60,
                "price": 400000,
            },
            {
                "name": "Natural Makeup",
                "category": "Makeup",
                "duration": 45,
                "price": 300000,
            },
            {
                "name": "Manicure",
                "category": "Nail Services",
                "duration": 45,
                "price": 150000,
            },
            {
                "name": "Pedicure",
                "category": "Nail Services",
                "duration": 60,
                "price": 180000,
            },
            {
                "name": "Gel Nails",
                "category": "Nail Services",
                "duration": 90,
                "price": 350000,
            },
            {
                "name": "Full Body Massage",
                "category": "Massage & Spa",
                "duration": 90,
                "price": 600000,
            },
            {
                "name": "Hot Stone Massage",
                "category": "Massage & Spa",
                "duration": 60,
                "price": 450000,
            },
        ]

        services_list = []
        for svc_data in services_data:
            service = Service.objects.create(
                name=svc_data["name"],
                category=categories[svc_data["category"]],
                description=f"Professional {svc_data['name']} service with experienced specialists.",
                duration_minutes=svc_data["duration"],
                base_price=svc_data["price"],
                is_active=True,
            )
            services_list.append(service)
            self.stdout.write(f"  ✓ {service.name}")

        # Create Salons
        self.stdout.write("Creating salons...")
        salons_data = [
            {
                "name": "Elegance Beauty Salon",
                "zone": 1,
                "address": "Tehran, Zone 1, Vanak St.",
                "phone": "02188776655",
                "description": "Premium beauty salon offering comprehensive hair and beauty services in a luxurious environment.",
            },
            {
                "name": "Royal Style Center",
                "zone": 3,
                "address": "Tehran, Zone 3, Enghelab Ave.",
                "phone": "02166554433",
                "description": "Modern salon specializing in trendy hairstyles and professional makeup services.",
            },
            {
                "name": "Beauty Paradise",
                "zone": 5,
                "address": "Tehran, Zone 5, Satarkhan St.",
                "phone": "02144332211",
                "description": "Full-service beauty center with expert staff and state-of-the-art equipment.",
            },
            {
                "name": "Golden Touch Salon",
                "zone": 2,
                "address": "Tehran, Zone 2, Shariati Ave.",
                "phone": "02122334455",
                "description": "Specialized in bridal services and special occasion styling.",
            },
            {
                "name": "Premium Hair Studio",
                "zone": 6,
                "address": "Tehran, Zone 6, Azadi Ave.",
                "phone": "02166778899",
                "description": "High-end hair studio known for precision cuts and expert color treatments.",
            },
            {
                "name": "Serenity Spa & Beauty",
                "zone": 4,
                "address": "Tehran, Zone 4, Pasdaran St.",
                "phone": "02188990011",
                "description": "Relaxing spa environment offering beauty treatments and massage therapy.",
            },
        ]

        for salon_data in salons_data:
            salon = Salon.objects.create(
                salon_name=salon_data["name"],
                description=salon_data["description"],
                zone=salon_data["zone"],
                address=salon_data["address"],
                phone_number=salon_data["phone"],
                instagram_link=f"https://instagram.com/{slugify(salon_data['name'])}",
                is_active=True,
                view_count=random.randint(100, 500),
            )

            # Add random services to salon
            salon_services = random.sample(services_list, k=random.randint(8, 12))
            salon.services.set(salon_services)

            # Add opening hours
            for day in range(1, 8):
                if day == 7:  # Friday closed
                    SalonOpeningHours.objects.create(
                        salon=salon, day_of_week=day, is_closed=True
                    )
                else:
                    SalonOpeningHours.objects.create(
                        salon=salon,
                        day_of_week=day,
                        open_time="10:00",
                        close_time="20:00",
                        is_closed=False,
                    )

            # Add amenities
            amenities = [
                {"title": "Free Wi-Fi", "icon": "bi-wifi"},
                {"title": "Air Conditioned", "icon": "bi-snow"},
                {"title": "Parking Available", "icon": "bi-car-front"},
                {"title": "Credit Card Accepted", "icon": "bi-credit-card"},
            ]

            for amenity_data in amenities:
                SalonAmenity.objects.create(
                    salon=salon,
                    title=amenity_data["title"],
                    icon_class=amenity_data["icon"],
                    is_active=True,
                )

            # Add sample reviews
            reviews_data = [
                {
                    "name": "Sara Ahmadi",
                    "rating": 5,
                    "comment": "Excellent service and professional staff!",
                },
                {
                    "name": "Maryam Rezaei",
                    "rating": 4,
                    "comment": "Great atmosphere and quality work.",
                },
                {
                    "name": "Nazanin Karimi",
                    "rating": 5,
                    "comment": "Best salon in the area, highly recommended!",
                },
            ]

            for review_data in reviews_data:
                SalonReview.objects.create(
                    salon=salon,
                    customer_name=review_data["name"],
                    rating=review_data["rating"],
                    comment=review_data["comment"],
                    is_active=True,
                )

            self.stdout.write(f"  ✓ {salon.salon_name}")

        self.stdout.write(self.style.SUCCESS("\n✅ Sample data created successfully!"))
        self.stdout.write(self.style.SUCCESS(f"Created:"))
        self.stdout.write(f"  - {ServiceCategory.objects.count()} service categories")
        self.stdout.write(f"  - {Service.objects.count()} services")
        self.stdout.write(f"  - {Salon.objects.count()} salons")
        self.stdout.write(f"  - {SalonReview.objects.count()} reviews")
