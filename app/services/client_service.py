"""
Service layer for client operations.
Contains business logic for creating, reading, updating, and deleting clients.
"""

from app import db
from app.models import Client
from typing import List, Optional, Dict, Any


class ClientService:
    """Handles business logic for client operations."""

    def get_all_clients(self) -> List[Client]:
       
        return Client.query.all()

    def get_client_by_id(self, client_id: int) -> Optional[Client]:
        
        return Client.query.get(client_id)

    def create_client(self, data: Dict[str, Any]) -> Client:
      
        if not data.get("name") or not data.get("email") or not data.get("phone"):
            raise ValueError("Name, email, and phone are required")

        # Check if email already exists
        existing_client = Client.query.filter_by(email=data["email"]).first()
        if existing_client:
            raise ValueError("Email already exists")

        client = Client(
            name=data["name"],
            email=data["email"],
            phone=data["phone"]
        )
        db.session.add(client)
        db.session.commit()
        return client

    def update_client(self, client_id: int, data: Dict[str, Any]) -> Optional[Client]:
        
        client = Client.query.get(client_id)
        if not client:
            return None

        if "name" in data:
            client.name = data["name"]
        if "email" in data:
            # Check if new email already exists for another client
            existing = Client.query.filter_by(email=data["email"]).first()
            if existing and existing.id != client_id:
                raise ValueError("Email already exists")
            client.email = data["email"]
        if "phone" in data:
            client.phone = data["phone"]

        db.session.commit()
        return client

    def delete_client(self, client_id: int) -> bool:
        """Delete a client."""
        client = Client.query.get(client_id)
        if not client:
            return False

        db.session.delete(client)
        db.session.commit()
        return True