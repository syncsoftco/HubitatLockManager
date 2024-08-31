import requests
import streamlit as st
import argparse


def create_key_code(api_url, username, code, device_id):
    """
    Create a new key code for a given username and optionally for a specified device.

    Args:
    api_url (str): The base URL of the API.
    username (str): The username for which to create the key code.
    code (str): An 8-digit code.
    device_id (int): The device ID to which the key code applies. Defaults to -1 if not provided.

    Returns:
    response (requests.Response): The response from the API call.
    """
    payload = {"username": username, "code": code}
    if device_id != -1:
        payload["device_id"] = device_id
    return requests.post(f"{api_url}/create_key_code", json=payload)


def delete_key_code(api_url, username, device_id):
    """
    Delete a key code for a given username from a specified device.

    Args:
    api_url (str): The base URL of the API.
    username (str): The username whose key code is to be deleted.
    device_id (int): The device ID from which to delete the key code.

    Returns:
    response (requests.Response): The response from the API call.
    """
    payload = {"username": username, "device_id": device_id}
    return requests.delete(f"{api_url}/delete_key_code", json=payload)


def list_devices(api_url):
    """
    List all available devices.

    Args:
    api_url (str): The base URL of the API.

    Returns:
    response (requests.Response): The response from the API call.
    """
    return requests.get(f"{api_url}/list_devices")


def list_key_codes(api_url, device_id):
    """
    List all key codes for a specified device.

    Args:
    api_url (str): The base URL of the API.
    device_id (int): The device ID for which to list key codes.

    Returns:
    response (requests.Response): The response from the API call.
    """
    params = {"device_id": device_id}
    return requests.get(f"{api_url}/list_key_codes", params=params)


def main(api_url):
    """
    Main driver function to render the Streamlit application.

    Args:
    api_url (str): The base URL of the API.
    """
    st.title("Smart Lock Management")

    # List Devices to populate dropdowns
    devices_response = list_devices(api_url)
    if devices_response.status_code != 200:
        st.error(f"Error fetching devices: {devices_response.json().get('error')}")
        return

    devices = devices_response.json()["devices"]
    device_options = {device["name"]: device["id"] for device in devices}

    # Create Key Code Section
    st.header("Create Key Code")
    with st.form("create_key_code_form"):
        username = st.text_input(
            "Username", help="Enter the username for the key code."
        )
        code = st.text_input("Code (8 digits)", help="Enter an 8-digit code.")
        device_name = st.selectbox(
            "Select Device",
            options=["All Devices"] + list(device_options.keys()),
            help="Select the device if applicable. Leave as 'All Devices' if not.",
        )
        create_key_code_button = st.form_submit_button("Create Key Code")
        if create_key_code_button:
            device_id = device_options[device_name] if device_name != "All Devices" else -1
            response = create_key_code(api_url, username, code, device_id)
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
        device_name_delete = st.selectbox(
            "Select Device to delete from",
            options=list(device_options.keys()),
            help="Select the device from which to delete the key code.",
        )
        delete_key_code_button = st.form_submit_button("Delete Key Code")
        if delete_key_code_button:
            device_id_delete = device_options[device_name_delete]
            response = delete_key_code(api_url, username_delete, device_id_delete)
            if response.status_code == 200:
                st.success("Key code deleted successfully!")
            else:
                st.error(f"Error: {response.json().get('error')}")

    st.markdown("---")

    # List Key Codes Section
    st.header("List Key Codes")
    with st.form("list_key_codes_form"):
        device_name_list = st.selectbox(
            "Select Device to list key codes from",
            options=list(device_options.keys()),
            help="Select the device to list all key codes from.",
        )
        list_key_codes_button = st.form_submit_button("List Key Codes")
        if list_key_codes_button:
            selected_device_id = device_options[device_name_list]
            response = list_key_codes(api_url, selected_device_id)
            if response.status_code == 200:
                key_codes = response.json()
                st.json(key_codes)
            else:
                st.error(f"Error: {response.text}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Smart Lock Management Streamlit app.")
    parser.add_argument("--api-url", type=str, required=True, help="URL of the Flask API")
    args = parser.parse_args()

    main(args.api_url)
