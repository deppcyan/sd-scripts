import os
import argparse
from PIL import Image

def resize_images(input_folder, output_folder, target_width):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpeg', '.jpg')):
            img_path = os.path.join(input_folder, filename)
            with Image.open(img_path) as img:
                original_width, original_height = img.size
                aspect_ratio = original_height / original_width
                target_height = int(target_width * aspect_ratio)
                resized_img = img.resize((target_width, target_height), Image.LANCZOS)
                
                output_path = os.path.join(output_folder, filename)
                resized_img.save(output_path)
                print(f"Resized image saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Resize images in a folder.")
    parser.add_argument("input_folder", help="Folder containing images to resize.")
    parser.add_argument("output_folder", help="Folder to save resized images.")
    parser.add_argument("target_width", type=int, help="Target width for resizing images.")
    
    args = parser.parse_args()
    resize_images(args.input_folder, args.output_folder, args.target_width)

if __name__ == "__main__":
    main()
