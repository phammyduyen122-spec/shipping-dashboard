import gdown
import os
import shutil
import glob
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    url = "https://drive.google.com/drive/folders/1-Rf7O1H-Qsepdrr6coXN7BFsur1gke-g"
    temp_dir = "gdrive_temp"
    
    # Clean temporary folder if it exists
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    
    print(f"Downloading Google Drive folder to {temp_dir}...")
    try:
        # download_folder downloads all files in the folder to the target directory
        gdown.download_folder(url=url, output=temp_dir, quiet=False, use_cookies=False)
        print("Folder downloaded successfully!")
        
        # Check files downloaded
        files = glob.glob(os.path.join(temp_dir, "*"))
        print(f"Files found in downloaded folder: {len(files)}")
        for f in files:
            basename = os.path.basename(f)
            print(f"  - {basename} (size: {os.path.getsize(f)} bytes)")
            
            # Copy to correct workspace locations
            if "chi-tiet-chia-qua-canh" in basename:
                perf_dir = "performance dashboard"
                os.makedirs(perf_dir, exist_ok=True)
                dest = os.path.join(perf_dir, basename)
                shutil.copy2(f, dest)
                print(f"    Copied performance file to: {dest}")
            elif "transfer" in basename:
                dest = os.path.join(".", basename)
                shutil.copy2(f, dest)
                print(f"    Copied transfer file to: {dest}")
                
        # Clean up temp folder
        shutil.rmtree(temp_dir)
        print("Cleaned up temporary directory.")
        
    except Exception as e:
        print(f"Error downloading folder: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
