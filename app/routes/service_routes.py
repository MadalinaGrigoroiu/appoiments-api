"""
Routes for service-related API endpoints.
Handles HTTP requests for service CRUD operations.
"""

from flask import Blueprint, request, jsonify
from app.services.service_service import ServiceService

bp = Blueprint("services", __name__, url_prefix="/api/services")
service_service = ServiceService()


@bp.route("", methods=["GET"])
def get_services():
    """Get all services."""
    try:
        services = service_service.get_all_services()
        return jsonify([service.to_dict() for service in services]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/<int:service_id>", methods=["GET"])
def get_service(service_id):
    """Get a specific service by ID."""
    try:
        service = service_service.get_service_by_id(service_id)
        if not service:
            return jsonify({"error": "Service not found"}), 404
        return jsonify(service.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("", methods=["POST"])
def create_service():
    """Create a new service."""
    try:
        data = request.get_json()
        service = service_service.create_service(data)
        return jsonify(service.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/<int:service_id>", methods=["PUT"])
def update_service(service_id):
    """Update a service."""
    try:
        data = request.get_json()
        service = service_service.update_service(service_id, data)
        if not service:
            return jsonify({"error": "Service not found"}), 404
        return jsonify(service.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/<int:service_id>", methods=["DELETE"])
def delete_service_handler(service_id):
    """Delete a service."""
    try:
        if service_service.delete_service(service_id):
            return jsonify({"message": "Service deleted"}), 200
        return jsonify({"error": "Service not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
        return jsonify({"success": True, "data": client}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("", methods=["POST"])
def create_client():
    """
    POST /api/clients
    Create a new client.
    
    JSON body:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+40712345678"
    }
    """
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ["name", "email", "phone"]
        if not all(field in data for field in required_fields):
            return jsonify({
                "success": False,
                "error": f"Missing required fields: {required_fields}"
            }), 400
        
        new_client = ClientService.create_client(
            name=data["name"],
            email=data["email"],
            phone=data["phone"]
        )
        
        return jsonify({"success": True, "data": new_client}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 409
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/<int:client_id>", methods=["PUT"])
def update_client(client_id: int):
    """
    PUT /api/clients/<client_id>
    Update client information.
    """
    try:
        data = request.get_json()
        updated_client = ClientService.update_client(
            client_id=client_id,
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone")
        )
        return jsonify({"success": True, "data": updated_client}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/<int:client_id>", methods=["DELETE"])
def delete_client(client_id: int):
    """
    DELETE /api/clients/<client_id>
    Delete a client.
    """
    try:
        ClientService.delete_client(client_id)
        return jsonify({"success": True, "message": "Client deleted"}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500