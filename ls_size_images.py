import os
import sys
from PIL import Image

def list_image_resolutions(folder_path):
    # Check if the folder exists
    if not os.path.isdir(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    # List all files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(('.jpeg', '.jpg')):
            file_path = os.path.join(folder_path, file_name)
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    print(f"{file_name}: {width}x{height}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <folder_path>")
        sys.exit(1)

    folder_name = sys.argv[1]
    list_image_resolutions(folder_name)
