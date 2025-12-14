
import os
import shutil

def get_unique_filename(directory, filename):
    """
    Generates a unique filename if the file already exists in the destination.
    Example: 'image.jpg' -> 'image_1.jpg' -> 'image_2.jpg'
    """
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    
    # Check if file exists, if so, append a number
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}_{counter}{extension}"
        counter += 1
        
    return new_filename

def organize_files():
    print("--- 📂 File Organizer Tool ---")
    
    # Step 1: Get folder path
    folder_path = input("Enter folder path to organize: ").strip()
    
    # Remove quotes if user copied path as "C:\Path"
    folder_path = folder_path.replace('"', '')

    if not os.path.exists(folder_path):
        print("❌ Error: The specified folder does not exist.")
        return

    print(f"\nScanning: {folder_path} ...")
    
    # Counters for summary
    files_moved = 0
    folders_created = set()

    # Step 2: Scan Directory
    try:
        items = os.listdir(folder_path)
    except PermissionError:
        print("❌ Error: Permission denied accessing this folder.")
        return

    for item in items:
        source_path = os.path.join(folder_path, item)

        # Ignore directories, process only files
        if os.path.isfile(source_path):
            # Step 3: Extract Extension
            # Handle files without extension (e.g., README)
            if '.' not in item or item.startswith('.'):
                extension = "OTHERS"
            else:
                extension = item.split('.')[-1].lower()
            
            # Skip the script itself if it's inside the folder
            if item == "organizer.py":
                continue

            # Target folder name (e.g., 'JPG', 'PDF')
            target_folder_name = extension.upper()
            target_folder_path = os.path.join(folder_path, target_folder_name)

            # Step 4: Create Folder if not exists
            if not os.path.exists(target_folder_path):
                os.makedirs(target_folder_path)
                folders_created.add(target_folder_name)

            # Step 5: Move File Safely
            # Handle Duplicate Names
            final_filename = get_unique_filename(target_folder_path, item)
            destination_path = os.path.join(target_folder_path, final_filename)

            try:
                shutil.move(source_path, destination_path)
                files_moved += 1
                print(f"✅ Moved: {item} -> {target_folder_name}/{final_filename}")
            except Exception as e:
                print(f"❌ Error moving {item}: {e}")

    # Step 6: Print Summary
    print("\n--- 📊 Organization Summary ---")
    print(f"Total Files Moved: {files_moved}")
    print(f"Folders Created: {len(folders_created)} ({', '.join(folders_created)})")
    print("🎉 Organization Complete!")

if __name__ == "__main__":
    organize_files()