import os
import torch
from transformers import AutoModelForImageClassification, AutoProcessor
from PIL import Image
from torchvision import transforms
from tqdm import tqdm
import sys

def load_model_and_processor(model_name):
    """
    Load the model and processor for the given model name.
    """
    model = AutoModelForImageClassification.from_pretrained(model_name)
    processor = AutoProcessor.from_pretrained(model_name)
    return model, processor

def tag_images(model, processor, image_folder, device):
    """
    Tag images in the specified folder using the provided model and processor.
    """
    # Define image transformations
    transform = transforms.Compose([
        transforms.Resize((processor.size, processor.size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=processor.image_mean, std=processor.image_std)
    ])
    
    # Get list of image files
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('jpg', 'jpeg', 'png'))]
    
    # Process each image
    for image_file in tqdm(image_files, desc="Tagging images"):
        # Open and transform image
        image_path = os.path.join(image_folder, image_file)
        image = Image.open(image_path).convert("RGB")
        image_tensor = transform(image).unsqueeze(0).to(device)
        
        # Run inference
        with torch.no_grad():
            outputs = model(image_tensor)
        
        # Get tags
        probs = torch.softmax(outputs.logits, dim=-1)
        top_probs, top_labels = torch.topk(probs, 5)  # Get top 5 tags
        tags = [(processor.id2label[label.item()], prob.item()) for label, prob in zip(top_labels[0], top_probs[0])]
        
        # Write results to a file with the same name as the image
        result_file_path = os.path.join(image_folder, f"{os.path.splitext(image_file)[0]}.txt")
        with open(result_file_path, "w") as f:
            for tag, prob in tags:
                f.write(f"{tag}: {prob:.4f}\n")
    
    print("Tagging completed. Results saved to text files.")

def main():
    # Check if directory path is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python tag_images.py <image_folder>")
        sys.exit(1)

    image_folder = sys.argv[1]

    # Check if the provided directory exists
    if not os.path.isdir(image_folder):
        print(f"Error: Directory '{image_folder}' does not exist.")
        sys.exit(1)
    
    # Configuration
    model_name = "SmilingWolf/wd-swinv2-tagger-v3"  # You can change this to any other SmilingWolf model
    
    # Load model and processor
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model, processor = load_model_and_processor(model_name)
    model.to(device)
    model.eval()
    
    # Tag images
    tag_images(model, processor, image_folder, device)

if __name__ == "__main__":
    main()

