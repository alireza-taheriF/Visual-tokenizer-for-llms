import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

class VisualFeatureExtractor:
    def __init__(self, model_name="openai/clip-vit-base-patch32", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.model = CLIPModel.from_pretrained(model_name).to(self.device)

    def extract_features(self, image_path):
        image = Image.open(image_path).convert("RGB")
        inputs =self.processor(images=image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model.vision_model(**inputs)
        return outputs.pooler_output.squeeze(0).cpu()
    
if __name__ == "__main__":
    extractor = VisualFeatureExtractor()
    emb = extractor.extract_features("data/images/sample1.jpg")
    print(f"Feature shape: {emb.shape}")