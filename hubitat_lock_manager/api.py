import dataclasses

from flask import Flask, request, jsonify

from hubitat_lock_manager import controller

HUB_IP = "192.168.86.37"

app = Flask(__name__)
smart_lock_controller = controller.create_smart_lock_controller(HUB_IP)


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
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/list_key_codes", methods=["GET"])
def list_key_codes():
    device_id = request.args.get("device_id", type=int)
    if not device_id:
        return (jsonify({"error": "device_id is required"}),)
    #
    # device_ids = frozenset(
    #     [device.id for device in smart_lock_controller.list_devices().devices]
    # )
    # if device_id not in device_ids:
    #     return jsonify({"error": f"device_id {device_id} not found"}), 400

    try:
        result = smart_lock_controller.list_key_codes(device_id)
        return jsonify(dataclasses.asdict(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", 5000))
