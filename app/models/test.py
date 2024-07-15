import os
from sqlalchemy import String
from sqlalchemy.ext.declarative import declared_attr


class FileField(String):
    def __init__(self, storage_manager, *args, **kwargs):
        self.storage_manager = storage_manager
        super(FileField, self).__init__(*args, **kwargs)

    @property
    def url(self):
        return self.storage_manager.get_file_url(self.path)

    @property
    def filename(self):
        return os.path.basename(self.path)

    @property
    def file(self):
        return self.storage_manager.get_file(self.path)

    @property
    def file_extension(self):
        return os.path.splitext(self.path)[1]

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    def __set__(self, instance, value):
        instance.__dict__['_file_path'] = value
        self.path = value

    def __get__(self, instance, owner):
        return instance.__dict__.get('_file_path', None)

    def delete_file(self):
        self.storage_manager.delete_file(self.path)
