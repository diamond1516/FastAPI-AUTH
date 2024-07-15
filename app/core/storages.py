import os
from werkzeug.utils import secure_filename


class StorageManager:
    def save_file(self, file, filename=None):
        raise NotImplementedError

    def delete_file(self, file_path):
        raise NotImplementedError

    def get_file(self, file_path):
        raise NotImplementedError

    def get_file_url(self, file_path):
        raise NotImplementedError


class LocalFileManager(StorageManager):
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

    def save_file(self, file, filename=None):
        if filename is None:
            filename = secure_filename(file.filename)
        file_path = os.path.join(self.upload_folder, filename)
        with open(file_path, 'wb') as f:
            f.write(file.read())
        return file_path

    def delete_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    def get_file(self, file_path):
        if os.path.exists(file_path):
            return open(file_path, 'rb')
        raise FileNotFoundError("File not found")

    def get_file_url(self, file_path):
        return f'/files/{file_path}'  # Bu misol uchun oddiy URL
