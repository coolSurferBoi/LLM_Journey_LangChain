from openai import OpenAI
import os

class OpenAiJourneyUtils:
    # Define supported models as class constant
    SUPPORTED_MODELS = {
    }
    MAX_INTERACTIONS = 5
    REFRESH_MESSAGE = (
        "\n\n Storyteller, Please try to end the story NOW!"
    )

    def __init__(self):
        """
        Initializes the GPTJourneyUtils instance.

        Args:
            client (openai.Client): The OpenAI API client instance to interact with OpenAI services.
        """
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.interactions_count = 0 

    def get_client(self):
        return self.client
    
    def get_img(self, model_name: str, prompt: str) -> str:
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