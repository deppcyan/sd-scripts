import argparse
import os
import numpy as np
import onnxruntime as rt
import pandas as pd
from PIL import Image
from tqdm import tqdm
import huggingface_hub

# Constants
MODEL_FILENAME = "model.onnx"
LABEL_FILENAME = "selected_tags.csv"

# Define the models
MODEL_REPOS = {
    "SmilingWolf/wd-v1-4-swinv2-tagger-v2": "/Users/johnny/models/wd-v1-4-swinv2-tagger-v2",
    # Add other models here if needed
}

# Load labels
def load_labels(dataframe):
    kaomojis = [
        "0_0", "(o)_(o)", "+_+", "+_-", "._.", "<o>_<o>", "<|>_<|>", "=_=", ">_<",
        "3_3", "6_9", ">_o", "@_@", "^_^", "o_o", "u_u", "x_x", "|_|", "||_||"
    ]
    name_series = dataframe["name"]
    name_series = name_series.map(
        lambda x: x.replace("_", " ") if x not in kaomojis else x
    )
    tag_names = name_series.tolist()
    rating_indexes = list(np.where(dataframe["category"] == 9)[0])
    general_indexes = list(np.where(dataframe["category"] == 0)[0])
    character_indexes = list(np.where(dataframe["category"] == 4)[0])
    return tag_names, rating_indexes, general_indexes, character_indexes

# Prepare image
def prepare_image(image, target_size):
    # Ensure image is in RGB mode if not already
    image = image.convert("RGB")

    image_shape = image.size
    max_dim = max(image_shape)
    pad_left = (max_dim - image_shape[0]) // 2
    pad_top = (max_dim - image_shape[1]) // 2

    padded_image = Image.new("RGB", (max_dim, max_dim), (255, 255, 255))
    padded_image.paste(image, (pad_left, pad_top))

    if max_dim != target_size:
        padded_image = padded_image.resize(
            (target_size, target_size),
            Image.BICUBIC,
        )

    image_array = np.asarray(padded_image, dtype=np.float32)
    image_array = image_array[:, :, ::-1]
    return np.expand_dims(image_array, axis=0)

# Maximum Cut Thresholding (MCut)
def mcut_threshold(probs):
    sorted_probs = probs[probs.argsort()[::-1]]
    difs = sorted_probs[:-1] - sorted_probs[1:]
    t = difs.argmax()
    thresh = (sorted_probs[t] + sorted_probs[t + 1]) / 2
    return thresh

# Predictor class
class Predictor:
    def __init__(self):
        self.model_target_size = None
        self.last_loaded_repo = None

    def download_model(self, model_repo):
        csv_path = huggingface_hub.hf_hub_download(model_repo, LABEL_FILENAME)
        model_path = huggingface_hub.hf_hub_download(model_repo, MODEL_FILENAME)
        return csv_path, model_path

    def load_model(self, model_repo):
        if model_repo == self.last_loaded_repo:
            return

        csv_path, model_path = self.download_model(model_repo)
        tags_df = pd.read_csv(csv_path)
        sep_tags = load_labels(tags_df)

        self.tag_names = sep_tags[0]
        self.rating_indexes = sep_tags[1]
        self.general_indexes = sep_tags[2]
        self.character_indexes = sep_tags[3]

        model = rt.InferenceSession(model_path)
        _, height, width, _ = model.get_inputs()[0].shape
        self.model_target_size = height

        self.last_loaded_repo = model_repo
        self.model = model

    def predict(self, image, model_repo, general_thresh, general_mcut_enabled, character_thresh, character_mcut_enabled):
        self.load_model(model_repo)
        image = prepare_image(image, self.model_target_size)

        input_name = self.model.get_inputs()[0].name
        label_name = self.model.get_outputs()[0].name
        preds = self.model.run([label_name], {input_name: image})[0]

        labels = list(zip(self.tag_names, preds[0].astype(float)))

        ratings_names = [labels[i] for i in self.rating_indexes]
        rating = dict(ratings_names)

        general_names = [labels[i] for i in self.general_indexes]
        if general_mcut_enabled:
            general_probs = np.array([x[1] for x in general_names])
            general_thresh = mcut_threshold(general_probs)
        general_res = [x for x in general_names if x[1] > general_thresh]
        general_res = dict(general_res)

        character_names = [labels[i] for i in self.character_indexes]
        if character_mcut_enabled:
            character_probs = np.array([x[1] for x in character_names])
            character_thresh = mcut_threshold(character_probs)
            character_thresh = max(0.15, character_thresh)
        character_res = [x for x in character_names if x[1] > character_thresh]
        character_res = dict(character_res)

        return rating, character_res, general_res

def format_tags(tags_dict, add_tags=None):
    """
    Format the dictionary of tags into a comma-separated string.
    """
    # Extract and sort the tags
    sorted_tags = sorted(tags_dict.keys())

    # Prepend the additional tags if provided
    if add_tags:
        sorted_tags = add_tags + sorted_tags
    
    # Join the tags into a comma-separated string
    formatted_tags = ", ".join(sorted_tags)
    
    return formatted_tags

def tag_images(image_folder, model_name, general_thresh, general_mcut_enabled, character_thresh, character_mcut_enabled, add_tags):
    predictor = Predictor()
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('jpg', 'jpeg', 'png'))]

    for image_file in tqdm(image_files, desc="Tagging images"):
        image_path = os.path.join(image_folder, image_file)
        image = Image.open(image_path).convert("RGB")
        rating, character_res, general_res = predictor.predict(
            image,
            model_name,
            general_thresh,
            general_mcut_enabled,
            character_thresh,
            character_mcut_enabled
        )
        
        tags = format_tags(general_res, add_tags)
        print(tags)
        
        output_file = os.path.join(image_folder, f"{os.path.splitext(image_file)[0]}.txt")
        with open(output_file, "w") as f:
            f.write(f"{tags}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image_folder", help="Path to the folder containing images")
    parser.add_argument("--model_name", default="SmilingWolf/wd-v1-4-swinv2-tagger-v2", help="Hugging Face model name")
    parser.add_argument("--general_thresh", type=float, default=0.35, help="Threshold for general tags")
    parser.add_argument("--general_mcut_enabled", action="store_true", help="Use MCut threshold for general tags")
    parser.add_argument("--character_thresh", type=float, default=0.85, help="Threshold for character tags")
    parser.add_argument("--character_mcut_enabled", action="store_true", help="Use MCut threshold for character tags")
    parser.add_argument("--add_tags", nargs="+", help="List of tags to prepend to each image's tags")
    args = parser.parse_args()

    tag_images(
        args.image_folder,
        args.model_name,
        args.general_thresh,
        args.general_mcut_enabled,
        args.character_thresh,
        args.character_mcut_enabled,
        args.add_tags
    )

if __name__ == "__main__":
    main()
