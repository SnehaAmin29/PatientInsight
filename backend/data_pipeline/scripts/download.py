import os
from dotenv import load_dotenv
import requests
import time
import sys
from pathlib import Path

# Load environment variables
load_dotenv()

# Access AWS credentials
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

def download_pmc_patients_dataset(output_dir: str) -> None:
    # Start time
    start_time = time.time()

    # Pointing to the start of the project
    root_path = Path(__file__).parent.parent.parent.parent.absolute()
    sys.path.append(str(root_path))
    output_dir = os.path.join(root_path, output_dir)
    print(f"Starting download to: {output_dir}")
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        url = "https://huggingface.co/datasets/zhengyun21/PMC-Patients/resolve/main/PMC-Patients.csv"
        output_path = os.path.join(output_dir, "PMC-Patients.csv")
        response = requests.get(url)
        response.raise_for_status()
        
        print("Downloading dataset")
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        print(f"Dataset downloaded to: {output_path}")
        print("Download completed successfully")
        
    except Exception as e:
        print(f"Download failed: {str(e)}")
        raise

    if os.path.exists(output_path):
        print('Download file exists. Successfully exiting the script')
    else:
        raise Exception('File not found in the download directory')
    
    # Calculating time elapsed
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time elapsed: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    print("Starting process to download data")
    output_dir = "backend/data_pipeline/data/raw"
    download_pmc_patients_dataset(output_dir)
