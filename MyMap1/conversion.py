import gpxpy
import geojson
import os
import re

def extract_elevation_up(desc):
    # Use regular expression to extract elevation up from the desc string
    match = re.search(r'Elevation up: (\d+(\.\d+)?)m', desc)
    if match:
        return float(match.group(1))
    else:
        return None

def gpx_to_geojson(gpx_file_paths, output_directory):
    features = []

    for gpx_file_path in gpx_file_paths:
        # Get input from the user for each track's properties
        idd = input("Enter idd for {}: ".format(gpx_file_path))
        name = input("Enter name for {}: ".format(gpx_file_path))
        #length = input("Enter length for {}: ".format(gpx_file_path))
        #elevation = input("Enter elevation for {}: ".format(gpx_file_path))
        category = input("Enter category for {}: ".format(gpx_file_path))
        country = input("Enter country for {}: ".format(gpx_file_path))
        link = input("Enter link for {}: ".format(gpx_file_path))

        with open(gpx_file_path, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                coordinates = [(point.longitude, point.latitude, point.elevation) for point in segment.points]
                line_string = geojson.LineString(coordinates)
                
                distance = round(track.length_3d()/1000, 1)

                # Extract elevation-up from desc
                elevation_up = round(extract_elevation_up(track.description),0)

                # Add properties to the GeoJSON feature
                properties = {
                    "idd": idd,
                    "name": name,
                    "length": distance,
                    "elevation": elevation_up,
                    "category": category,
                    "country": country,
                    "link": link
                }

                feature = geojson.Feature(geometry=line_string, properties=properties)
                features.append(feature)

    feature_collection = geojson.FeatureCollection(features)

    write_leaflet_code_to_file(feature_collection, output_directory)
    
    return feature_collection

def write_leaflet_code_to_file(geojson_data, output_directory):
    # Get input from the user for XX
    XX = input("Enter variable name: ")
    geojson_str = geojson.dumps(geojson_data, indent=2)
    modified_geojson_str = f"var {XX} = {geojson_str}"
    geojson_data = modified_geojson_str
    # Create the Leaflet JavaScript code string
    leaflet_code = f"""
var g{XX} = L.geoJSON({XX}, {{
    style: TrackStyle,
    onEachFeature: onEachFeature
}});
var id{XX} = {XX}.features[0].properties.idd;
geoJSONArray[id{XX}] = g{XX};
geoJSONs.push(g{XX});
"""
    # Write the code to a text file
    output_file_path = os.path.join(output_directory, f"{XX}.js")
    with open(output_file_path, 'w') as output_file:
        #geojson.dump(geojson_data, output_file)
        output_file.write(modified_geojson_str)
    
    output_text_file_path = "variableTags.txt"
    with open(output_text_file_path, 'a') as output_file:
        output_file.write(leaflet_code)
        
    script_tag = f'<script src="Tracks/{XX}.js"></script>\n'
    script_file_path = "scriptTags.txt"
    with open(script_file_path, 'a') as script_file:
        script_file.write(script_tag)
#################################################################################################################
output_directory = "GeoTracks/"
gpx_files = [

"Komoot/PenserJochSterzing 16.0 1270-1383079283.gpx",
"Komoot/PenserJochBozen 47.2 2040-1383079061.gpx",
   
]

geojson_data = gpx_to_geojson(gpx_files, output_directory)

