from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import sys
import os
import zipfile
import requests
from tqdm import tqdm

# Global Variables
q, model, default_device, device_info, samplerate = None, None, None, None, None

def download_file(url, file_name=None):
    try:
        # Extract the file name from the URL if not provided
        if not file_name:
            file_name = url.split('/')[-1]

        # Check if the file already exists in the current directory
        if os.path.exists(file_name):
            print("[INFO] File already exists. Skipping download.")
            return

        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        
        # Open the file in binary write mode and write the content
        with open(file_name, 'wb') as file:
            # Get the total file size in bytes
            total_size = int(response.headers.get('content-length', 0))
            # Initialize the progress bar
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
            for data in response.iter_content(chunk_size=1024):
                # Write data to file
                file.write(data)
                # Update the progress bar
                progress_bar.update(len(data))
            progress_bar.close()
        
        print("[INFO] File downloaded successfully!")
    except Exception as e:
        print("[ERROR] Error downloading file:", e)

def unzip_file(zip_file, extract_to):
    try:
        # Check if the zip file exists
        if not os.path.exists(zip_file):
            print("[ERROR] Zip file not found!")
            return
        
        # Create the extraction directory if it doesn't exist
        if not os.path.exists(extract_to):
            os.makedirs(extract_to)
        
        # Open the zip file for reading
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # Extract all files to the specified directory
            zip_ref.extractall(extract_to)
        
        print("[DEBUG] File unzipped successfully!")
    except Exception as e:
        print(f"[ERROR] Error unzipping file: {e}")

def init():
    global q, model, default_device, device_info, samplerate
    model_path = ""
    possible_paths = ["vosk-model-en-in-0.5", "vosk-model-small-en-in-0.4"]
    for path in possible_paths:
        if os.path.exists(path):
            model_path = path
            print(f"[DEBUG] Model Path = {model_path}")
            break
    if model_path == "":
        while True:
            print("Choose Which Model to Download?\n1. Large Model\n2. Small Model")
            io2 = input("Enter 1 or 2:")
            try:
                if io2 == "1":
                    print("[INFO] Downloading Large Model... 1GB apprx.")
                    model_path = possible_paths[0]
                    download_file("https://alphacephei.com/vosk/models/vosk-model-en-in-0.5.zip", f"{possible_paths[0]}.zip")
                    unzip_file(f"{possible_paths[0]}.zip", ".")
                    break
                elif io2 == "2":
                    print("[INFO] Downloading Small Model... 36MB apprx.")
                    model_path = possible_paths[1]
                    download_file("https://alphacephei.com/vosk/models/vosk-model-small-en-in-0.4.zip", f"{possible_paths[1]}.zip")
                    unzip_file(f"{possible_paths[1]}.zip", ".")
                    break
            except Exception:
                print("[ERROR] An Error Occured!")
                sys.exit(-1)
            else:
                print("[WARNING] Incorrect Value")
    
    q = queue.Queue()
    model = Model(model_path=model_path)
    default_device = sd.default.device
    device_info = sd.query_devices(default_device, "input")
    samplerate = int(device_info["default_samplerate"])

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def stt():

    
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=default_device, dtype="int16", channels=1, callback=callback):
        
        rec = KaldiRecognizer(model, samplerate)

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                print(rec.Result())
            else:
                print(rec.PartialResult())
