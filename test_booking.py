
from app import create_app
from app.extensions import db
from app.models import User, ServiceCategory, ProviderProfile, Booking, Review

app = create_app()

with app.app_context():
    customer = User.query.filter_by(
        email="customer@example.com"
    ).first()

    provider = User.query.filter_by(
        email="provider@example.com"
    ).first()

    if customer is None or provider is None:
        print("Run python test_db.py first.")
    else:
        profile = ProviderProfile.query.filter_by(
            user_id=provider.id
        ).first()

        category = ServiceCategory.query.filter_by(
            name="Plumber"
        ).first()

        if profile is None or category is None:
            print("Provider profile or Plumber category is missing.")
        else:
            # Create one sample booking if it doesn't exist.
            booking = Booking.query.filter_by(
                customer_id=customer.id,
                provider_profile_id=profile.id,
                description="Test leaking tap repair"
            ).first()

            if booking is None:
                booking = Booking(
                    customer_id=customer.id,
                    provider_profile_id=profile.id,
                    service_category_id=category.id,
                    service_address="Kukatpally, Hyderabad",
                    description="Test leaking tap repair",
                    status="completed",
                )
                db.session.add(booking)
                db.session.commit()

            # Create one sample review if it doesn't exist.
            review = Review.query.filter_by(
                booking_id=booking.id
            ).first()

            if review is None:
                review = Review(
                    booking_id=booking.id,
                    reviewer_id=customer.id,
                    provider_profile_id=profile.id,
                    rating=5,
                    comment="Sample review for database testing.",
                )
                db.session.add(review)
                db.session.commit()

            # Read the booking and related records.
            print("\nBooking details:")
            print("Booking ID:", booking.id)
            print("Customer:", booking.customer.name)
            print("Provider:", booking.provider_profile.user.name)
            print("Service:", booking.service_category.name)
            print("Status:", booking.status)

            print("\nReview details:")
            print("Rating:", booking.review.rating, "/ 5")
            print("Comment:", booking.review.comment)

            print("\nBooking and review test completed!")
