"""DB models for appointments system.

WARNING: SQLite is fine for dev, but switch to PostgreSQL for production
"""

from app import db
from datetime import datetime


class Client(db.Model):
    """Client model - who books appointments."""

    __tablename__ = "clients"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    email: str = db.Column(db.String(100), unique=True, nullable=False)
    phone: str = db.Column(db.String(20), nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    appointments = db.relationship(
        "Appointment", backref="client", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self) -> dict:
        """Convert to dict."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "created_at": self.created_at.isoformat(),
        }


class Service(db.Model):
    """Service model."""

    __tablename__ = "services"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False, unique=True)
    description: str = db.Column(db.String(500))
    duration_minutes: int = db.Column(db.Integer, nullable=False)
    price: float = db.Column(db.Float, nullable=False)

    # Relationship
    appointments = db.relationship(
        "Appointment", backref="service", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self) -> dict:
        """Convert service object to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "duration_minutes": self.duration_minutes,
            "price": self.price,
        }


class Appointment(db.Model):
    """Represents a booked appointment between a client and a service.

    Attributes:
        id: Unique identifier
        client_id: Foreign key to Client
        service_id: Foreign key to Service
        appointment_date: When the appointment is scheduled
        status: Current status (pending, confirmed, completed, cancelled)
        notes: Additional notes about the appointment
        created_at: When the appointment was created
    """

    __tablename__ = "appointments"

    id: int = db.Column(db.Integer, primary_key=True)
    client_id: int = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    service_id: int = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    appointment_date: datetime = db.Column(db.DateTime, nullable=False)
    status: str = db.Column(
        db.String(20), default="pending"
    )  # pending, confirmed, completed, cancelled
    notes: str = db.Column(db.String(500))
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        """Convert appointment object to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "client_name": self.client.name,
            "service_id": self.service_id,
            "service_name": self.service.name,
            "appointment_date": self.appointment_date.isoformat(),
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
        }
