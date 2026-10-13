
from datetime import datetime

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(
        db.String(20),
        nullable=False,
        default="customer"
    )

    # One provider account can have one provider profile.
    provider_profile = db.relationship(
        "ProviderProfile",
        back_populates="user",
        uselist=False
    )

    # Bookings created by this user as a customer.
    customer_bookings = db.relationship(
        "Booking",
        back_populates="customer",
        foreign_keys="Booking.customer_id"
    )

    # Reviews written by this user.
    authored_reviews = db.relationship(
        "Review",
        back_populates="reviewer",
        foreign_keys="Review.reviewer_id"
    )

    def __repr__(self):
        return f"<User {self.email}>"


class ServiceCategory(db.Model):
    __tablename__ = "service_categories"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    description = db.Column(db.Text, nullable=True)

    # Providers who offer this category.
    provider_profiles = db.relationship(
        "ProviderProfile",
        back_populates="service_category"
    )

    # Bookings made for this category.
    bookings = db.relationship(
        "Booking",
        back_populates="service_category"
    )

    def __repr__(self):
        return f"<ServiceCategory {self.name}>"


class ProviderProfile(db.Model):
    __tablename__ = "provider_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    service_category_id = db.Column(
        db.Integer,
        db.ForeignKey("service_categories.id"),
        nullable=False
    )

    phone = db.Column(db.String(20), nullable=False)

    experience_years = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    area = db.Column(db.String(100), nullable=False)

    price_min = db.Column(db.Numeric(10, 2), nullable=True)

    price_max = db.Column(db.Numeric(10, 2), nullable=True)

    is_available = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    is_approved = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    is_blocked = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    user = db.relationship(
        "User",
        back_populates="provider_profile"
    )

    service_category = db.relationship(
        "ServiceCategory",
        back_populates="provider_profiles"
    )

    bookings = db.relationship(
        "Booking",
        back_populates="provider_profile"
    )

    reviews = db.relationship(
        "Review",
        back_populates="provider_profile"
    )

    def __repr__(self):
        return f"<ProviderProfile {self.id}>"


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    provider_profile_id = db.Column(
        db.Integer,
        db.ForeignKey("provider_profiles.id"),
        nullable=False
    )

    service_category_id = db.Column(
        db.Integer,
        db.ForeignKey("service_categories.id"),
        nullable=False
    )

    service_address = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(db.Text, nullable=True)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="pending"
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    customer = db.relationship(
        "User",
        back_populates="customer_bookings",
        foreign_keys=[customer_id]
    )

    provider_profile = db.relationship(
        "ProviderProfile",
        back_populates="bookings"
    )

    service_category = db.relationship(
        "ServiceCategory",
        back_populates="bookings"
    )

    review = db.relationship(
        "Review",
        back_populates="booking",
        uselist=False
    )

    def __repr__(self):
        return f"<Booking {self.id}: {self.status}>"


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)

    booking_id = db.Column(
        db.Integer,
        db.ForeignKey("bookings.id"),
        unique=True,
        nullable=False
    )

    reviewer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    provider_profile_id = db.Column(
        db.Integer,
        db.ForeignKey("provider_profiles.id"),
        nullable=False
    )

    rating = db.Column(db.Integer, nullable=False)

    comment = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    __table_args__ = (
        db.CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name="check_review_rating"
        ),
    )

    booking = db.relationship(
        "Booking",
        back_populates="review"
    )

    reviewer = db.relationship(
        "User",
        back_populates="authored_reviews",
        foreign_keys=[reviewer_id]
    )

    provider_profile = db.relationship(
        "ProviderProfile",
        back_populates="reviews"
    )

    def __repr__(self):
        return f"<Review {self.id}: {self.rating}/5>"
