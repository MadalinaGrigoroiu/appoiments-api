"""
Service layer for appointment operations.
Handles booking, updating, and managing appointments.
"""

from app import db
from app.models import Appointment, Client, Service
from datetime import datetime
from typing import List, Optional, Dict, Any


class AppointmentService:
    """Handles business logic for appointment operations."""

    def get_all_appointments(self) -> List[Appointment]:
        """Retrieve all appointments."""
        return Appointment.query.all()

    def get_appointment_by_id(self, appointment_id: int) -> Optional[Appointment]:
        """Retrieve an appointment by ID."""
        return Appointment.query.get(appointment_id)

    def create_appointment(self, data: Dict[str, Any]) -> Appointment:
        """Create a new appointment."""
        if not data.get("client_id") or not data.get("service_id") or not data.get("appointment_date"):
            raise ValueError("Client ID, Service ID, and appointment date are required")

        # Verify client and service exist
        client = Client.query.get(data["client_id"])
        service = Service.query.get(data["service_id"])

        if not client:
            raise ValueError("Client not found")
        if not service:
            raise ValueError("Service not found")

        appointment = Appointment(
            client_id=data["client_id"],
            service_id=data["service_id"],
            appointment_date=datetime.fromisoformat(data["appointment_date"]),
            status=data.get("status", "pending"),
            notes=data.get("notes", "")
        )
        db.session.add(appointment)
        db.session.commit()
        return appointment

    def update_appointment(self, appointment_id: int, data: Dict[str, Any]) -> Optional[Appointment]:
        """Update an appointment."""
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return None

        if "appointment_date" in data:
            appointment.appointment_date = datetime.fromisoformat(data["appointment_date"])
        if "status" in data:
            appointment.status = data["status"]
        if "notes" in data:
            appointment.notes = data["notes"]

        db.session.commit()
        return appointment

    def delete_appointment(self, appointment_id: int) -> bool:
        """Delete an appointment."""
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return False

        db.session.delete(appointment)
        db.session.commit()
        return True

