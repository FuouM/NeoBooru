import os
import argparse
import sys
import time
import tensorflow as tf
import utils
from natural_sort import natural_sorted
from evaluate import evaluate_image

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(
        prog="NeoBooru",
        description="""Automatic Anime image Tagging using DeepDanbooru.
        Supported formats: PNG, JPG, JPEG, GIF""")
    
    parser.add_argument("--gpu", 
        dest="gpu_id", help="GPU device id to use (Default=0)", default=0, type=int)
    
    parser.add_argument("--cpu",
        dest="cpu", help="CPU only mode", action="store_true")
    
    parser.add_argument("--model",
        dest="model_path", help="Path to model file", type=str, required=True)
    
    parser.add_argument("--tags",
        dest="tags_path", help="Path to tags file (txt)", type=str, required=True)
    
    parser.add_argument("--chartag",
        dest="char_path", help="Path to character tags file (txt)", type=str)

    parser.add_argument("--target",
        dest="target_path", help="Path to image/folder", type=str, required=True)

    parser.add_argument("--threshold",
        dest="threshold", help="Threshold for tag confidence. (Default=0.5 [0.1 - 0.99])", default=0.5, type=float)

    parser.add_argument("--limit",
        dest="tag_limit", help="Limit for amount of tags. (Default=5). Doesn't affect character tags if --chartag is provided.",
        default=5, type=int)
    
    parser.add_argument("--inplace",
        dest="inplace", help="File renaming mode (No txt). Format: char_names__B__C", action="store_true")
    
    parser.add_argument("--verbose",
        dest="verbose", help="Print the tags for each successful image", action="store_true")
    
    args = parser.parse_args()

    if not os.path.isfile(args.model_path):
        parser.error("Model file not found.")

    if not os.path.isfile(args.tags_path):
        parser.error("Tags file not found.")

    if not 0.1 <= args.threshold <= 0.99:
        parser.error("Threshold should be between 0.1 and 0.99.")

    if args.tag_limit <= 0:
        parser.error("Limit should be greater than 0.")

    return args
    
def main():
    # CONSTANTS
    compile_model = False
    verbose = False
    save_txt = True
    allow_folder = True
    
    # FOLDER FILE EXTENSIONS
    folder_filters = "*.[Pp][Nn][Gg],*.[Jj][Pp][Gg],*.[Jj][Pp][Ee][Gg],*.[Gg][Ii][Ff]"

    # Set up
    args = parse_args()
    threshold = args.threshold
    target_path = args.target_path
    model_path = args.model_path
    tags_path = args.tags_path
    char_path = args.char_path
    tag_limit = args.tag_limit
    is_inplace = args.inplace
    is_verbose = args.verbose
    
    devices = tf.config.list_physical_devices('GPU')
    if not args.cpu and len(devices) > 0:
        print('GPU is available')
        print(devices)
        tf.config.set_visible_devices(devices[args.gpu_id], 'GPU')
    else:
        print('GPU is not available. CPU mode running.')
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        tf.config.set_visible_devices([], 'GPU')


    target = []

    if os.path.isdir(target_path):
        target = utils.get_image_file_paths_recursive(target_path, folder_filters)
        target = natural_sorted(target)
        print(f"Folder mode: {len(target)} files to be tagged.")
    elif os.path.isfile(target_path):
        print("Single image mode.")
        target = [target_path]
    else:
        print("No image found. Exiting")
        sys.exit(1)

    
    if not os.path.isfile(model_path):
        print("No model found. Exiting")
        sys.exit(1)

    
    tags = utils.load_tags(tags_path)
    char_mode = False
    if char_path:
        print("Character and General tags separation Mode.")
        try:
            character_tags = utils.load_tags(char_path)
            char_mode = True
        except FileNotFoundError:
            print("Tag files not found. Just tags mode.")
    else:
        print("Just tags mode.")
        character_tags = []

    #Load model
    model_start_time = time.time()
    model = tf.keras.models.load_model(model_path, compile=compile_model)
    print(f"Model load time: {time.time() - model_start_time}s")
    # def separate_tags(tags, character_tags, limit):
    #     char = list()
    #     gen = list()
    #     for tag in tags:
    #         if tag in character_tags:
    #             char.append(tag)
    #         else:
    #             gen.append(tag)
    #     return char, gen[:limit]
    
    def separate_tags(tags, character_tags, limit):
        char = [tag for tag in tags if tag in character_tags]
        gen = [tag for tag in tags if tag not in character_tags][:limit]
        return char, gen

    total_start_time = time.time()
    for image_path in target:
        try:
            start_time = time.time()
            print(f"Tags of {image_path}:") # Print image path
            tag_score = [(tag, score) for tag, score in evaluate_image(image_path, model, tags, threshold)]
            sorted_list = sorted(tag_score, key=lambda x: x[1], reverse=True)
            tag_list = [x[0] for x in sorted_list]
            file_name = os.path.splitext(image_path)[0]
                
            if char_mode:
                char, gen = separate_tags(tag_list, character_tags, tag_limit)
            else:
                char, gen = (tag_list,), None
            if is_verbose:
                print(char)
                print()
                print(gen)
            if is_inplace:
                print(f"File renamed to {utils.rename_file(image_path, char, gen)}")
            else:
                if char_mode:
                    utils.save_txt_file_char_mode(f"{file_name}.txt", char, gen)
                else:
                    utils.save_txt_file(f"{file_name}.txt", char)
                print("txt_file saved")


            print(f"{time.time() - start_time:.3f}s") # Print elapsed time
        except:
            print(f"Error: {image_path}")
            pass

    print(f"Everything took {time.time() - total_start_time:.3f}s")
    
    
if __name__ == '__main__':
    main()
    