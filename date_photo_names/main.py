import pathlib
from datetime import datetime
import shutil
import os

# Directories to scan for files.
directories = ["C:/Media/"]

# Directory where all the files will be moved to.
target_directory = "C:/RenamedMedia"

# User needs to guarantee that none of the directories contain a file with the following name:
temp_filename = "################################################################################################################################"

if not os.path.exists(target_directory):
    os.mkdir(target_directory)
else:
    assert len(os.listdir(target_directory)) == 0, "Target directory must be empty"

class File():
    def __init__(self, name: str, directory: str, timestamp: str):
        # Name of the file including its extension.
        self.name = name
        # Directory of the file.
        self.directory = directory
        # Earliest timestamp string of a file's creation or modification.
        self.timestamp = timestamp

files = []

# Key: 
# Value: number of occurences of the timestamp in the file list.
timestamps = {}

# Populate the file list by 
for directory in directories:
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        file_object = pathlib.Path(path)
        if file_object.exists():
            # Time when the file was created.
            creation_time = datetime.fromtimestamp(file_object.stat().st_ctime)
            # Time when the file was last modified.
            modification_time = datetime.fromtimestamp(file_object.stat().st_mtime)
            # Find the earlier of the two times as copying may change the creation time to be later.
            timestamp = min(creation_time, modification_time) 
            # Format the timestamp into the desired string style
            timestamp = timestamp.strftime("%Y-%m-%d %H-%M")
            files.append(File(filename, directory, timestamp))

for index, file in enumerate(files):
    # Check if timestamp exists in dictionary, 
    # it it does, increment the occurences of the timestamp, 
    # if not, make the entry 1.
    if file.timestamp in timestamps.keys():
        timestamps[file.timestamp] += 1
    else:
        timestamps[file.timestamp] = 1
    # Current full path of the file.
    current_path = os.path.join(file.directory, file.name)
    # Find file extension for renaming the file properly.
    _, extension = os.path.splitext(current_path)
    # Generate a new name for the file.
    new_filename = file.timestamp + " " + str(timestamps[file.timestamp]) + extension
    # Full path for the temporary file (for renaming).
    temp_path = os.path.join(file.directory, temp_filename + extension)
    # Rename file to temporary file.
    os.rename(current_path, temp_path)
    # Move file to target directory.
    shutil.move(temp_path, target_directory)
    # Rename the file at the target location to the final desired file path.
    os.rename(os.path.join(target_directory, temp_filename + extension), os.path.join(target_directory, new_filename))
    # Print every 1000 files processed.
    if index % 1000 == 0:
        print(str(index) + "/" + str(len(files)) + " files processed...")

print("File renaming and moving complete!")