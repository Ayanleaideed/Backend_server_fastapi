import os
import requests
import getpass

# Define the endpoint
endpoint = "http://127.0.0.1:8000/receive-data/"
# endpoint = "https://backend-server-fastapi.vercel.app/receive-data"

# Define the token
token = "TestTokenDemo_123"  # Replace with your actual token

# Get the current username
username = getpass.getuser()

# Get list of files from a directory (Desktop in this code)
desktop_path = os.path.join("C:\\Users", username, "Desktop")
files = [f for f in os.listdir(desktop_path) if os.path.isfile(os.path.join(desktop_path, f))]

# Prepare the data payload
data = {
    "username": username,
    "files": files
}

# Set the headers to include the Authorization token
headers = {
    "Authorization": f"Bearer {token}"
}

# Send the data to the FastAPI endpoint with the token in headers
response = requests.post(endpoint, json=data, headers=headers)

# Print the response from the server
print("Response from server:", response.json())
