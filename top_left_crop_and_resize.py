import os
import sys
from PIL import Image

def top_left_crop_and_resize(image_path, target_size, output_path):
    """Crops the image from the top-left corner and resizes it to the target size."""
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            
            # Calculate crop box for top-left corner
            new_size = min(width, height)
            right = new_size
            bottom = new_size

            # Perform the crop
            img_cropped = img.crop((0, 0, right, bottom))
            
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
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_path, source_dir)
                target_path = os.path.join(target_dir, relative_path)

                target_dir_path = os.path.dirname(target_path)
                if not os.path.exists(target_dir_path):
                    os.makedirs(target_dir_path)

                top_left_crop_and_resize(source_path, target_size, target_path)

# Example usage
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python top_left_crop_and_resize.py <source_dir> <target_dir> <target_size>")
        sys.exit(1)
    
    SOURCE_DIR = sys.argv[1]
    TARGET_DIR = sys.argv[2]
    TARGET_SIZE = int(sys.argv[3])

    process_images(SOURCE_DIR, TARGET_DIR, TARGET_SIZE)
