from openai import OpenAI
import os

class OpenAiJourneyUtils:
    """
    Utility class for generating images using OpenAI image models within the journey game.
    It manages OpenAI client initialization, interaction tracking, and provides a simple
    interface for creating images from text prompts.
    """

    def __init__(self):
        """
        Initializes the OpenAI client using the API key from environment variables
        and resets the interaction counter for the current session.
        """
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.interactions_count = 0 

    def get_client(self):
        """
        Returns the initialized OpenAI client instance.
        This allows other components to reuse the authenticated client
        without creating additional connections.
        """
        return self.client
    
    def get_img(self, model_name: str, prompt: str) -> str:
        """
        Generates an image from the given text prompt using the specified OpenAI model.
        Returns the URL of the generated image, or raises a RuntimeError if
        image generation fails.
        """
        try:
            image_response = self.client.images.generate(
                model=model_name,
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            return image_response.data[0].url
        except Exception as e:
            raise RuntimeError(f"Image generation failed: {str(e)}")
