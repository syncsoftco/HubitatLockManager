import dataclasses
import logging
import os

from flask import Flask, request, jsonify

from hubitat_lock_manager import controller

COMMAND_EXECUTOR = os.getenv("SELENIUM_HUB_URL", "")
HUB_IP = os.getenv("HUB_IP", "192.168.86.37")

app = Flask(__name__)
smart_lock_controller = controller.create_smart_lock_controller(
    HUB_IP,
    COMMAND_EXECUTOR,
)


@app.route("/create_key_code", methods=["POST"])
def create_key_code():
    data = request.json
    params = controller.CreateKeyCodeParams(
        code=data["code"],
        username=data["username"],
        device_id=data.get("device_id", -1),
    )
    try:
        results = list(smart_lock_controller.create_key_code(params))
        return jsonify([dataclasses.asdict(result) for result in results]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/delete_key_code", methods=["DELETE"])
def delete_key_code():
    data = request.json
    username = data["username"]
    device_id = data["device_id"]
    try:
        result = smart_lock_controller.delete_key_code(username, device_id)
        return jsonify(dataclasses.asdict(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/list_devices", methods=["GET"])
def list_devices():
    try:
        result = smart_lock_controller.list_devices()
        return jsonify(dataclasses.asdict(result)), 200
    except ValueError as e:
        logging.error(f"ValueError: {str(e)}")
        return jsonify({"error": "Invalid request data"}), 400
    except KeyError as e:
        logging.error(f"KeyError: {str(e)}")
        return jsonify({"error": "Missing data"}), 400
    except Exception as e:
        logging.error(f"Unhandled Exception: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/list_key_codes", methods=["GET"])
def list_key_codes():
    device_id = request.args.get("device_id", type=int)
    if not device_id:
        raise ValueError("device_id is required")

    try:
        result = smart_lock_controller.list_key_codes(device_id)
        return jsonify(dataclasses.asdict(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", 5000))
