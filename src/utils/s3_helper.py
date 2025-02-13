import boto3
import os

S3_BUCKET = "pallavi-data-bucket"
LOCAL_FOLDER = "data/"

s3_client = boto3.client("s3")


def upload_files():
    """Uploads CSV files from the local 'data/' folder to S3."""
    if not os.path.exists(LOCAL_FOLDER):
        print(f"Folder {LOCAL_FOLDER} does not exist. Creating...")
        os.makedirs(LOCAL_FOLDER)

    for file in os.listdir(LOCAL_FOLDER):
        if file.endswith(".csv"):
            file_path = os.path.join(LOCAL_FOLDER, file)
            s3_client.upload_file(file_path, S3_BUCKET, f"csv-files/{file}")
            print(f"Uploaded {file} to S3 bucket {S3_BUCKET}")


if __name__ == "__main__":
    upload_files()
