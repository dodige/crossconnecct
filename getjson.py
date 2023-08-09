# Import requests and os modules
import requests
import os

# Define the url and the playerid
url = "https://example.com/api/json"
playerid = "123456"

# Send a GET request with the playerid as a parameter
response = requests.get(url, params={"playerid": playerid})

# Check if the response is successful
if response.status_code == 200:
    # Parse the response as a JSON object
    data = response.json()

    # Create a list of dictionaries from the JSON object
    items = data["items"]

    # Create a temp folder named medias if it does not exist
    os.makedirs("medias", exist_ok=True)

    # Loop through the items in the list
    for item in items:
        # Get the filename, type and s3url from the item
        filename = item["filename"]
        type = item["type"]
        s3url = item["s3url"]

        # Download the file from the s3url and save it in the temp folder with the filename and type
        r = requests.get(s3url)
        with open(os.path.join("medias", filename + "." + type), "wb") as f:
            f.write(r.content)

        # Print a message to indicate the download is done
        print(f"Downloaded {filename}.{type} from {s3url}")
