import argparse
import dataclasses
import pprint

from hubitat_lock_manager import controller, smart_lock


def parse_args():
    parser = argparse.ArgumentParser(description="SmartLockController CLI")
    parser.add_argument("--hub-ip", required=True, help="Hub IP address")
    parser.add_argument("--device-id", type=int, help="Device ID")
    parser.add_argument(
        "--action",
        required=True,
        choices=["create", "delete", "get", "list", "update"],
        help="Action to perform",
    )
    parser.add_argument("--username", help="Username for the key code")
    parser.add_argument("--code", help="8-digit code")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if not args.hub_ip:
        raise ValueError("Hub IP is required")

    webdriver_config = smart_lock.WebdriverConfig(args.hub_ip)
    config = smart_lock.create_webdriver_smart_lock_config(webdriver_config)

    smart_lock_controller = controller.create_smart_lock_controller(config)

    if args.action == "create":
        if not args.username or not args.code:
            pprint.pprint(
                "Both username and code are required for creating a key code."
            )
            return

        if args.device_id:
            result = smart_lock_controller.create_key_code(
                args.username, args.code, args.device_id
            )
        else:
            result = list(
                smart_lock_controller.create_key_code_on_all_devices(
                    args.username, args.code
                )
            )

        pprint.pprint(f"Create key code result: {result}")

    elif args.action == "delete":
        if not args.username:
            pprint.pprint("Username is required for deleting a key code.")
            return

        if args.device_id:
            result = smart_lock_controller.delete_key_code(
                args.username, args.device_id
            )
        else:
            result = list(
                smart_lock_controller.delete_key_code_on_all_devices(args.username)
            )
        pprint.pprint(f"Delete key code result: {result}")

    elif args.action == "get":
        if not args.username:
            pprint.pprint("Username is required for getting a key code.")
            return
        result = smart_lock_controller.get_key_code(args.username, args.device_id)
        pprint.pprint(f"Get key code result: {result}")

    elif args.action == "list":
        result = smart_lock_controller.list_key_codes(args.device_id)
        pprint.pprint(f"List key codes result: {dataclasses.asdict(result)}")

    elif args.action == "list_devices":
        result = smart_lock_controller.list_devices()
        pprint.pprint(f"List devices result: {result}")

    elif args.action == "update":
        if not args.username or not args.code:
            pprint.pprint(
                "Both username and code are required for updating a key code."
            )
            return
        result = smart_lock_controller.update_key_code(
            args.device_id, args.username, args.code
        )
        pprint.pprint(f"Update key code result: {result}")


if __name__ == "__main__":
    # Usage:
    # python -m hubitat_lock_manager.main --hub-ip
    # <hub_ip> --app-id <app_id> --access-token <access_token> --device-id
    # <device_id> --device-type <device_type> --action <action> --username
    # <username> --code <code>

    # Example:
    # python -m hubitat_lock_manager.main --hub-ip
    main()
