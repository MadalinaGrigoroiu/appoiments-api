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
        """Retrieve all clients."""
        return Client.query.all()

    def get_client_by_id(self, client_id: int) -> Optional[Client]:
        """Retrieve a client by ID."""
        return Client.query.get(client_id)

    def create_client(self, data: Dict[str, Any]) -> Client:
        """Create a new client."""
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
        """Update a client."""
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
class ClientService:
    """Service class for client-related operations."""
    
    @staticmethod
    def create_client(name: str, email: str, phone: str) -> Dict[str, Any]:
        """
        Create a new client.
        
        Args:
            name: Client's full name
            email: Client's email address
            phone: Client's contact phone
            
        Returns:
            Dictionary with created client data
            
        Raises:
            ValueError: If email already exists or invalid data
        """
        # Check if email already exists
        existing_client = Client.query.filter_by(email=email).first()
        if existing_client:
            raise ValueError(f"Email {email} already exists")
        
        new_client = Client(name=name, email=email, phone=phone)
        db.session.add(new_client)
        db.session.commit()
        
        return new_client.to_dict()
    
    @staticmethod
    def get_all_clients() -> List[Dict[str, Any]]:
        """
        Retrieve all clients from the database.
        
        Returns:
            List of client dictionaries
        """
        clients = Client.query.all()
        return [client.to_dict() for client in clients]
    
    @staticmethod
    def get_client_by_id(client_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific client by ID.
        
        Args:
            client_id: Client's unique identifier
            
        Returns:
            Client dictionary or None if not found
        """
        client = Client.query.get(client_id)
        if client:
            return client.to_dict()
        return None
    
    @staticmethod
    def update_client(client_id: int, name: str = None, email: str = None, 
                     phone: str = None) -> Dict[str, Any]:
        """
        Update client information.
        
        Args:
            client_id: Client's unique identifier
            name: Updated name (optional)
            email: Updated email (optional)
            phone: Updated phone (optional)
            
        Returns:
            Updated client dictionary
            
        Raises:
            ValueError: If client not found or email already exists
        """
        client = Client.query.get(client_id)
        if not client:
            raise ValueError(f"Client with ID {client_id} not found")
        
        if email and email != client.email:
            existing = Client.query.filter_by(email=email).first()
            if existing:
                raise ValueError(f"Email {email} already exists")
            client.email = email
        
        if name:
            client.name = name
        if phone:
            client.phone = phone
        
        db.session.commit()
        return client.to_dict()
    
    @staticmethod
    def delete_client(client_id: int) -> bool:
        """
        Delete a client and all related appointments.
        
        Args:
            client_id: Client's unique identifier
            
        Returns:
            True if deleted successfully
            
        Raises:
            ValueError: If client not found
        """
        client = Client.query.get(client_id)
        if not client:
            raise ValueError(f"Client with ID {client_id} not found")
        
        db.session.delete(client)
        db.session.commit()
        return True