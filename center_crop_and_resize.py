import os
import sys
from PIL import Image

def center_crop_and_resize(image_path, target_size, output_path):
    """Crops the image to the center and resizes it to the target size."""
    try:
        with Image.open(image_path) as img:
            # Calculate crop box
            width, height = img.size
            new_size = min(width, height)
            left = (width - new_size) / 2
            top = (height - new_size) / 2
            right = (width + new_size) / 2
            bottom = (height + new_size) / 2

            # Perform the crop
            img_cropped = img.crop((left, top, right, bottom))
            
            # Resize the cropped image
            img_resized = img_cropped.resize((target_size, target_size), Image.LANCZOS)

            # Save the result
            img_resized.save(output_path)
            print(f"Processed and saved {output_path}")

    except Exception as e:
        print(f"Error processing image {image_path}: {e}")

def process_images(source_dir, target_dir, target_size):
    """Processes all images in the source directory by cropping and resizing them."""
    if not os.path.isdir(source_dir):
        print("The specified source directory does not exist.")
        return
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_path, source_dir)
                target_path = os.path.join(target_dir, relative_path)

                target_dir_path = os.path.dirname(target_path)
                if not os.path.exists(target_dir_path):
                    os.makedirs(target_dir_path)

                center_crop_and_resize(source_path, target_size, target_path)

# Example usage
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python center_crop_and_resize.py <source_dir> <target_dir> <target_size>")
        sys.exit(1)
    
    SOURCE_DIR = sys.argv[1]
    TARGET_DIR = sys.argv[2]
    TARGET_SIZE = int(sys.argv[3])

    process_images(SOURCE_DIR, TARGET_DIR, TARGET_SIZE)
