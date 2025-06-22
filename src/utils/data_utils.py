import os
import requests
import zipfile
import shutil

class DataDownloader:
    def __init__(self, save_data_dir: str,
                 data_url: str = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"):
        self.save_data_dir = save_data_dir
        self.url = data_url
        self.zip_path = os.path.join(self.save_data_dir, "ml-latest-small.zip")
        self.extracted_folder = os.path.join(self.save_data_dir, "ml-latest-small")
        self.target_folder = os.path.join(self.save_data_dir, "dataset")
        self.csv_path = os.path.join(self.target_folder, "movies.csv")

    def download(self):
        if not os.path.exists(self.csv_path):
            os.makedirs(self.save_data_dir, exist_ok=True)

            print("Downloading MovieLens dataset...")
            r = requests.get(self.url)
            with open(self.zip_path, "wb") as f:
                f.write(r.content)

            print("Extracting...")
            with zipfile.ZipFile(self.zip_path, "r") as zip_ref:
                zip_ref.extractall(self.save_data_dir)

            os.remove(self.zip_path)
            
            # Rename extracted folder to 'data'
            if os.path.exists(self.target_folder):
                shutil.rmtree(self.target_folder)

            os.rename(self.extracted_folder, self.target_folder)
            print("Done.")
        else:
            print("MovieLens dataset already exists.")
