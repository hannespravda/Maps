import xml.etree.ElementTree as ET
import os

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
        search_str = f'[\n            {search_array[0]},\n            {search_array[1]}\n          ]'
        replace_str = str(replace_array)
        search_str1 = f'[{search_array[0]}, {search_array[1]}]'

        if search_str in js_content:
            js_content = js_content.replace(search_str, replace_str)
            match_counter += 1
            
        if search_str1 in js_content:
            js_content = js_content.replace(search_str1, replace_str)
            match_counter += 1

    return js_content, match_counter

if __name__ == "__main__":
    gpx_folder = "Komoot1"
    js_folder = "Tracks2"

    for gpx_file_name in os.listdir(gpx_folder):
        if gpx_file_name.endswith(".gpx"):
            gpx_file_path = os.path.join(gpx_folder, gpx_file_name)
            gpx_data = read_gpx(gpx_file_path)

            for js_file_name in os.listdir(js_folder):
                if js_file_name.endswith(".js"):
                    js_file_path = os.path.join(js_folder, js_file_name)

                    try:
                        with open(js_file_path, "r") as js_file:
                            js_content = js_file.read()
                    except FileNotFoundError:
                        print(f"JavaScript file not found: {js_file_path}")
                        continue

                    updated_js_content, match_counter = replace_coordinates(js_content, gpx_data)

                    with open(js_file_path, "w") as updated_js_file:
                        updated_js_file.write(updated_js_content)

                    print(f"Replacement complete for {js_file_name}. Matches found: {match_counter} in {gpx_file_name}")