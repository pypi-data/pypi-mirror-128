import os
    
def get_files_from_directory(dir_path, extension_type=''):
    files = [f.path for f in os.scandir(dir_path) if f.is_file()]
    if len(extension_type) > 0:
        files = [f.path for f in os.scandir(dir_path) if f.is_file() and f.path.endswith('.'+extension_type)]
    return files