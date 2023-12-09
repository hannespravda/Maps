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

def search_passi_file(idd, passi_file_path):
    # Search for idd in the "passi" file
    with open(passi_file_path, 'r') as passi_file:
        for line in passi_file:
            if f'"idd":"{idd}"' in line:
                return True
    return False

def add_new_element_to_file(idd, height, passName, category, country, passLink, long, lat, output_file_path):
    # Write the new element to the "NewElements.txt" file
    new_element = f'{{"type":"Feature","properties":{{"idd":"{idd}","height":"{height}","name":"{passName}","category":"{category}","country":"{country}","link":"{passLink}"}}, "geometry":{{"type":"Point","coordinates":[{long}, {lat}]}}}},'
    with open(output_file_path, 'a') as new_elements_file:
        #new_elements_file.write(new_element)
        new_elements_file.seek(0, os.SEEK_END)
        new_elements_file.write(new_element)

def gpx_to_geojson(gpx_file_paths, output_directory, passi_file_path):
    features = []
    passi_check_counter = 0
    gpx_file_name = os.path.splitext(os.path.basename(gpx_file_paths[0]))[0]
    
    idd = input("Enter idd for {}: ".format(gpx_file_name))
    category = input("Enter category for {}: ".format(gpx_file_name))
    country = input("Enter country for {}: ".format(gpx_file_name))

    for gpx_file_path in gpx_file_paths:
        # Check if idd exists in "passi" file
        if passi_check_counter == 0 and not search_passi_file(idd, passi_file_path):
            passi_check_counter += 1
            passName = input("Enter Pass Name for {}: ".format(gpx_file_path))
            #passHeight = input("Enter height for {}: ".format(gpx_file_path))
            passLink = input("Enter Pass Link for {}: ".format(gpx_file_path))
            
            with open(gpx_file_path, 'r') as gpx_file:
                gpx = gpxpy.parse(gpx_file)
                last_trackpoint = gpx.tracks[0].segments[0].points[-1]
                passHeight = round(last_trackpoint.elevation)
                long = last_trackpoint.longitude
                lat = last_trackpoint.latitude

            # Add new element to "NewElements.txt" file
            add_new_element_to_file(idd, passHeight, passName, category, country, passLink, long, lat, "NewElements.txt")
        
        name = input("Enter Track Name for {}: ".format(gpx_file_path))
        link = input("Enter Track Link for {}: ".format(gpx_file_path))

        

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
    leaflet_code = f"""addGeoJSONTrack(map, geoJSONs, geoJSONArray, {XX});\n"""
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
#"Komoot/EttalerSattelWest-1389226786.gpx",
#"Komoot/GrießenpassFieberbrunn-1389230060.gpx",
#"Komoot/GrießenpassOst-1389231789.gpx",
#"Komoot/CroceSalvenMalegno-1387049277.gpx",
#"Komoot/CroceSalvenNord-1387049355.gpx",
#"Komoot/PassabochePisogne-1387049711.gpx",
#"Komoot/PassabochePisogneII-1387049822.gpx",
#"Komoot/PassabocheSanZeno-1387049988.gpx",
#"Komoot/SanFermoSud-1387050691.gpx",
#"Komoot/SanFermoWest-1387051061.gpx",
#"Komoot/MariaEck Siegsdorf-1387312381.gpx",
#"Komoot/MariaEckKleineStraße-1387312636.gpx",
#"Komoot/Masererpass Reit Winkl-1387310263.gpx",
#"Komoot/MasererpassMarquartstein-1387311497.gpx",
#"Komoot/NiklasreuthAu-1387314608.gpx",
#"Komoot/NiklasreuthAuSüd-1387314937.gpx",
#"Komoot/NiklasreuthWörnsmühl-1387316006.gpx",
#"Komoot/RossmettlenAndermatt-1388812487.gpx",
#"Komoot/NiklasreuthMiesbbach-1388918664.gpx",
#"Komoot/NiklasreuthMiesbbachNord-1388919365.gpx",
#"Komoot/Val Bavona-1388813769.gpx",
#"Komoot/MonteGeneroso-1388941390.gpx",
#"Komoot/NiklasreuthNord-1388919640.gpx",
#"Komoot/ValDiMuggioAlt-1388942230.gpx",
#"Komoot/ValDiMuggioMain-1388942460.gpx",
#"Komoot/AlpeGiumello-1388945856.gpx",
#"Komoot/Hohenschäftlarn-1389175766.gpx",
#"Komoot/LudwigshöheKleineRampe-1389171628.gpx",
#"Komoot/LudwigshöheSüd-1389172145.gpx",
#"Komoot/AufkirchenBachhausen-1389189418.gpx",
#"Komoot/AufkirchenBerg-1389190199.gpx",
#"Komoot/HohenschäftlarnAbikurve-1389178581.gpx",
#"Komoot/Leutstetten-1389195777.gpx",
#"Komoot/HochbergSiegsdorf-1389203607.gpx",
#"Komoot/HochbergSüdost-1389204550.gpx",
#"Komoot/HochbergTraunstein-1389205813.gpx",
#"Komoot/LeutstettenOlympia-1389196424.gpx",
#"Komoot/BichlpassOst-1389212006.gpx",
#"Komoot/RiedlNord-1389210179.gpx",
#"Komoot/RiedlOst-1389209602.gpx",
#"Komoot/RiedlWest-1389208702.gpx",
#"Komoot/BichlpassNord-1389212609.gpx",
#"Komoot/Eibsee-1389223431.gpx",
#"Komoot/KesselbergKochel-1389222358.gpx",
#"Komoot/KesselbergWalchensee-1389221274.gpx",
#"Komoot/EttalerSattelOst-1389224808.gpx",
]

passi_file = "passi.js"

geojson_data = gpx_to_geojson(gpx_files, output_directory, passi_file)
