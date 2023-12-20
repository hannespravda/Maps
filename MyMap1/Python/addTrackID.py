import os
import json

folder_path = 'Tracks'

def add_track_ids(file_path, start_index):
    try:
        with open(file_path, 'r') as file:
            # Read the content of the file
            content = file.read()

            # Extract JSON data by removing "var {file_name} =" from the beginning
            json_start = content.find('{')
            if json_start != -1:
                json_data = content[json_start:]
                data = json.loads(json_data)

                # Update trackIDs
                num_features = len(data['features'])
                for feature_index, feature in enumerate(data['features']):
                    feature['properties']['trackID'] = start_index + feature_index

                # Add "var {file_name} =" at the beginning
                content = f'var {os.path.splitext(os.path.basename(file_path))[0]} = ' + json.dumps(data, indent=2)

                # Save the modified data back to the file
                with open(file_path, 'w') as file:
                    file.write(content)

                print(f'File {file_path} has been updated with trackIDs.')
                return num_features
            else:
                raise ValueError('Invalid file format')

    except Exception as e:
        print(f'Error processing {file_path}: {str(e)}')
        return 0

def process_files():
    success_count = 0
    start_index = 0

    for index, file_name in enumerate(sorted(os.listdir(folder_path))):
        if file_name.endswith('.js'):
            file_path = os.path.join(folder_path, file_name)
            
            try:
                # Process the file and get the number of features
                num_features = add_track_ids(file_path, start_index)
                start_index += num_features
                success_count += 1
            except Exception as e:
                print(f'Error processing {file_path}: {str(e)}')

    #print(f'\nSuccessfully processed {success_count} files.')

if __name__ == "__main__":
    process_files()
