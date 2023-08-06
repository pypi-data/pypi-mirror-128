# Downloading Hungarian Wordnet from original source
import requests
import os
from importlib_resources import files


class WordNetDownloader:
    def __init__(self, url_wordnet="https://rgai.inf.u-szeged.hu/sites/rgai.inf.u-szeged.hu/files/HuWN.zip",
                 wordnet_zip_path=files("resources") / "HuWN.zip",
                 wordnet_xml_path=files("resources") / "HuWN_final4.xml"):
        self.wordnet_zip_file = wordnet_zip_path
        self.url_wordnet = url_wordnet
        self.wordnet_xml_path = wordnet_xml_path
        self.download_needed = False

    def check_existing_file(self):
        if not os.path.isfile(self.wordnet_xml_path):
            print("Wordnet xml file missing, downloading from original source.")
            self.download_needed = True
        else:
            self.download_needed = False

    def download(self):
        try:
            # downloading from original source
            data = requests.get(self.url_wordnet, allow_redirects=True)
            with open(self.wordnet_zip_file, 'wb') as file:
                file.write(data.content)
        except ValueError:
            print("Download failed.")

    def unzip(self):
        # unzipping
        os.system('unzip {} -d {}'.format(self.wordnet_zip_file, files("resources")))

    def cleanup(self):
        # deleting zip file
        os.remove(self.wordnet_zip_file)

    def run(self):
        self.check_existing_file()
        if self.download_needed:
            self.download()
            self.unzip()
            self.cleanup()


if __name__ == "__main__":
    downloader = WordNetDownloader()
    downloader.run()
