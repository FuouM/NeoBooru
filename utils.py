from pathlib import Path
import tensorflow as tf

def save_txt_file(txt_path, _list):
    last_index = len(list)-1
    last_tag = _list[last_index]
    with open(txt_path, 'w') as writer:
        for i in list:
            if last_tag == i:
                writer.write(i)
                writer.close()
            else:
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

def is_gpu_available():
    return len(tf.config.list_physical_devices('GPU')) > 0