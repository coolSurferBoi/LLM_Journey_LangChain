import os
from huggingface_hub import InferenceClient
from pathlib import Path
from PIL import Image


class HuggingFaceJourneysUtils:
    """
    Utility class for generating and saving images using supported Hugging Face text-to-image models.
    It manages model/provider validation, client initialization, interaction limits, and persistence
    of generated images to a static output directory for downstream use (e.g., web apps).
    """
    # Define supported models as class constant
    SUPPORTED_MODELS = {
        'black-forest-labs/FLUX.1-dev': 'together'
    }
    
    # Define constants
    OUTPUT_DIR = Path("static/HuggingFaceImages/generated")
    IMAGE_FILENAME = "hgfImage.png"
    MAX_INTERACTIONS = 5
    REFRESH_MESSAGE = (
        "\n\n Storyteller, Please try to end the story NOW!"
    )
    def __init__(self, model_name: str):
        """
        Initializes the Hugging Face inference client for a supported text-to-image model.
        Validates the model, configures the provider and authentication token, prepares the
        output directory, and sets generation parameters such as temperature.
        """
        if model_name not in self.SUPPORTED_MODELS:
            raise ValueError(f"Unsupported model: {model_name}")
        
        self.provider = self.SUPPORTED_MODELS[model_name]
        self.client = InferenceClient(
            provider=self.provider,
            token=os.getenv("HF_TOKEN")  # Use token instead of api_key
        )
        self.interactions_count = 0
        self.output_dir = self.OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_client(self) -> InferenceClient:
        """
        Returns the initialized Hugging Face InferenceClient instance.
        This allows external components to reuse the configured client
        without reinitializing authentication or provider settings.
        """
        return self.client
    
    def get_img(self, model_name: str, prompt: str) -> str:
        """
        Generates an image from the given text prompt using the specified model
        and saves it to the configured output directory. Returns the relative
        static path to the saved image, or raises a RuntimeError on failure.
        """
        try:
            img = self.client.text_to_image(prompt=prompt, model=model_name)
            return self._save_img(img)
        except Exception as e:
            raise RuntimeError(f"Image generation failed: {str(e)}")

    def _save_img(self, img: Image.Image) -> str:
        """
        Saves the generated PIL image to the configured output directory
        using a fixed filename. Returns the relative static path to the
        saved image for use in web responses or templates.
        """
        save_path = self.output_dir / self.IMAGE_FILENAME
        img.save(save_path)
        return f"/static/HuggingFaceImages/generated/{self.IMAGE_FILENAME}"