"""
Service layer for service (appointment type) operations.
Handles CRUD operations for available services.
"""

from app import db
from app.models import Service
from typing import List, Optional, Dict, Any


class ServiceService:


    def get_all_services(self) -> List[Service]:
        """all services."""
        return Service.query.all()

    def get_service_by_id(self, service_id: int) -> Optional[Service]:
        """a service by ID."""
        return Service.query.get(service_id)

    def create_service(self, data: Dict[str, Any]) -> Service:
        """ new service."""
        if not data.get("name") or data.get("duration_minutes") is None or data.get("price") is None:
            raise ValueError("Name, duration_minutes, and price are required")

        # Check if name already exists
        existing_service = Service.query.filter_by(name=data["name"]).first()
        if existing_service:
            raise ValueError(" already exists")

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
      
        service = Service.query.get(service_id)
        if not service:
            return None

        if "name" in data:
            # Check if new name already exists for another service
            existing = Service.query.filter_by(name=data["name"]).first()
            if existing and existing.id != service_id:
                raise ValueError(" already exists")
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
