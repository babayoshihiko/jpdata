import zipfile
import os
import posixpath
import io
import sys
from typing import List, Union

def _repair_filename(raw_filename: str, encodings_to_try: List[str]) -> str:
    """
    Attempts to repair a mojibake (garbled) filename by using 'latin1' or 'cp437'
    as a lossless intermediary to get the original bytes, and then decoding those
    bytes with candidate encodings (e.g., cp932/Shift-JIS).

    This addresses issues where the filename was incorrectly decoded using
    a standard encoding when it should have used a specific encoding.

    :param raw_filename: The potentially garbled string filename from ZipInfo.
    :param encodings_to_try: A list of candidate encodings (e.g., ['cp932', 'utf-8']).
    :return: The repaired filename string, using the OS-specific path separator.
    """
    
    # Try both common ZIP intermediate encodings. One of these is likely the encoding
    # that Python used incorrectly to turn the original bytes into the garbled string.
    INTERMEDIATE_ENCODINGS = ['latin1', 'cp437']

    for intermediate_enc in INTERMEDIATE_ENCODINGS:
        # 1. Convert the garbled string back to raw bytes using the intermediate encoding.
        # This is a lossless way to recover the original byte sequence from the garbled string.
        try:
            raw_bytes = raw_filename.encode(intermediate_enc)
        except Exception:
            # Skip this intermediate encoding if encoding fails (highly unlikely with latin1/cp437)
            continue

        # 2. Try decoding the raw bytes with the candidate encodings
        for encoding in encodings_to_try:
            try:
                # Decode the bytes using the correct encoding (e.g., 'cp932')
                repaired_name = raw_bytes.decode(encoding, errors='strict')
                
                # Simple heuristic check: ensure the name isn't just garbage or empty
                if repaired_name and len(repaired_name.strip()) > 0:
                    # Clean up path separators and return
                    # This replaces forward and back slashes with the OS-specific separator
                    return repaired_name.replace('/', os.sep).replace('\\', os.sep)
            except UnicodeDecodeError:
                continue # Try the next encoding

    # 3. If all attempts fail, return the original name, but correct path separators.
    print(f"Warning: Could not repair name '{raw_filename}'. Using original with path fix.")
    return raw_filename.replace('/', os.sep).replace('\\', os.sep)


def robust_extractall(zip_path: str, destination_dir: str, preferred_encoding: str = 'cp932'):
    """
    Extracts a ZIP archive, attempting to correct filenames that were
    incorrectly encoded, typically addressing Japanese encoding issues (Shift-JIS/cp932).

    :param zip_path: Path to the ZIP file.
    :param destination_dir: Directory where the contents will be extracted.
    :param preferred_encoding: The primary encoding to try for Japanese filenames (default: 'cp932').
    """
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Set up the list of encodings to try (preferred first)
    encodings_to_try = [preferred_encoding, 'utf-8', 'shift_jis', 'euc_jp']

    print(f"Attempting to extract: {zip_path}")
    print(f"Destination: {destination_dir}")

    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            
            # Use 'zf.infolist()' to get raw information including the filename
            for member_info in zf.infolist():
                
                # Get the filename as Python has decoded it (may be garbled)
                corrupted_name = member_info.filename
                
                # Try to repair the filename
                fixed_name = _repair_filename(corrupted_name, encodings_to_try)
                
                # Create the full target path
                # os.path.join handles both Unix and Windows path construction
                target_path = os.path.join(destination_dir, fixed_name)
                
                # Sanity check: prevent path traversal attacks (e.g., names like '../../etc/passwd')
                if not os.path.abspath(target_path).startswith(os.path.abspath(destination_dir)):
                    print(f"Skipping potentially malicious path: {fixed_name}")
                    continue

                if member_info.is_dir():
                    # Create directories if they don't exist
                    if not os.path.exists(target_path):
                        os.makedirs(target_path)
                    print(f"Created directory: {fixed_name}")
                else:
                    # Ensure the containing directory exists for files
                    parent_dir = os.path.dirname(target_path)
                    if not os.path.exists(parent_dir):
                        os.makedirs(parent_dir)
                    
                    # Extract the file by streaming the content
                    with zf.open(member_info) as source, open(target_path, 'wb') as target:
                        print(f"Extracting file: {fixed_name}")
                        target.write(source.read())

            print("\nExtraction complete.")

    except zipfile.BadZipFile:
        print(f"Error: The file at {zip_path} is not a valid ZIP file.")
    except Exception as e:
        print(f"An unexpected error occurred during extraction: {e}")


def unzip_qgis_safe(folder_path, zip_file):
    """
    Safely unzip inside QGIS without filename mojibake.
    Handles CP932, UTF-8, backslashes, Yen signs, and bypasses PyQt.
    """
    zip_path = posixpath.join(folder_path, zip_file)

    robust_extractall(zip_path, folder_path)
