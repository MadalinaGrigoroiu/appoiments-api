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

class AppointmentService:
    """Service class for appointment-related operations."""
    
    @staticmethod
    def create_appointment(client_id: int, service_id: int, 
                          appointment_date: str, notes: str = None) -> Dict[str, Any]:
        """
        Book a new appointment.
        
        Args:
            client_id: ID of the client
            service_id: ID of the service
            appointment_date: ISO format datetime string (e.g., "2024-01-20T10:00:00")
            notes: Optional notes about the appointment
            
        Returns:
            Dictionary with created appointment data
            
        Raises:
            ValueError: If client/service not found or date is invalid
        """
        # Validate client and service exist
        client = Client.query.get(client_id)
        if not client:
            raise ValueError(f"Client with ID {client_id} not found")
        
        service = Service.query.get(service_id)
        if not service:
            raise ValueError(f"Service with ID {service_id} not found")
        
        # Parse and validate date
        try:
            appt_date = datetime.fromisoformat(appointment_date)
        except ValueError:
            raise ValueError("Invalid date format. Use ISO format: YYYY-MM-DDTHH:MM:SS")
        
        # Check for conflicts (same client, same time slot)
        conflict = Appointment.query.filter(
            Appointment.client_id == client_id,
            Appointment.appointment_date == appt_date,
            Appointment.status != "cancelled"
        ).first()
        
        if conflict:
            raise ValueError("Client already has an appointment at this time")
        
        new_appointment = Appointment(
            client_id=client_id,
            service_id=service_id,
            appointment_date=appt_date,
            status="pending",
            notes=notes
        )
        
        db.session.add(new_appointment)
        db.session.commit()
        
        return new_appointment.to_dict()
    
    @staticmethod
    def get_all_appointments() -> List[Dict[str, Any]]:
        """Retrieve all appointments."""
        appointments = Appointment.query.all()
        return [appt.to_dict() for appt in appointments]
    
    @staticmethod
    def get_appointment_by_id(appointment_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve specific appointment by ID."""
        appointment = Appointment.query.get(appointment_id)
        if appointment:
            return appointment.to_dict()
        return None
    
    @staticmethod
    def get_appointments_by_client(client_id: int) -> List[Dict[str, Any]]:
        """Get all appointments for a specific client."""
        appointments = Appointment.query.filter_by(client_id=client_id).all()
        return [appt.to_dict() for appt in appointments]
    
    @staticmethod
    def update_appointment_status(appointment_id: int, status: str) -> Dict[str, Any]:
        """
        Update appointment status.
        
        Args:
            appointment_id: Appointment ID
            status: New status (pending, confirmed, completed, cancelled)
            
        Returns:
            Updated appointment dictionary
        """
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            raise ValueError(f"Appointment with ID {appointment_id} not found")
        
        valid_statuses = ["pending", "confirmed", "completed", "cancelled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        
        appointment.status = status
        db.session.commit()
        
        return appointment.to_dict()
    
    @staticmethod
    def cancel_appointment(appointment_id: int) -> Dict[str, Any]:
        """Cancel an appointment."""
        return AppointmentService.update_appointment_status(appointment_id, "cancelled")
    
    @staticmethod
    def delete_appointment(appointment_id: int) -> bool:
        """Delete an appointment."""
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            raise ValueError(f"Appointment with ID {appointment_id} not found")
        
        db.session.delete(appointment)
        db.session.commit()
        return True