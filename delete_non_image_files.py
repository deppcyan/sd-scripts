import os
import argparse

# List of allowed file extensions (e.g., txt, jpg, png)
ALLOWED_EXTENSIONS = {'.jpeg', '.jpg', '.png'}

def list_files(directory):
    """List all files in the directory."""
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def get_file_extension(file_name):
    """Return the file extension of the given file name."""
    return os.path.splitext(file_name)[1].lower()

def main(directory):
    if not os.path.isdir(directory):
        print("The specified directory does not exist.")
        return

    files = list_files(directory)
    files_to_delete = []

    for file in files:
        ext = get_file_extension(file)
        if ext not in ALLOWED_EXTENSIONS:
            files_to_delete.append(file)
    
    if not files_to_delete:
        print("No files with disallowed extensions found.")
        return

    print("Files with disallowed extensions:")
    for file in files_to_delete:
        print(f"File: {file} (Extension: {get_file_extension(file)})")
    
    user_input = input("Do you want to delete all of these files? (yes/no): ").strip().lower()
    if user_input == 'yes':
        for file in files_to_delete:
            file_path = os.path.join(directory, file)
            os.remove(file_path)
            print(f"Deleted: {file}")
    else:
        print("No files were deleted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find and optionally delete files with disallowed extensions.')
    parser.add_argument('directory', type=str, help='Path to the directory to manage')
    args = parser.parse_args()
    
    main(args.directory)
