import requests
import streamlit as st

API_URL = "http://127.0.0.1:5000"  # URL of your Flask API


def create_key_code(username, code, device_id):
    """
    Create a new key code for a given username and optionally for a specified device.

    Args:
    username (str): The username for which to create the key code.
    code (str): An 8-digit code.
    device_id (int): The device ID to which the key code applies. Defaults to -1 if not provided.

    Returns:
    response (requests.Response): The response from the API call.
    """
    payload = {"username": username, "code": code}
    if device_id != -1:
        payload["device_id"] = device_id
    return requests.post(f"{API_URL}/create_key_code", json=payload)


def delete_key_code(username, device_id):
    """
    Delete a key code for a given username from a specified device.

    Args:
    username (str): The username whose key code is to be deleted.
    device_id (int): The device ID from which to delete the key code.

    Returns:
    response (requests.Response): The response from the API call.
    """
    payload = {"username": username, "device_id": device_id}
    return requests.delete(f"{API_URL}/delete_key_code", json=payload)


def list_devices():
    """
    List all available devices.

    Returns:
    response (requests.Response): The response from the API call.
    """
    return requests.get(f"{API_URL}/list_devices")


def list_key_codes(device_id):
    """
    List all key codes for a specified device.

    Args:
    device_id (int): The device ID for which to list key codes.

    Returns:
    response (requests.Response): The response from the API call.
    """
    params = {"device_id": device_id}
    return requests.get(f"{API_URL}/list_key_codes", params=params)


def main():
    """
    Main driver function to render the Streamlit application.
    """
    st.title("Smart Lock Management")

    # Create Key Code Section
    st.header("Create Key Code")
    with st.form("create_key_code_form"):
        username = st.text_input("Username", help="Enter the username for the key code.")
        code = st.text_input("Code (8 digits)", help="Enter an 8-digit code.")
        device_id = st.number_input(
            "Device ID (optional)",
            min_value=-1,
            step=1,
            value=-1,
            help="Enter the device ID if applicable. Leave as -1 if not.",
        )
        create_key_code_button = st.form_submit_button("Create Key Code")
        if create_key_code_button:
            response = create_key_code(username, code, device_id)
            if response.status_code == 200:
                st.success("Key code created successfully!")
            else:
                st.error(f"Error: {response.text}")

    st.markdown("---")

    # Delete Key Code Section
    st.header("Delete Key Code")
    with st.form("delete_key_code_form"):
        username_delete = st.text_input(
            "Username to delete",
            help="Enter the username whose key code you want to delete.",
        )
        device_id_delete = st.number_input(
            "Device ID to delete from",
            min_value=0,
            step=1,
            help="Enter the device ID from which to delete the key code.",
        )
        delete_key_code_button = st.form_submit_button("Delete Key Code")
        if delete_key_code_button:
            response = delete_key_code(username_delete, device_id_delete)
            if response.status_code == 200:
                st.success("Key code deleted successfully!")
            else:
                st.error(f"Error: {response.json().get('error')}")

    st.markdown("---")

    # List Key Codes Section
    st.header("List Key Codes")

    devices_response = list_devices()
    if devices_response.status_code != 200:
        st.error(f"Error fetching devices: {devices_response.json().get('error')}")
    else:
        devices = devices_response.json()["devices"]
        device_options = {device['name']: device['id'] for device in devices}
        with st.form("list_key_codes_form"):
            device_name_list = st.selectbox(
                "Select Device to list key codes from",
                options=list(device_options.keys()),
                help="Select the device to list all key codes from.",
            )
            list_key_codes_button = st.form_submit_button("List Key Codes")
            if list_key_codes_button:
                selected_device_id = device_options[device_name_list]
                response = list_key_codes(selected_device_id)
                if response.status_code == 200:
                    key_codes = response.json()
                    st.json(key_codes)
                else:
                    st.error(f"Error: {response.text}")


if __name__ == "__main__":
    main()
