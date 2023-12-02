import xml.etree.ElementTree as ET

def read_gpx(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Define the namespace
    ns = {'gpx': 'http://www.topografix.com/GPX/1/1'}

    coordinates_with_elevation = []
    for trkpt in root.findall(".//gpx:trkpt", namespaces=ns):
        lat = float(trkpt.get("lat"))
        lon = float(trkpt.get("lon"))
        elevation = float(trkpt.find("gpx:ele", namespaces=ns).text)
        coordinates_with_elevation.append({"lon": lon, "lat": lat, "ele": elevation})

    return coordinates_with_elevation
    

def replace_coordinates(js_content, gpx_data):
    match_counter = 0

    for gpx_coord in gpx_data:
        lon, lat, elevation = gpx_coord["lon"], gpx_coord["lat"], gpx_coord["ele"]
        search_array = [lon, lat]
        replace_array = [lon, lat, elevation]

        # Convert arrays to strings for searching in the JavaScript content
        search_str = f'[{search_array[0]}, {search_array[1]}]'
        replace_str = str(replace_array)

        if search_str in js_content:
            js_content = js_content.replace(search_str, replace_str)
            match_counter += 1

    return js_content, match_counter

if __name__ == "__main__":
    gpx_file_path = "Komoot/AllosNord 17.3 1140-1382806286.gpx" #"Komoot/AllosSud 33.7 1190-1382805780.gpx"
    js_file_path = "Tracks1/Allos.js"

    try:
        with open(js_file_path, "r") as js_file:
            js_content = js_file.read()
    except FileNotFoundError:
        print(f"JavaScript file not found: {js_file_path}")
        exit()

    gpx_data = read_gpx(gpx_file_path)
    updated_js_content, match_counter = replace_coordinates(js_content, gpx_data)

    with open(js_file_path, "w") as updated_js_file:
        updated_js_file.write(updated_js_content)

    print(f"Replacement complete. Updated JavaScript file saved. Matches found: {match_counter}")
