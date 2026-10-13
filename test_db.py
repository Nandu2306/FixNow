
from app import create_app
from app.extensions import db
from app.models import User, ServiceCategory, ProviderProfile

app = create_app()

with app.app_context():
    # Add sample service categories if they don't exist.
    service_names = [
        "Plumber",
        "Electrician",
        "Carpenter",
        "Painter",
        "Furniture Work",
        "Blueprint & Drawing",
    ]

    for name in service_names:
        category = ServiceCategory.query.filter_by(
            name=name
        ).first()

        if category is None:
            db.session.add(ServiceCategory(name=name))

    db.session.commit()

    # Create a sample customer if not already present.
    customer = User.query.filter_by(
        email="customer@example.com"
    ).first()

    if customer is None:
        customer = User(
            name="Sample Customer",
            email="customer@example.com",
            password_hash="TEMPORARY_TEST_HASH",
            role="customer",
        )
        db.session.add(customer)
        db.session.commit()

    # Create a sample provider account if it doesn't exist.
    provider = User.query.filter_by(
        email="provider@example.com"
    ).first()

    if provider is None:
        provider = User(
            name="Sample Plumber",
            email="provider@example.com",
            password_hash="TEMPORARY_TEST_HASH",
            role="provider",
        )
        db.session.add(provider)
        db.session.commit()

    # Create the provider profile if missing.
    profile = ProviderProfile.query.filter_by(
        user_id=provider.id
    ).first()

    if profile is None:
        plumber_category = ServiceCategory.query.filter_by(
            name="Plumber"
        ).first()

        profile = ProviderProfile(
            user_id=provider.id,
            service_category_id=plumber_category.id,
            phone="9000000000",
            experience_years=3,
            area="Kukatpally",
            price_min=300,
            price_max=800,
            is_available=True,
            is_approved=True,
        )

        db.session.add(profile)
        db.session.commit()

    print("\nService categories:")
    for category in ServiceCategory.query.order_by(
        ServiceCategory.name
    ).all():
        print("-", category.name)

    print("\nUsers:")
    for user in User.query.order_by(User.id).all():
        print("-", user.name, "|", user.role, "|", user.email)

    print("\nProvider profiles:")
    for item in ProviderProfile.query.all():
        print(
            "-",
            item.user.name,
            "|",
            item.service_category.name,
            "|",
            item.area,
            "| Available:",
            item.is_available,
        )

    print("\nDatabase test completed!")
