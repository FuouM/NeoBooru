from pathlib import Path

def load_tags(tags_path):
    with open(tags_path, "r") as tags_stream:
        tags = [tag for tag in (tag.strip() for tag in tags_stream) if tag]
        return tags
    
def get_file_paths_in_directory(path, patterns):
    return [
        str(file_path)
        for pattern in patterns
        for file_path in Path(path).rglob(pattern)
    ]


def get_image_file_paths_recursive(folder_path, patterns_string):
    patterns = patterns_string.split(",")

    return get_file_paths_in_directory(folder_path, patterns)
