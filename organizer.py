import os
import shutil

def get_unique_path(destination_folder, filename):
    """
    Handles duplicate names by appending a number if the file already exists.
    Requirement: No file should be overwritten.
    """
    base, extension = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    
    while os.path.exists(os.path.join(destination_folder, unique_filename)):
        unique_filename = f"{base}_{counter}{extension}"
        counter += 1
        
    return os.path.join(destination_folder, unique_filename)

def organize_folder(target_path):
    """
    Scans a folder and moves files into subfolders based on their extensions.
    """
    if not os.path.isdir(target_path):
        print(f"Error: The path '{target_path}' is not a valid directory.")
        return

    print("Organizing...")
    
    files_moved = 0
    folders_created = set()

    try:
        # Scan all items in the directory
        for item in os.listdir(target_path):
            item_path = os.path.join(target_path, item)

            # Ignore folders; only process files
            if os.path.isfile(item_path):
                # Extract extension (e.g., .pdf, .jpg)
                _, extension = os.path.splitext(item)
                
                if not extension:
                    extension = ".no_extension"
                
                # Format folder name (removing the dot and making it uppercase)
                folder_name = extension[1:].upper() if extension.startswith('.') else extension.upper()
                dest_folder_path = os.path.join(target_path, folder_name)

                # Create folder dynamically if it doesn't exist
                if not os.path.exists(dest_folder_path):
                    os.makedirs(dest_folder_path)
                    folders_created.add(folder_name)

                # Move file safely with duplicate handling
                final_dest_path = get_unique_path(dest_folder_path, item)
                shutil.move(item_path, final_dest_path)
                files_moved += 1

        # Print summary
        print("-" * 30)
        print("Files moved successfully!")
        print(f"Total files moved: {files_moved}")
        print(f"Folders created: {len(folders_created)} ({', '.join(folders_created) if folders_created else 'None'})")
        print("-" * 30)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    while True:
        print("\n--- File Organizer System ---")
        print("1. Organize a Folder")
        print("5. Exit System")
        
        choice = input("\nEnter choice: ")

        if choice == '1':
            path = input("Enter folder path to organize: ").strip()
            # Clean path from quotes if user dragged and dropped folder
            path = path.replace('"', '').replace("'", "")
            organize_folder(path)
        elif choice == '5':
            print("Exiting System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 5.")

if __name__ == "__main__":
    main()