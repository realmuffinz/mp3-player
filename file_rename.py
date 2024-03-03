import os

def rename_files(folder_path):
    files = os.listdir(folder_path)
    
    for file_name in files:
        if 'SpotMate.online - ' in file_name:
            # Construct the new file name by removing the prefix
            new_file_name = file_name.replace('SpotMate.online - ', '')
            
            # Rename the file
            os.rename(os.path.join(folder_path, file_name), os.path.join(folder_path, new_file_name))
            print(f"Renamed '{file_name}' to '{new_file_name}'")
    
    print("All files renamed successfully.")

# Replace 'folder_path' with the path to your folder
folder_path = 'C:/your/path/to/folder'

rename_files(folder_path)