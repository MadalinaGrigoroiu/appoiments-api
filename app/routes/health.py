"""
Health check and status endpoints.
"""

from flask import Blueprint, jsonify

bp = Blueprint("health", __name__, url_prefix="/health")


@bp.route("", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "message": "Appointments API is running",
        "version": "1.0.0"
    }), 200


@bp.route("/status", methods=["GET"])
def api_health():
    """API health check endpoint."""
    return jsonify({
        "status": "ok",
        "service": "appointments-api"
    }), 200
