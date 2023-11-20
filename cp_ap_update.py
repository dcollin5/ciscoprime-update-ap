#Based on the /webacs/api/v4/op/apService/accessPoint-PUT?_docs in Cisco Prime

import requests
import re

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import json

import xml.etree.ElementTree as ET

# Load configuration from the config file
def load_config(filename):
    try:
        with open(filename, "r") as config_file:
            config = json.load(config_file)
            return config["base_url"], config["username"], config["password"]
    except FileNotFoundError:
        raise Exception("Config file not found")
    except KeyError:
        raise Exception("Config file does not contain 'base_url', 'username', and 'password' fields")
        
# Load configuration from the config file
def load_config(filename):
    try:
        with open(filename, "r") as config_file:
            config = json.load(config_file)
            return config["base_url"], config["username"], config["password"]
    except FileNotFoundError:
        raise Exception("Config file not found")
    except KeyError:
        raise Exception("Config file does not contain 'base_url', 'username', and 'password' fields")


def get_next_ap_id(list_of_aps_on_floor):

    # Extract numeric part from the last item
    last_item = list_of_aps_on_floor[-1]
    last_numeric_part = int(re.search(r'\d+$', last_item).group())

    # Increment the last numeric part by 1
    next_numeric_part = last_numeric_part + 1

    # Create the new ID
    non_numeric_part = last_item[:last_item.index(str(last_numeric_part))]
    next_id = f"{non_numeric_part}{next_numeric_part:02d}"
    print (next_id)
    return next_id


# Function to query AP name and return IP address
def get_list_of_current_aps_per_floor(base_url, username, password, ap_floor_location):

    ap_url = base_url + f"data/AccessPointDetails?.full=true&.sort=ipAddress&name=contains(%22{ap_floor_location}%22)"

    auth_headers = {
        "Content-Type": "application/json",
    }

    ap_response = requests.get(ap_url, headers=auth_headers, auth=(username, password), verify=False)

    if ap_response.status_code == 200:
        # Parse the XML content of the response
        xml_content = ap_response.text
        root = ET.fromstring(xml_content)
        
        floor_aps = []
        # Loop through the child elements of the root
        for entity in root.findall('entity'):
            #variable_element = root  # Replace with the actual element name
            # Find the entity element

            ap_name_element = entity.find(".//name")
            ap_locationHierarchy_element = entity.find(".//locationHierarchy").text

            #print (name_element.text)
        
            if ap_name_element is not None:
                floor_aps.append(ap_name_element.text)

            else:
                print("ap_name_element  not found in the XML.")
                
        # Sort the list
        floor_aps.sort()
        for item in floor_aps:
            print(f"- {item}")
        
        return floor_aps, ap_locationHierarchy_element
    else:
        raise Exception(f"Failed to query AP info for AP name: {ap_floor_location}")


# Function to query AP name and return IP address
def get_ap_accessPointId_info(base_url, username, password, ap_name):

    ap_url = base_url + f"data/AccessPoints?.full=true&.sort=ipAddress&name=endsWith(%22{ap_name}%22)"
    auth_headers = {
        "Content-Type": "application/json",
    }

    ap_response = requests.get(ap_url, headers=auth_headers, auth=(username, password), verify=False)

    if ap_response.status_code == 200:
        # Parse the XML content of the response
        xml_content = ap_response.text
        root = ET.fromstring(xml_content)
        print (xml_content)
        # Find the 'accessPointsDTO' element and get the value of the 'id' attribute
        accessPointId = root.find(".//accessPointsDTO").attrib.get('id')

        if accessPointId is not None:
            accessPointId = str(accessPointId)

        else:
            print("Address element not found in the XML.")
        
        return accessPointId
    else:
        raise Exception(f"Failed to query AP info for AP name: {ap_name}")
        
# Function update AP name and 
def update_ap_name_and_locationHierarchy(ap_id, new_ap_name, ap_locationHierarchy_element):
    #write something.
    print (ap_locationHierarchy_element)
    ap_url = base_url + f"op/apService/accessPoint"
    print ("ap_url: " + ap_url)
    auth_headers = {
        "Content-Type": "text/xml",
    }

    xml_payload = """<?xml version="1.0" ?>
<unifiedApDetailsDTO>
  <accessPointId>{}</accessPointId>
  <name>{}</name>
  <location>{}</location>
  <mapLocation>{}</mapLocation>
  <locationHierarchy>{}</locationHierarchy>
  </unifiedApDetailsDTO>
    """.format(ap_id,new_ap_name,ap_locationHierarchy_element,ap_locationHierarchy_element,ap_locationHierarchy_element)
    #

    ap_response = requests.put(ap_url, headers=auth_headers, auth=(username, password), verify=False, data=xml_payload)
    if ap_response.status_code == 200:
        # Parse the XML content of the response
        xml_content_response = ap_response.text
        #root = ET.fromstring(xml_content_response)
        print (xml_content_response)

    else:
        raise Exception(f"Failed to query AP info for AP name: {new_ap_name}")
    
# Main function to loop through a file
if __name__ == "__main__":
    try:
        base_url, username, password = load_config("config.json")

        # Read AP names from a file (one per line)
        with open("new_ap_names.txt", "r") as file:
            print("Read file in list of APs to check IP addresses")
            for line in file:
                # Strip leading and trailing whitespaces from the line
                stripped_line = line.strip()

                # Split the line into a list of strings using whitespace as the delimiter
                ap_names = stripped_line.split()
                #new_ap_name = next_available_ap_name(ap_names[0])
                list_of_aps_on_floor, ap_locationHierarchy_element = get_list_of_current_aps_per_floor(base_url, username, password, ap_names[1])
                
                #increment these IPs to get next AP ID
                new_ap_name = get_next_ap_id(list_of_aps_on_floor)
                
                #Get accessPointDetailsDTO ID
                accessPointId = get_ap_accessPointId_info (base_url, username, password, ap_names[0])
                
                print("Change AP name From: " + ap_names[0])
                print ("To New AP Name: " + new_ap_name )
                print ("Adding to Floor: " + ap_locationHierarchy_element)
                print ("AP accessPointId: " + accessPointId)
                
                #Update old AP name 'ap_names' with new AP name 'new_ap_name'
                update_ap_name_and_locationHierarchy(accessPointId,new_ap_name, ap_locationHierarchy_element)
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")

