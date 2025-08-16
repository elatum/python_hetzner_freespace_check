import requests
import json
import os

# https://console.hetzner.com/projects/
# It is highly recommended to use environment variables for sensitive data
#  export HETZNER_API_TOKEN="[YOUR_API_TOKEN]"
#  export HETZNER_STORAGE_BOX_ID="[YOUR_STORAGE_BOX_ID]"
# API_TOKEN = os.environ.get("HETZNER_API_TOKEN")
# STORAGE_BOX_ID = os.environ.get("HETZNER_STORAGE_BOX_ID")

API_TOKEN = "[YOUR_API_TOKEN]"
STORAGE_BOX_ID = "[YOUR_STORAGE_BOX_ID]"
fs_threshold=300 #GB
GOOGLE_CHAT_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/????????/messages?key=?????????????????&token=???????????????????" 
ret_msg = ""

def send_google_chat_message(webhook_url, message_text):
        """
        Sends a text message to a Google Chat space using an incoming webhook.

        Args:
            webhook_url (str): The URL of the Google Chat incoming webhook.
            message_text (str): The text content of the message to send.
        """
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        payload = {
            'text': message_text
        }
        
        try:
            response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            print(f"Message sent successfully. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending message: {e}")







if not API_TOKEN or not STORAGE_BOX_ID:
    print("Error: HETZNER_API_TOKEN and HETZNER_STORAGE_BOX_ID environment variables must be set.")
    exit()

API_URL = f"https://api.hetzner.com/v1/storage_boxes/{STORAGE_BOX_ID}"
# API_URL = f"https://api.hetzner.cloud/v1/storage_boxes/"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}


try:
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    data = response.json()
    storage_box = data.get("storage_box")
    storage_box_type = storage_box.get("storage_box_type")

    # Extract the storage usage details
    sb_stats = storage_box.get("stats")
    
    print(storage_box_type)
    if sb_stats:
        # The API returns the usage in bytes.
        size = storage_box_type.get("size")
        size_data = sb_stats.get("size_data")
        
        # Convert bytes to a more readable format (e.g., GB or TB)
        # 1 GB = 1024 * 1024 * 1024 bytes
        size_gb = size / (1024**3)
        used_gb = size_data / (1024**3)
        free_space = round(size_gb - used_gb)
        print(free_space)

        print("Hetzner Storage Box Usage:")
        print(f"Total Size: {size_gb:.2f} GB")
        print(f"Used Space: {used_gb:.2f} GB")
        print(f"Free Space: {(size_gb - used_gb):.2f} GB")
    else:
        print("Error: 'storage_box' key not found in the API response.")

except requests.exceptions.RequestException as e:
    print(f"An error occurred while making the API request: {e}")
except json.JSONDecodeError as e:
    print(f"An error occurred while parsing the JSON response: {e}")


if free_space < fs_threshold:
    #TOO LITTLE FREESPACE
    ret_msg = f"Hetzner [PROBLEM] - Freespace is less than {fs_threshold}GB"
    ret_msg =  ret_msg + " (from tasksched on PC)"
    print(ret_msg)

    try:
        send_google_chat_message(GOOGLE_CHAT_WEBHOOK_URL, ret_msg)
    except requests.exceptions.HTTPError as err:
        print(f"Error sending message: {err}")

else:
    ret_msg = f"NO WORRIES - FREESPACE IS MORE THAN {fs_threshold}GB"
    print(ret_msg)
    print("No notification sent")




