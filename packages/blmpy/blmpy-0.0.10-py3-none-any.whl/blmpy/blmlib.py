# import os

# class blmos:
#     def get_files_from_directory(self, dir_path, extension_type=''):
#         files = [f.path for f in os.scandir(dir_path) if f.is_file()]
#         if len(extension_type) > 0:
#             files = [f.path for f in os.scandir(dir_path) if f.is_file() and f.path.endswith('.'+extension_type)]
#         return files
import json

class blmjson:
    def load_json_file(self, filename):
        with open(filename) as f:
            tmp_data = f.read()
            while not (tmp_data[0].startswith('[') or tmp_data[0].startswith('{')):
                tmp_data = tmp_data[1:]
        return json.loads(tmp_data)


        