# Import requests and os modules
import requests
import os

# Define the url and the playerid
url = "https://s3.ca-central-1.amazonaws.com/gospelgeneration.com/dd.json"
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

    # Define a function to create a playlist file
    def createPlaylist(items):
        # Open a file named playlist.m3u in write mode
        with open(os.path.join("medias", "playlist.m3u"), "w") as f:
            # Write the header of the playlist file
            #f.write("#EXTM3U\n")

            # Loop through the items in the list
            for item in items:
                # Get the filename, type, startdate, enddate and priority from the item
                filename = item["filename"]
                type = item["type"]
                startdate = item["startdate"]
                enddate = item["enddate"]
                priority = item["priority"]

                # Write the metadata of the file in the playlist file
                #f.write(f"#EXTINF:-1, {filename}.{type}\n")
                #f.write(f"#EXT-X-START-DATE:{startdate}\n")
                #f.write(f"#EXT-X-END-DATE:{enddate}\n")
                #f.write(f"#EXT-X-PRIORITY:{priority}\n")

                # Write the path of the file in the playlist file
                f.write(os.path.join("/home/pi/medias", filename + "." + type) + "\n")

        # Print a message to indicate the playlist file is created
        print("Created playlist.m3u")

    # Call the function to create the playlist file
    createPlaylist(items)

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
