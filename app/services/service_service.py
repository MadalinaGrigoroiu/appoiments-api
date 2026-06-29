"""
Service layer for service (appointment type) operations.
Handles CRUD operations for available services.
"""

from app import db
from app.models import Service
from typing import List, Optional, Dict, Any


class ServiceService:
    """Handles business logic for service operations."""

    def get_all_services(self) -> List[Service]:
        """Retrieve all services."""
        return Service.query.all()

    def get_service_by_id(self, service_id: int) -> Optional[Service]:
        """Retrieve a service by ID."""
        return Service.query.get(service_id)

    def create_service(self, data: Dict[str, Any]) -> Service:
        """Create a new service."""
        if not data.get("name") or data.get("duration_minutes") is None or data.get("price") is None:
            raise ValueError("Name, duration_minutes, and price are required")

        # Check if name already exists
        existing_service = Service.query.filter_by(name=data["name"]).first()
        if existing_service:
            raise ValueError("Service name already exists")

        service = Service(
            name=data["name"],
            description=data.get("description", ""),
            duration_minutes=data["duration_minutes"],
            price=data["price"]
        )
        db.session.add(service)
        db.session.commit()
        return service

    def update_service(self, service_id: int, data: Dict[str, Any]) -> Optional[Service]:
        """Update a service."""
        service = Service.query.get(service_id)
        if not service:
            return None

        if "name" in data:
            # Check if new name already exists for another service
            existing = Service.query.filter_by(name=data["name"]).first()
            if existing and existing.id != service_id:
                raise ValueError("Service name already exists")
            service.name = data["name"]
        if "description" in data:
            service.description = data["description"]
        if "duration_minutes" in data:
            service.duration_minutes = data["duration_minutes"]
        if "price" in data:
            service.price = data["price"]

        db.session.commit()
        return service

    def delete_service(self, service_id: int) -> bool:
        """Delete a service."""
        service = Service.query.get(service_id)
        if not service:
            return False

        db.session.delete(service)
        db.session.commit()
        return True
class ServiceService:
    """Service class for service-related operations."""
    
    @staticmethod
    def create_service(name: str, description: str, duration_minutes: int, 
                      price: float) -> Dict[str, Any]:
        """
        Create a new service offering.
        
        Args:
            name: Service name
            description: Service description
            duration_minutes: How long service takes in minutes
            price: Service price
            
        Returns:
            Dictionary with created service data
        """
        new_service = Service(
            name=name,
            description=description,
            duration_minutes=duration_minutes,
            price=price
        )
        db.session.add(new_service)
        db.session.commit()
        
        return new_service.to_dict()
    
    @staticmethod
    def get_all_services() -> List[Dict[str, Any]]:
        """Retrieve all available services."""
        services = Service.query.all()
        return [service.to_dict() for service in services]
    
    @staticmethod
    def get_service_by_id(service_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve specific service by ID."""
        service = Service.query.get(service_id)
        if service:
            return service.to_dict()
        return None
    
    @staticmethod
    def delete_service(service_id: int) -> bool:
        """Delete a service."""
        service = Service.query.get(service_id)
        if not service:
            raise ValueError(f"Service with ID {service_id} not found")
        
        db.session.delete(service)
        db.session.commit()
        return True