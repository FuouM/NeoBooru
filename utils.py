from pathlib import Path
import os
import re

def save_txt_file(txt_path, _list):
    with open(txt_path, 'w') as writer:
        for i in list:
            writer.write(i + ", ")
    print("Saved text file.")

def save_txt_file_char_mode(txt_path, char, gen):
    with open(txt_path, 'w') as writer:
        writer.write("Character:\n")
        for i in char:
            writer.write(i + "\n")
        writer.write("\nGenerals:\n")
        for i in gen:
            writer.write(i + "\n")
                
    print("Saved text file.")

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

def remove_non_words(lst):
    return [s for s in lst if any(c.isalpha() for c in s)]

def sanitize_filename(name):
    # Replace characters that are not allowed in Windows file names with underscores
    return re.sub(r'[<>:"/\\|?*]', '', name)

def rename_file(filepath, *string_lists):
    # join the elements of each list with commas and concatenate them with underscores
    new_name = '__'.join([','.join(lst) for lst in string_lists])
    new_name = sanitize_filename(new_name)
    
    # add the new name to the file path, replacing the original file name
    filename, ext = os.path.splitext(os.path.basename(filepath))
    new_filename = filename[:10] + ext
    new_path = os.path.join(os.path.dirname(filepath), f"{new_name}_{new_filename}")

    # rename the file
    os.rename(filepath, new_path)
    
    return new_path
