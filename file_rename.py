import os

def rename_files(folder_path):
    # Get the list of files in the folder
    files = os.listdir(folder_path)
    
    for file_name in files:
        # Check if the file name contains the specified prefix
        if 'SpotMate.online - ' in file_name:
            # Construct the new file name by removing the prefix
            new_file_name = file_name.replace('SpotMate.online - ', '')
            
            # Rename the file
            os.rename(os.path.join(folder_path, file_name), os.path.join(folder_path, new_file_name))
            print(f"Renamed '{file_name}' to '{new_file_name}'")
    
    print("All files renamed successfully.")

# Replace 'folder_path' with the path to your folder
folder_path = 'C:/Users/kanov/Music/techno'

# Call the function to rename files in the specified folder
rename_files(folder_path)