# Import requests and os modules
import requests
import os

# Define the url and the playerid
#url1 = "https://s3.ca-central-1.amazonaws.com/gospelgeneration.com/dd.json"
url1 = "https://nnd9o86k93.execute-api.ca-central-1.amazonaws.com/default/ccData?playerid=123456"
playerid = "123456"

# Send a GET request with the playerid as a parameter
response = requests.get(url1, params={"playerid": playerid})

# Check if the response is successful
if response.status_code == 200:
    # Parse the response as a JSON object
    data = response.json()


    # Check if the json has a tagged name dontreload
    if data.get("dontreload") ==  True:
        # Print a message and stop execution
        print("The json file has a dontreload tag. No action is taken.")
        exit()


    # Create a list of dictionaries from the JSON object
    items = data["items"]

    # Create a temp folder named medias if it does not exist
    os.makedirs("medias", exist_ok=True)

    # Define a function to download a file from a url
    def downloadFile(url, filename):
        # Send a GET request to the url
        r = requests.get(url, stream=True)

        # Check if the response is successful
        if r.status_code == 200:
            # Open a file in the medias folder with the same filename as in the url
            with open(os.path.join("medias", filename), "wb") as f:
                # Write the content of the response to the file
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)

            # Print a message to indicate the file is downloaded
            print(f"Downloaded {filename}")

        else:
            # Print an error message if the response is not successful
            print(f"Error downloading {filename}: {r.status_code}")

    # Define a function to create a playlist file
    def createPlaylist(items):
        # Create a text file named playlistupdating.txt in the medias folder
        with open(os.path.join("medias", "playlistupdating.txt"), "w") as f:
            # Write a message to indicate the playlist is being updated
            f.write("Playlist is being updated...\n")

        # Open a file named playlist.m3u in write mode
        with open(os.path.join("medias", "playlist.m3u"), "w") as f:
            # Write the header of the playlist file
            f.write("#EXTM3U\n")

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

        # Delete the text file named playlistupdating.txt from the medias folder
        os.remove(os.path.join("medias", "playlistupdating.txt"))

    # Loop through the items in the list
    for item in items:
        # Get the url and filename from the item
        url = item["s3url"]
        filename = item["filename"] + "." + item["type"]

        # Download the file from the url and save it in the medias folder with the same filename
        downloadFile(url, filename)

    # Create a playlist file from the items in the list after all files have been downloaded
    createPlaylist(items)

else:
    # Print an error message if the response is not successful
    print(f"Error getting data: {response.status_code}")
