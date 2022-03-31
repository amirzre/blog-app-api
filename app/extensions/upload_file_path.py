from os.path import basename, splitext


def get_file_name_ext(filepath):
    """Split name and extention of file"""

    base_name = basename(filepath)
    name, ext = splitext(base_name)
    return name, ext


def upload_file_path(instance, filename):
    """Create new name for files"""

    name, ext = get_file_name_ext(filename)
    final_name = f'{instance.id}-{instance.title}.{ext}'
    return f'blogs/{final_name}'
