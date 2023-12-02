import gpxpy

def write_coordinates_to_text(gpx_path, output_text_path):
    with open(gpx_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    with open(output_text_path, 'w') as output_file:
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    # Write the coordinates with elevation to the text file
                    output_file.write(f"[{point.longitude},{point.latitude},{point.elevation}],\n")

# Example usage
gpx_path = "Komoot/AchenpassWiesing  34.3 660-1382781179.gpx"
output_text_path = "coordinates.txt"
write_coordinates_to_text(gpx_path, output_text_path)