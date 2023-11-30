# Cisco Prime AP Name and Location Updater Script

## Overview

This Python script streamlines the process of updating Cisco Prime with new Access Point (AP) names and locations. By providing the current AP name and location in the `new_ap_names.txt` file, the script dynamically determines the next available AP name for the specified location and increments the highest value by 1. The primary requirement for the script's successful execution is that the APs involved are online.

## Features

1. **Dynamic AP Naming:** The script intelligently calculates the next available AP name for a given location, ensuring a systematic and organized approach to AP naming.

2. **Location-Based Updates:** Updates are location-specific, allowing for efficient management of APs within different areas or zones.

3. **Input File Support:** The script reads input data from the `new_ap_names.txt` file, simplifying the process of updating multiple APs in one go.

4. **Online AP Verification:** The script checks for the online status of APs to ensure that the update process is performed accurately.

## Usage

1. **Input File Format:**
   - The `new_ap_names.txt` file should contain entries in the format: `CurrentAPName Location`, where "CurrentAPName" is the existing AP name, and "Location" is the desired location for the AP.

     Example:
     ```
     AP68d1.61dd.dddd AP-154-01
     ```

2. **Execution:**
   - Run the script with the following command:
     ```bash
     python update_cisco_prime.py
     ```

3. **Output:**
   - The script will update Cisco Prime with the new AP names and locations as specified in the input file.

## Important Notes

- **Online AP Requirement:**
  - Ensure that the APs mentioned in the input file are online during script execution for accurate updates.

- **Sequential Naming:**
  - The script relies on sequential naming for APs within a given location. Ensure that the existing AP names follow a numeric pattern for successful dynamic naming.

- **Cisco Prime Compatibility:**
  - This script is designed for compatibility with Cisco Prime infrastructure. Verify the compatibility with your specific Cisco Prime version before use.

## Contribution and Issues

Feel free to contribute to the script or report any issues on the [GitHub repository](https://github.com/your-username/cisco-prime-updater).

## License

This script is licensed under the [MIT License](LICENSE), granting you the freedom to modify and distribute the code for your purposes.
