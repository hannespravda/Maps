import json

# Open the .js file and read the content
with open('passi.js', 'r') as f:
    # Read the file content and remove the "var passi = " part
    file_content = f.read().replace('var passi = ', '')

# Load the JSON data
data = json.loads(file_content)

# Create sets to store unique idds and links
unique_idds = set()
unique_links = set()
duplicate_idds = set()
duplicate_links = set()

# Iterate through features
for feature in data['features']:
    idd = feature['properties']['idd']
    link = feature['properties']['link']

    # Check for duplicates in idd
    if idd in unique_idds:
        duplicate_idds.add(idd)
    else:
        unique_idds.add(idd)

    # Check for duplicates in link
    if link in unique_links:
        duplicate_links.add(link)
    else:
        unique_links.add(link)

# Print duplicates
print("Duplicate idds:", duplicate_idds)
print("Duplicate links:", duplicate_links)