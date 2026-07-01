"""
Routes for client-related API endpoints.
Handles HTTP requests for client CRUD operations.
"""

from flask import Blueprint, request, jsonify
from app.services.client_service import ClientService

bp = Blueprint("clients", __name__, url_prefix="/api/clients")
client_service = ClientService()


@bp.route("", methods=["GET"])
def get_clients():
   
    try:
        clients = client_service.get_all_clients()
        return jsonify([client.to_dict() for client in clients]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/<int:client_id>", methods=["GET"])
def get_client(client_id):
   
    try:
        client = client_service.get_client_by_id(client_id)
        if not client:
            return jsonify({"error": "Client not found"}), 404
        return jsonify(client.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("", methods=["POST"])
def create_client():
   
    try:
        data = request.get_json()
        client = client_service.create_client(data)
        return jsonify(client.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/<int:client_id>", methods=["PUT"])
def update_client(client_id):
    
    try:
        data = request.get_json()
        client = client_service.update_client(client_id, data)
        if not client:
            return jsonify({"error": "Client not found"}), 404
        return jsonify(client.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/<int:client_id>", methods=["DELETE"])
def delete_client_handler(client_id):
   
    try:
        if client_service.delete_client(client_id):
            return jsonify({"message": "Client deleted"}), 200
        return jsonify({"error": "Client not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500