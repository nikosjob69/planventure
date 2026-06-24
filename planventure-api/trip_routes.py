from datetime import datetime

from flask import Blueprint, jsonify, request

from auth_utils import get_current_user, require_auth
from itinerary_utils import generate_default_itinerary
from trip_model import Trip
from user_model import db

bp = Blueprint("trip_routes", __name__, url_prefix="/trips")


def parse_date(value, field_name):
    if not value:
        raise ValueError(f"{field_name} is required.")
    try:
        return datetime.fromisoformat(value).date()
    except ValueError:
        raise ValueError(f"{field_name} must be an ISO date string (YYYY-MM-DD).")


def get_user_trip(trip_id, user):
    return Trip.query.filter_by(id=trip_id, user_id=user.id).first()


@bp.route("", methods=["POST"])
@require_auth()
def create_trip():
    user = get_current_user()
    data = request.get_json(silent=True) or {}

    destination = (data.get("destination") or "").strip()
    if not destination:
        return jsonify({"error": "Destination is required."}), 400

    try:
        start_date = parse_date(data.get("start_date"), "start_date")
        end_date = parse_date(data.get("end_date"), "end_date")
    except ValueError as err:
        return jsonify({"error": str(err)}), 400

    if start_date > end_date:
        return jsonify({"error": "end_date must be the same as or after start_date."}), 400

    latitude = data.get("latitude")
    longitude = data.get("longitude")
    itinerary = data.get("itinerary")

    try:
        latitude = float(latitude) if latitude is not None else None
        longitude = float(longitude) if longitude is not None else None
    except (TypeError, ValueError):
        return jsonify({"error": "latitude and longitude must be numeric values."}), 400

    # Generate default itinerary if not provided
    if not itinerary:
        itinerary = generate_default_itinerary(destination, start_date, end_date)

    trip = Trip(
        user_id=user.id,
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        latitude=latitude,
        longitude=longitude,
        itinerary=itinerary,
    )

    db.session.add(trip)
    db.session.commit()

    return jsonify(trip.to_dict()), 201


@bp.route("", methods=["GET"])
@require_auth()
def list_trips():
    user = get_current_user()
    trips = Trip.query.filter_by(user_id=user.id).order_by(Trip.start_date).all()
    return jsonify([trip.to_dict() for trip in trips]), 200


@bp.route("/generate-itinerary", methods=["POST"])
@require_auth()
def generate_itinerary():
    data = request.get_json(silent=True) or {}

    destination = (data.get("destination") or "").strip()
    if not destination:
        return jsonify({"error": "Destination is required."}), 400

    try:
        start_date = parse_date(data.get("start_date"), "start_date")
        end_date = parse_date(data.get("end_date"), "end_date")
    except ValueError as err:
        return jsonify({"error": str(err)}), 400

    if start_date > end_date:
        return jsonify({"error": "end_date must be the same as or after start_date."}), 400

    itinerary = generate_default_itinerary(destination, start_date, end_date)
    return jsonify({
        "destination": destination,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "itinerary": itinerary
    }), 200


@bp.route("/<int:trip_id>", methods=["GET"])
@require_auth()
def get_trip(trip_id):
    user = get_current_user()
    trip = get_user_trip(trip_id, user)
    if not trip:
        return jsonify({"error": "Trip not found."}), 404
    return jsonify(trip.to_dict()), 200


@bp.route("/<int:trip_id>", methods=["PUT"])
@require_auth()
def update_trip(trip_id):
    user = get_current_user()
    trip = get_user_trip(trip_id, user)
    if not trip:
        return jsonify({"error": "Trip not found."}), 404

    data = request.get_json(silent=True) or {}
    if "destination" in data:
        destination = (data.get("destination") or "").strip()
        if not destination:
            return jsonify({"error": "Destination is required."}), 400
        trip.destination = destination

    if "start_date" in data:
        try:
            trip.start_date = parse_date(data.get("start_date"), "start_date")
        except ValueError as err:
            return jsonify({"error": str(err)}), 400

    if "end_date" in data:
        try:
            trip.end_date = parse_date(data.get("end_date"), "end_date")
        except ValueError as err:
            return jsonify({"error": str(err)}), 400

    if trip.start_date and trip.end_date and trip.start_date > trip.end_date:
        return jsonify({"error": "end_date must be the same as or after start_date."}), 400

    if "latitude" in data:
        latitude = data.get("latitude")
        try:
            trip.latitude = float(latitude) if latitude is not None else None
        except (TypeError, ValueError):
            return jsonify({"error": "latitude must be numeric."}), 400

    if "longitude" in data:
        longitude = data.get("longitude")
        try:
            trip.longitude = float(longitude) if longitude is not None else None
        except (TypeError, ValueError):
            return jsonify({"error": "longitude must be numeric."}), 400

    if "itinerary" in data:
        trip.itinerary = data.get("itinerary")

    db.session.commit()
    return jsonify(trip.to_dict()), 200


@bp.route("/<int:trip_id>", methods=["DELETE"])
@require_auth()
def delete_trip(trip_id):
    user = get_current_user()
    trip = get_user_trip(trip_id, user)
    if not trip:
        return jsonify({"error": "Trip not found."}), 404

    db.session.delete(trip)
    db.session.commit()
    return jsonify({"message": "Trip deleted successfully."}), 200
