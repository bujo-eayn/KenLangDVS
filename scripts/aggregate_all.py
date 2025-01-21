import os
import requests
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pathlib import Path


# Authenticate and initialize Google Drive
def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)


# Upload file to Google Drive
def upload_to_drive(drive, file_path, folder_id=None):
    file = drive.CreateFile(
        {'parents': [{'id': folder_id}]} if folder_id else {})
    file.SetContentFile(file_path)
    file.Upload()
    print(f"Uploaded {file_path} to Google Drive (ID: {file['id']}).")
    return file['id']


# Download dataset
def download_dataset(name, url, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{name}.zip")
    print(f"Downloading {name}...")
    response = requests.get(url, stream=True)
    with open(output_path, "wb") as f:
        f.write(response.content)
    print(f"Downloaded {name} to {output_path}.")
    return output_path


# Main aggregation logic
def aggregate_all():
    datasets = [
        {"name": "Kencorpus", "url": "https://example.com/kencorpus.zip",
            "language": ["Swahili", "Dholuo", "Luhya"], "task": "NLP"},
        {"name": "thinkKenya", "url": "https://example.com/thinkkenya.zip",
            "language": ["Kidaw’ida", "Kalenjin", "Dholuo"], "task": "NLP"},
        {"name": "Leipzig Corpus", "url": "https://example.com/leipzig.zip",
            "language": ["Kikuyu"], "task": "NLP"},
        {"name": "Kikuyu-English Translation", "url": "https://example.com/kikuyu_translation.zip",
            "language": ["Kikuyu"], "task": "Translation"},
        {"name": "BibleTTS", "url": "https://example.com/bibletts.zip",
            "language": ["Kikuyu", "Swahili"], "task": "Speech"},
        {"name": "KenSwQuAD", "url": "https://example.com/kenswquad.zip",
            "language": ["Swahili"], "task": "QA"},
        {"name": "MasakhaNER", "url": "https://example.com/masakhaner.zip",
            "language": ["Swahili", "Luo"], "task": "NER"},
        {"name": "Swahili News", "url": "https://example.com/swahili_news.zip",
            "language": ["Swahili"], "task": "Sentiment Analysis"}
    ]

    drive = authenticate_drive()
    metadata = []

    for dataset in datasets:
        file_path = download_dataset(
            dataset['name'], dataset['url'], "/app/data/raw")
        drive_file_id = upload_to_drive(drive, file_path)
        metadata.append({
            "name": dataset["name"],
            "file_path": file_path,
            "google_drive_id": drive_file_id,
            "languages": dataset["language"],
            "task": dataset["task"],
            "source": dataset["url"]
        })

    # Save metadata
    metadata_path = "/app/data/metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"Metadata saved to {metadata_path}.")


if __name__ == "__main__":
    aggregate_all()
