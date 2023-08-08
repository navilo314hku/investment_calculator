import os 
def CreateFolderIfNotExist(directory):
    if not os.path.exists(directory):
        # Create the directory
        os.makedirs(directory)
        print(f"Directory created: {directory}")
    else:
        print(f"Directory already exists: {directory}")