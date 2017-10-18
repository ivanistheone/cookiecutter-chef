import os
import zipfile
from utils.downloader import read

class HTMLWriter():
    """
        Class for writing zipfiles
    """

    zf = None               # Zip file to write to
    write_to_path = None    # Where to write zip file

    def __init__(self, write_to_path):
        """ Args: write_to_path: (str) where to write zip file """
        self.map = {}                       # Keeps track of content to write to csv
        self.write_to_path = write_to_path  # Where to write zip file

    def __enter__(self):
        """ Called when opening context (e.g. with HTMLWriter() as writer: ) """
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        """ Called when closing context """
        self.close()

    def _write_to_zipfile(self, filename, content):
        if filename not in self.zf.namelist():
            info = zipfile.ZipInfo(filename, date_time=(2013, 3, 14, 1, 59, 26))
            info.comment = "HTML FILE".encode()
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 0
            self.zf.writestr(info, content)

    def _copy_to_zipfile(self, filename):
        if filename not in self.zf.namelist():
            self.zf.write(filename)

    """ USER-FACING METHODS """

    def open(self):
        """ open: Opens zipfile to write to
            Args: None
            Returns: None
        """
        self.zf = zipfile.ZipFile(self.write_to_path, "w")

    def close(self):
        """ close: Close zipfile when done
            Args: None
            Returns: None
        """
        self.zf.close()

    def write_contents(self, filename, contents, directory="src"):
        """ write_contents: Write contents to filename in zip
            Args:
                contents: (str) contents of file
                filename: (str) name of file in zip
                directory: (str) directory in zipfile to write file to (optional)
            Returns: path to file in zip
        """
        filepath = "{}/{}".format(directory, filename)
        self._write_to_zipfile(filepath, contents)
        return filepath

    def write_file(self, filepath):
        """ write_file: Write file to zip
            Args:
                filepath: (str) location to local file
                directory: (str) directory in zipfile to write file to (optional)
            Returns: path to file in zip
        """
        self._copy_to_zipfile(filepath)
        return filepath

    def write_url(self, url, filename, directory="src"):
        """ write_url: Write contents from url to filename in zip
            Args:
                url: (str) url to file to download
                filename: (str) name of file in zip
                directory: (str) directory in zipfile to write file to (optional)
            Returns: path to file in zip
        """
        return self.write_contents(filename, read(url), directory=directory)

    def write_main_file(self, contents):
        """ write_main_file: Write main index file to zip
            Args:
                contents: (str) contents of file
            Returns: path to file in zip
        """
        self._write_to_zipfile('index.html', contents)
