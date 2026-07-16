import gdown
import os
import shutil
import glob
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    urls = [
        "https://drive.google.com/drive/folders/1-Rf7O1H-Qsepdrr6coXN7BFsur1gke-g",
        "https://drive.google.com/drive/folders/123jgWrt18ousMRlasUjEwd9rrn76ksNS"
    ]
    temp_dir = "gdrive_temp"
    
    # Clean temporary folder if it exists
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    
    print(f"Downloading Google Drive folders to {temp_dir}...")
    try:
        for url in urls:
            print(f"Downloading folder: {url} ...")
            # download_folder downloads all files in the folder to the target directory
            gdown.download_folder(url=url, output=temp_dir, quiet=False, use_cookies=False)
        print("All folders downloaded successfully!")
        
        # Check files downloaded recursively
        total_files = 0
        for root, dirs, files_list in os.walk(temp_dir):
            for file in files_list:
                f = os.path.join(root, file)
                basename = file
                total_files += 1
                print(f"  - {basename} (size: {os.path.getsize(f)} bytes) from {root}")
                
                # Copy to correct workspace locations
                if "chi-tiet-chia-qua-canh" in basename.lower():
                    perf_dir = "performance dashboard"
                    os.makedirs(perf_dir, exist_ok=True)
                    dest = os.path.join(perf_dir, basename)
                    shutil.copy2(f, dest)
                    print(f"    Copied performance file to: {dest}")
                elif "transfer" in basename.lower():
                    dest = os.path.join(".", basename)
                    shutil.copy2(f, dest)
                    print(f"    Copied transfer file to: {dest}")
        print(f"Total files found recursively: {total_files}")
                
        # Clean up temp folder
        shutil.rmtree(temp_dir)
        print("Cleaned up temporary directory.")
        
    except Exception as e:
        print(f"Error downloading folder: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
