import streamlit as st
import argparse
import json
from hubitat_lock_manager.rest_client import CloudRunRestClient

def create_key_code(client, username, code, device_id):
    """
    Create a new key code for a given username and optionally for a specified device.

    Args:
    client (CloudRunRestClient): An instance of the CloudRunRestClient.
    username (str): The username for which to create the key code.
    code (str): An 8-digit code.
    device_id (int): The device ID to which the key code applies. Defaults to -1 if not provided.

    Returns:
    response (str): The response from the API call as a string.
    """
    payload = {"username": username, "code": code}
    if device_id != -1:
        payload["device_id"] = device_id
    return client.post("create_key_code", payload)

def delete_key_code(client, username, device_id):
    """
    Delete a key code for a given username from a specified device.

    Args:
    client (CloudRunRestClient): An instance of the CloudRunRestClient.
    username (str): The username whose key code is to be deleted.
    device_id (int): The device ID from which to delete the key code.

    Returns:
    response (str): The response from the API call as a string.
    """
    payload = {"username": username, "device_id": device_id}
    return client.delete("delete_key_code", payload)

def list_devices(client):
    """
    List all available devices.

    Args:
    client (CloudRunRestClient): An instance of the CloudRunRestClient.

    Returns:
    response (str): The response from the API call as a string.
    """
    return client.get("list_devices")

def list_key_codes(client, device_id):
    """
    List all key codes for a specified device.

    Args:
    client (CloudRunRestClient): An instance of the CloudRunRestClient.
    device_id (int): The device ID for which to list key codes.

    Returns:
    response (str): The response from the API call as a string.
    """
    params = {"device_id": device_id}
    return client.get(f"list_key_codes?device_id={device_id}")

def main(api_url):
    """
    Main driver function to render the Streamlit application.

    Args:
    api_url (str): The base URL of the API.
    """
    client = CloudRunRestClient(api_url)

    st.title("Smart Lock Management")

    # List Devices to populate dropdowns
    devices_response = list_devices(client)

    try:
        devices_data = json.loads(devices_response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON response. Response body: {devices_response}") from e

    if not devices_data or "error" in devices_data:
        st.error(f"Error fetching devices: {devices_data.get('error')}")
        return

    devices = devices_data["devices"]
    device_options = {device["name"]: device["id"] for device in devices}

    # Create Key Code Section
    st.header("Create Key Code")
    with st.form("create_key_code_form"):
        username = st.text_input("Username", help="Enter the username for the key code.")
        code = st.text_input("Code (8 digits)", help="Enter an 8-digit code.")
        device_name = st.selectbox(
            "Select Device",
            options=["All Devices"] + list(device_options.keys()),
            help="Select the device if applicable. Leave as 'All Devices' if not.",
        )
        create_key_code_button = st.form_submit_button("Create Key Code")
        if create_key_code_button:
            device_id = device_options[device_name] if device_name != "All Devices" else -1
            response = create_key_code(client, username, code, device_id)
            response_data = json.loads(response)
            if "error" not in response_data:
                st.success("Key code created successfully!")
            else:
                st.error(f"Error: {response}")

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
            response = delete_key_code(client, username_delete, device_id_delete)
            response_data = json.loads(response)
            if "error" not in response_data:
                st.success("Key code deleted successfully!")
            else:
                st.error(f"Error: {response}")

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
            response = list_key_codes(client, selected_device_id)
            response_data = json.loads(response)
            if "error" not in response_data:
                st.json(response_data)
            else:
                st.error(f"Error: {response}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Smart Lock Management Streamlit app.")
    parser.add_argument("--api-url", type=str, required=True, help="URL of the Flask API")
    args = parser.parse_args()

    main(args.api_url)
