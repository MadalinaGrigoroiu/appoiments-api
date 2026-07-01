"""
Routes for appointment-related API endpoints.
Handles HTTP requests for booking and managing appointments.
"""

from flask import Blueprint, request, jsonify
from app.services.appoiment_service import AppointmentService

bp = Blueprint("appointments", __name__, url_prefix="/api/appointments")
appointment_service = AppointmentService()


@bp.route("", methods=["GET"])
def get_appointments():
  
    try:
        appointments = appointment_service.get_all_appointments()
        return jsonify([apt.to_dict() for apt in appointments]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/<int:appointment_id>", methods=["GET"])
def get_appointment(appointment_id):
   
    try:
        appointment = appointment_service.get_appointment_by_id(appointment_id)
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404
        return jsonify(appointment.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("", methods=["POST"])
def create_appointment():
    """Create a new appointment."""
    try:
        data = request.get_json()
        appointment = appointment_service.create_appointment(data)
        return jsonify(appointment.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/<int:appointment_id>", methods=["PUT"])
def update_appointment(appointment_id):
    """Update an appointment."""
    try:
        data = request.get_json()
        appointment = appointment_service.update_appointment(appointment_id, data)
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404
        return jsonify(appointment.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/<int:appointment_id>", methods=["DELETE"])
def delete_appointment_handler(appointment_id):

    try:
        if appointment_service.delete_appointment(appointment_id):
            return jsonify({"message": "Appointment deleted"}), 200
        return jsonify({"error": "Appointment not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500