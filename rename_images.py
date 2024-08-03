import os
import sys

def rename_files_in_directory(directory):
    # Get a sorted list of all .jpeg files in the directory
    files = sorted([f for f in os.listdir(directory) if f.endswith('.jpeg')])

    # Determine the number of digits needed for zero-padding
    num_files = len(files)
    num_digits = len(str(num_files))

    # Rename each file to a zero-padded sequential number
    for index, filename in enumerate(files, start=1):
        # Construct the old and new file paths
        old_file_path = os.path.join(directory, filename)
        
        # Format the new file name with leading zeros
        new_file_name = f"{index:0{num_digits}}.jpeg"
        new_file_path = os.path.join(directory, new_file_name)

        # Rename the file
        os.rename(old_file_path, new_file_path)
        print(f"Renamed '{filename}' to '{new_file_name}'")

def main():
    # Check if directory path is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python rename_images.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]

    # Check if the provided directory exists
    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        sys.exit(1)

    # Call the function to rename the files
    rename_files_in_directory(directory_path)

if __name__ == "__main__":
    main()

