import json

# Open the .js file and read the content
with open('passi.js', 'r') as f:
    # Read the file content and remove the "var passi = " part
    file_content = f.read().replace('var passi = ', '')

# Load the JSON data
data = json.loads(file_content)

# Open a text file for writing
with open('openTracks.txt', 'w') as output_file:
    # Iterate through features
    for feature in data['features']:
        # Check if the country is "nn"
        if feature['properties']['country'] == 'nn':
            # Write name and height to the text file
            output_file.write(f"idd: {feature['properties']['idd']}, Name: {feature['properties']['name']}, Height: {feature['properties']['height']}\n")
