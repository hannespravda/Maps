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
#"Komoot/TourmaletOst-1391384135.gpx",
#"Komoot/Col de Pailhères Ost-1391389212.gpx",
#"Komoot/Col de Pailhères West-1391389581.gpx",
#"Komoot/Coll d'Ordino Canillo-1391390023.gpx",
#"Komoot/Coll d'Ordino Ordino-1391390226.gpx",
#"Komoot/SoulorNord-1391901141.gpx",
#"Komoot/SoulorOst-1391900640.gpx",
#"Komoot/AspinOst-1391904086.gpx",
#"Komoot/AubisqueSoulor-1391902547.gpx",
#"Komoot/AubisqueWest-1391903386.gpx",
#"Komoot/SoulorAubisque-1391902058.gpx",
#"Komoot/AspinWest-1391905156.gpx",
#"Komoot/PeyresourdLoudenvielle-1391908793.gpx",
#"Komoot/PeyresourdNordwest-1391908256.gpx",
#"Komoot/PeyresourdOst-1391906107.gpx",
#"Komoot/MenteOst-1391913017.gpx",
#"Komoot/Portet-d'AspetOst-1391910191.gpx",
#"Komoot/Portet-d'AspetWest-1391912314.gpx",
#"Komoot/AgnesSudwest-1391914610.gpx",
#"Komoot/AgnesViaLers-1391914091.gpx",
#"Komoot/MarieBlanqueOst-1391915154.gpx",
#"Komoot/MenteWest-1391913411.gpx",
#"Komoot/LersNordWest-1391916448.gpx",
#"Komoot/LersOst-1391915987.gpx",
#"Komoot/MarieBlanqueWest-1391915552.gpx",
#"Komoot/EnvaliraAndorra-1391919617.gpx",
#"Komoot/PortillonES-1391917757.gpx",
#"Komoot/PortillonFR-1391917468.gpx",
#"Komoot/EnvaliraNordost-1391920884.gpx",
#"Komoot/JauNord-1391935118.gpx",
#"Komoot/JauOst-1391928911.gpx",
#"Komoot/BalesNord-1391946242.gpx",
#"Komoot/BalesSüd-1391945224.gpx",
#"Komoot/CoreOst-1391944135.gpx",
#"Komoot/CoreWest-1391944567.gpx",
#"Komoot/PierreMartinNordMain-1391947345.gpx",
#"Komoot/PierreMartinOst-1391949043.gpx",
#"Komoot/PierreMartinSudost-1391948450.gpx",
#"Komoot/PierreMartinNordAlt-1391950238.gpx",
#"Komoot/PierreMartinNordost-1391949870.gpx",
#"Komoot/Arcalis-1391953200.gpx",
#"Komoot/CampoImperatore-1391955636.gpx",
#"Komoot/PierreMartinColSouscousse-1391950744.gpx",
#"Komoot/PierreMartinES-1391951229.gpx",
#"Komoot/BlockhausPassoLunciano-1391956504.gpx",
#"Komoot/BlockhausRoccamorice-1391957080.gpx",
#"Komoot/LenzerheideChur-1391961642.gpx",
#"Komoot/LenzerheideTiefencastel-1391962614.gpx",
#"Komoot/LenzerheideSudI-1391963901.gpx",
#"Komoot/LenzerheideSudII-1391964599.gpx",
#"Komoot/TivoAlt-1391971275.gpx",
#"Komoot/TivoMain-1391970627.gpx",
#"Komoot/CoeNordwest-1391979767.gpx",
#"Komoot/CoeValbona-1391979479.gpx",
#"Komoot/ForcellaValbonaOst-1391978241.gpx",
#"Komoot/ForcellaValbonaOstCoe-1391979072.gpx",
#"Komoot/CoeWest-1391980068.gpx",
#"Komoot/TourmaletWest-1391383770.gpx",
#"Komoot/Port de la Bonaigua Ost-1391386156.gpx",
#"Komoot/Port de la Bonaigua West-1391386811.gpx",
]

passi_file = "passi.js"

geojson_data = gpx_to_geojson(gpx_files, output_directory, passi_file)
