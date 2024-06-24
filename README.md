 # Hubitat Lock Manager

 Hubitat Lock Manager is a Python library to manage smart locks within the Hubitat ecosystem. It provides CRUD functionality for lock codes using Selenium WebDriver.

 ## Installation

 You can install the library using pip:

 ```
 pip install hubitat_lock_manager
 ```

 ## Usage

 ```python
 from hubitat_lock_manager.hubitat_service import HubitatManager, HubitatLockHelper

 helper = HubitatLockHelper(driver_path='path_to_chromedriver')
 manager = HubitatManager(driver_path='path_to_chromedriver', helper=helper)

 # Example usage
 manager.create_key_code(lock_id='lock1', code='1234', name='Guest')
 ```

 ## License

 This project is licensed under the MIT License - see the LICENSE file for details.
