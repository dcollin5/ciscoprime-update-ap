# ciscoprime-update-ap
Script that will update cisco prime with a new AP name, and location.

# 
If you provide the "CurrentAPName Location" in the new_ap_names.txt file, such as "AP68d1.61dd.dddd AP-154-01," the script will execute to perform a Cisco Prime update. The script dynamically determines the next available AP name according to the location and increments the highest value by 1. 
It's important to ensure that the APs are online for the script to function correctly.
