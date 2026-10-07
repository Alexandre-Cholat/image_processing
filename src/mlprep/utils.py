import hashlib
import shutil
import click
import numpy as np
from PIL import Image
import os
from collections import defaultdict
from tqdm import tqdm

def get_all_jpg_files(directory):
    """
    Finds all .jpg files in a folder and its subfolders 
    and returns them as a list of full file paths.
    """
    jpg_files = []
    
    # os.walk yields a 3-tuple: (current_path, directories_in_path, files_in_path)
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Use .lower() to ensure we catch .JPG as well as .jpg
            if file.lower().endswith(".jpg"):
                # Combine the directory path and filename correctly for any OS
                full_path = os.path.join(root, file)
                jpg_files.append(full_path)
                
    return jpg_files

def get_file_hash(filepath, chunk_size=65536):
    """
    Computes the SHA-256 hash of a file.
    Reads the file in chunks to avoid memory issues with large files.
    """
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    except (OSError, IOError) as e:
        print(f"Could not read file {filepath}: {e}")
        return None

def find_duplicate_files(file_paths):
    """
    Takes a list of file paths and returns a dictionary where:
    - The key is the file hash.
    - The value is a list of file paths that share that hash.
    Only groups containing more than one file (actual duplicates) are returned.
    """
    hash_map = defaultdict(list)

    for path in file_paths:
        # Ensure the path exists and is actually a file
        if os.path.isfile(path):
            file_hash = get_file_hash(path)
            if file_hash:
                hash_map[file_hash].append(path)

    # Filter the dictionary to only include entries that have duplicates
    # (i.e., the list of paths for that hash must be longer than 1)
    duplicates = {
        hash_val: paths 
        for hash_val, paths in hash_map.items() 
        if len(paths) > 1
    }

    return duplicates

def validity_check(image):
    try:
        img = Image.open(image)
        img.verify()  # Checks if file is broken
        img.close()
    except (IOError, SyntaxError):
        return False

    return True

def target_existance(target):
    # create target if doesnt exist:
    if not os.path.exists(target):
        os.makedirs(target)
    else:
        if any(files for _, _, files in os.walk(target)):
            if not click.confirm(
                f"Warning: target directory '{target}' already contains files. Continue?",
                default=False,
            ):
                raise click.Abort()

def resize_and_pad(img, target_w, target_h):
    """
    Resizes image maintaining aspect ratio and adds black padding 
    to reach the exact target width and height.
    """
    # 1. Calculate the aspect ratio scaling
    original_w, original_h = img.size
    ratio = min(target_w / original_w, target_h / original_h)
    new_size = (int(original_w * ratio), int(original_h * ratio))

    # 2. Resize the image using high-quality Resampling
    # Note: We use Image.Resampling.LANCZOS for high quality
    resized_img = img.resize(new_size, Image.Resampling.LANCZOS)

    # 3. Create a new black background canvas
    # "RGB" mode is used to ensure compatibility with .jpg
    new_img = Image.new("RGB", (target_w, target_h), (0, 0, 0))

    # 4. Calculate position to center the image
    offset_x = (target_w - new_size[0]) // 2
    offset_y = (target_h - new_size[1]) // 2

    # 5. Paste the resized image onto the canvas
    new_img.paste(resized_img, (offset_x, offset_y))
    
    return new_img


# main function
def prep_img(source, target, H, W):
    # get .JPG
    img_list = get_all_jpg_files(source)
    click.echo(f"{len(img_list)} .jpg found.")

    # check if already exists, warn user if contains files
    target_existance(target)

    # find dupilicates :
    found_duplicates = find_duplicate_files(img_list)
    
    sum = 0
    if found_duplicates:
        
        for file_hash, paths in found_duplicates.items():
            for p in paths:
                sum = sum +1

    click.echo(f"Found {sum} dupilcates.")

    # Tracking variables
    seen_hashes = set()
    processed_count = 0

    # Process files
    # progress bar
    pbar = tqdm(img_list, desc="Processing Images", unit="img")

    for path in pbar:
        pbar.set_postfix({"ok": processed_count})

        # Check for duplicates via hash
        file_hash = get_file_hash(path)
        
        if file_hash in seen_hashes:
            continue  # Skip this file, it's a duplicate

        # Check for corruption
        if not validity_check(path):
            print(f"[ERROR] Corrupted file detected and skipped: {path}")
            continue # Skip this file

        # If we reach here, the file is unique and healthy
        try:

            with Image.open(path) as img:
                # Convert to RGB (important if source is grayscale or RGBA)
                img = img.convert("RGB")
                
                # Perform the resize and padding
                final_img = resize_and_pad(img, W, H)

                # Generate clean filename
                processed_count += 1
                new_filename = f"image_{processed_count:05d}.jpg"
                destination = os.path.join(target, new_filename)

                # Save the processed image
                final_img.save(destination, "JPEG", quality=95)
                
                # Mark hash as seen
                seen_hashes.add(file_hash)
            
        except Exception as e:
            print(f"[ERROR] Could not move {path}: {e}")

    print(f"Successfully moved:  {processed_count} files to {target}")



@click.command()
@click.option('--H', default=256, help='Target image height.')
@click.option('--W', default=256, help='Target image width.')
@click.option('--source', default='images', help='The image directory.')
@click.option('--target', default='output', help='The directory to save processed images.')

def prep_img_logic(source, target, H, W):
    """
    Searches all directories & sub-directories in SOURCE_DIR
    recursivelly for .jpg files. Creates new padded images at
    desired size in TARGET_DIR.
    """
    prep_img(source, target, H, W)












    

