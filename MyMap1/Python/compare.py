import json
import os

# Open the .js file and read the content
with open('passi.js', 'r') as f:
    # Read the file content and remove the "var passi = " part
    file_content = f.read().replace('var passi = ', '')

# Load the JSON data
data = json.loads(file_content)

# Iterate through features in passi.js
for feature in data['features']:
    # Check if the link property starts with "https"
    if feature['properties']['link'].startswith('https'):
        idd = feature['properties']['idd']

        # Search for the term "#{idd}" in all .js elements inside the 'Tracks' folder
        found_match = False
        tracks_folder = 'Tracks'
        for filename in os.listdir(tracks_folder):
            if filename.endswith(".js"):
                with open(os.path.join(tracks_folder, filename), 'r', encoding='utf-8', errors='ignore') as track_file:
                    track_content = track_file.read()
                    if f'"{idd}"' in track_content:
                        found_match = True
                        break

        # If no match is found, print the idd to the console
        if not found_match:
            print(f"No match found for idd: {idd}")