import os
import sys
from PIL import Image

def get_image_size(image_path):
    """Returns the size (width, height) of the image."""
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception as e:
        print(f"Error opening image {image_path}: {e}")
        return None

def find_and_delete_small_images(directory, max_width, max_height):
    """Finds images smaller than the specified size and deletes them after user confirmation."""
    if not os.path.isdir(directory):
        print("The specified directory does not exist.")
        return
    
    images_to_delete = []
    
    # Walk through all files in the directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                file_path = os.path.join(root, file)
                size = get_image_size(file_path)
                
                if size:
                    width, height = size
                    if width < max_width or height < max_height:
                        images_to_delete.append(file_path)
    
    if not images_to_delete:
        print("No images found that match the criteria.")
        return

    # List images to be deleted
    print("The following images are below the specified size and will be deleted:")
    for image_path in images_to_delete:
        print(image_path)

    # Ask user for confirmation
    confirm = input("Do you want to delete these images? (yes/no): ").strip().lower()
    if confirm == 'yes':
        for image_path in images_to_delete:
            try:
                os.remove(image_path)
                print(f"Deleted {image_path}")
            except Exception as e:
                print(f"Error deleting {image_path}: {e}")
    else:
        print("No images were deleted.")

# Example usage
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python filter_and_delete_images.py <directory> <max_width> <max_height>")
        sys.exit(1)
    
    DIRECTORY = sys.argv[1]
    MAX_WIDTH = int(sys.argv[2])
    MAX_HEIGHT = int(sys.argv[3])

    find_and_delete_small_images(DIRECTORY, MAX_WIDTH, MAX_HEIGHT)
