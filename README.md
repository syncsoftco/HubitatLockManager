# Hubitat Lock Manager

Hubitat Lock Manager is a Python library for managing smart locks within the Hubitat ecosystem. It provides CRUD functionality for lock codes using Selenium WebDriver.

## Installation

You can install the library using pip:

```bash
pip install git+https://github.com/syncsoftco/HubitatLockManager@v0.0.95
```

## Usage

```python
from hubitat_lock_manager.hubitat_service import HubitatManager, HubitatLockHelper

# Initialize the helper and manager with the path to the chromedriver
helper = HubitatLockHelper(driver_path='path_to_chromedriver')
manager = HubitatManager(driver_path='path_to_chromedriver', helper=helper)

# Example usage: Create a new key code
create_params = {
    'device_id': 1,        # Replace with your device ID
    'code': '1234',        # The lock code to set
    'username': 'user1'    # The username associated with the lock code
}
manager.create_key_code(**create_params)

# Example usage: Delete a key code
delete_params = {
    'device_id': 1,        # Replace with your device ID
    'username': 'user1'    # The username associated with the lock code
}
manager.delete_key_code(**delete_params)

# Example usage: List all key codes
key_codes = manager.list_key_codes(device_id=1)  # Replace with your device ID
for code in key_codes:
    print(f"Username: {code['username']}, Code: {code['code']}")
```

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
