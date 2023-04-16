import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key and API secret from environment variables
API_KEY = os.getenv("AMADEUS_API_KEY")
API_SECRET = os.getenv("AMADEUS_API_SECRET")
BASE_URL = os.getenv("AMADEUS_API_TOKEN_BASE_URL")

# Make sure both API key and API secret are available
if not API_KEY or not API_SECRET:
    raise ValueError(
        "API_KEY and API_SECRET must be \
        set in environment variables."
    )

# Send token request
response = requests.post(
    BASE_URL,
    headers={
        "Content-Type": "application/x-www-form-urlencoded",
    },
    data=(
        f"grant_type=client_credentials&client_id={API_KEY}"
        f"&client_secret={API_SECRET}"
    ),
)

# Check for successful response
if response.status_code == 200:
    # Extract access token from response
    access_token = response.json().get("access_token")
    expires_in = response.json().get("expires_in")
    if access_token:
        # Read the .env file to get the current contents
        with open(".env", "r") as env_file:
            env_lines = env_file.readlines()

        # Update the .env file with the new access token
        updated_env_lines = []
        for line in env_lines:
            # Replace the existing AMADEUS_API_ACCESS_TOKEN line
            if line.startswith("AMADEUS_API_ACCESS_TOKEN="):
                updated_env_lines.append(
                    f"AMADEUS_API_ACCESS_TOKEN=" f'"{access_token}"\n'
                )
            else:
                updated_env_lines.append(line)

        with open(".env", "w") as env_file:
            env_file.writelines(updated_env_lines)

        print(f"Access token obtained successfully: {access_token}")
        print(f"It expires in: {expires_in/60}m")
    else:
        print("Access token not found in response.")
else:
    print(f"Failed to obtain access token. Response:{response.text}")
